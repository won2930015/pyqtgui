#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import bisect       # 导入二分模块
import collections  # 导入集合模块
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *   # 包含QTcpSocket(),QUdpSocket()等网络模块.

PORT = 9407         # 端口号
SIZEOF_UINT16 = 2   # 2表示两字节.
MAX_BOOKINGS_PER_DAY = 5    # 最大_预订_每_天[一天最大预订房间数]

# Key = date, value = list of room IDs
Bookings = collections.defaultdict(list)        # https://www.cnblogs.com/herbert/archive/2013/01/09/2852843.html
#                                               # collections::集合, defaultdict::默认_字典(KEY:value对)
#                                               # 创建Bookings为一个字典列表. -.-????


def printBookings():
    for key in sorted(Bookings):
        print(key, Bookings[key])
    print()


class Socket(QTcpSocket):

    def __init__(self, parent=None):
        super(Socket, self).__init__(parent)
        self.connect(self, SIGNAL("readyRead()"), self.readRequest)  # readyRead()::准备_读 信号
        self.connect(self, SIGNAL("disconnected()"), self.deleteLater)  # disconnected()::断开 信号
        self.nextBlockSize = 0  # 下一_块_尺寸

    def readRequest(self):      # readRequest::读_请求
        stream = QDataStream(self)
        stream.setVersion(QDataStream.Qt_4_2)

        if self.nextBlockSize == 0:
            if self.bytesAvailable() < SIZEOF_UINT16:   # bytesAvailable()::有效_字节 [返回 有效字节数值<SIZEOF_UINT16时 返回]
                return
            self.nextBlockSize = stream.readUInt16()
        if self.bytesAvailable() < self.nextBlockSize:  # 有效字节数值 与 读取的数值 不一致时 返回.
            return

        action = stream.readQString()    # 读取'动作[BOOK/UNBOOK]'
        date = QDate()          # 创建日期对象.
        if action in ("BOOK", "UNBOOK"):
            room = stream.readQString()     # 读取 房间号
            stream >> date              # 读取 日期
            bookings = Bookings.get(date.toPyDate())    # 获得给定日期[date]的预订清单, toPyDate::去_计算_日期.
            uroom = room    # uroom::房间副本[为什么要设置副本不太明白用意.]
        if action == "BOOK":
            if bookings is None:
                bookings = Bookings[date.toPyDate()]    # 如果是空列表的再次获得给定日期的预定清单列表.
            if len(bookings) < MAX_BOOKINGS_PER_DAY:    # MAX_BOOKINGS_PER_DAY::最大_预订_每_天[一天最大预订房间数]
                if uroom in bookings:
                    self.sendError("Cannot accept duplicate booking")   # 不能接受重复预订.
                else:
                    bisect.insort(bookings, uroom)
                    self.sendReply(action, room, date)  # sendReply::发送_答复
            else:
                self.sendError("{} is fully booked".format(     # x年x日预订已满.
                               date.toString(Qt.ISODate)))
        elif action == "UNBOOK":
            if bookings is None or uroom not in bookings:
                self.sendError("Cannot unbook nonexistent booking")     # 不能取消不存在的预订.
            else:
                bookings.remove(uroom)
                self.sendReply(action, room, date)  # sendReply::发送_答复
        else:
            self.sendError("Unrecognized request")  # 未识别的请求
        printBookings()

    def sendError(self, msg):
        reply = QByteArray()    # 答复
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString("ERROR")
        stream.writeQString(msg)
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        self.write(reply)

    def sendReply(self, action, room, date):
        reply = QByteArray()    # 答复
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString(action)
        stream.writeQString(room)
        stream << date
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        self.write(reply)


class TcpServer(QTcpServer):

    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)

    def incomingConnection(self, socketId):  # incomingConnection::进入_连接 ,socketId::客户端传来的socket对象.
        socket = Socket(self)
        socket.setSocketDescriptor(socketId)    # 设置_套接字_描述符
        

class BuildingServicesDlg(QPushButton):     # 构建_服务_窗口

    def __init__(self, parent=None):
        super(BuildingServicesDlg, self).__init__(
                "&Close Server", parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)    # WindowStaysOnTopHint::窗口_停留_到_顶部_提示[窗口顶置提示]

        self.loadBookings()
        self.tcpServer = TcpServer(self)
        if not self.tcpServer.listen(QHostAddress("0.0.0.0"), PORT):    # listen::监听
            QMessageBox.critical(self, "Building Services Server",      # critical::危险[危险窗口]
                    "Failed to start server: {}".format(
                    self.tcpServer.errorString()))
            self.close()
            return

        self.connect(self, SIGNAL("clicked()"), self.close)
        font = self.font()
        font.setPointSize(24)
        self.setFont(font)
        self.setWindowTitle("Building Services Server")


    def loadBookings(self):
        # Generate fake data    创建伪数据
        import random

        today = QDate.currentDate()
        for i in range(10):
            date = today.addDays(random.randint(7, 60))
            for j in range(random.randint(1, MAX_BOOKINGS_PER_DAY)):
                # Rooms are 001..534 excl. 100, 200, ..., 500
                floor = random.randint(0, 5)    # floor::层
                room = random.randint(1, 34)    # room::房号
                bookings = Bookings[date.toPyDate()]
                if len(bookings) >= MAX_BOOKINGS_PER_DAY:
                    continue
                bisect.insort(bookings, "{0:1d}{1:02d}".format(     # {0:1d}::一位整数, {1:02d}::两位整数前面不足位数用0填充.
                              floor, room))
        printBookings()


app = QApplication(sys.argv)
form = BuildingServicesDlg()
form.show()
form.move(0, 0)
app.exec_()

