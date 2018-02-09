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

import bisect       #导入二分模块
import collections  #导入集合模块
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

PORT = 9407         #端口号
SIZEOF_UINT16 = 2   #2表示两字节
MAX_BOOKINGS_PER_DAY = 5    #最大_预订_天数

# Key = date, value = list of room IDs
Bookings = collections.defaultdict(list)        #https://www.cnblogs.com/herbert/archive/2013/01/09/2852843.html
                                                #collections::集合, defaultdict::默认_字典(KEY:value对)
                                                #创建Bookings为一个字典列表. -.-????
def printBookings():
    for key in sorted(Bookings):
        print(key, Bookings[key])
    print()


class Socket(QTcpSocket):

    def __init__(self, parent=None):
        super(Socket, self).__init__(parent)
        self.connect(self, SIGNAL("readyRead()"), self.readRequest) #readyRead()::准备_读 信号
        self.connect(self, SIGNAL("disconnected()"), self.deleteLater)  #disconnected()::断开 信号
        self.nextBlockSize = 0  #下一_块_尺寸


    def readRequest(self):  #readRequest::读_请求
        stream = QDataStream(self)
        stream.setVersion(QDataStream.Qt_4_2)

        if self.nextBlockSize == 0:
            if self.bytesAvailable() < SIZEOF_UINT16:   #bytesAvailable()::字节_可用 [返回 字节可用数值<SIZEOF_UINT16时 返回]
                return
            self.nextBlockSize = stream.readUInt16()
        if self.bytesAvailable() < self.nextBlockSize:
            return

        action = stream.readQString()
        date = QDate()
        if action in ("BOOK", "UNBOOK"):
            room = stream.readQString()
            stream >> date
            bookings = Bookings.get(date.toPyDate())
            uroom = room
        if action == "BOOK":
            if bookings is None:
                bookings = Bookings[date.toPyDate()]
            if len(bookings) < MAX_BOOKINGS_PER_DAY:
                if uroom in bookings:
                    self.sendError("Cannot accept duplicate booking")   #不能接受重复预订.
                else:
                    bisect.insort(bookings, uroom)
                    self.sendReply(action, room, date)
            else:
                self.sendError("{} is fully booked".format(
                               date.toString(Qt.ISODate)))
        elif action == "UNBOOK":
            if bookings is None or uroom not in bookings:
                self.sendError("Cannot unbook nonexistent booking")
            else:
                bookings.remove(uroom)
                self.sendReply(action, room, date)
        else:
            self.sendError("Unrecognized request")
        printBookings()


    def sendError(self, msg):
        reply = QByteArray()
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString("ERROR")
        stream.writeQString(msg)
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        self.write(reply)


    def sendReply(self, action, room, date):
        reply = QByteArray()
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


    def incomingConnection(self, socketId):
        socket = Socket(self)
        socket.setSocketDescriptor(socketId)
        

class BuildingServicesDlg(QPushButton):

    def __init__(self, parent=None):
        super(BuildingServicesDlg, self).__init__(
                "&Close Server", parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.loadBookings()
        self.tcpServer = TcpServer(self)
        if not self.tcpServer.listen(QHostAddress("0.0.0.0"), PORT):
            QMessageBox.critical(self, "Building Services Server",
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
        # Generate fake data
        import random

        today = QDate.currentDate()
        for i in range(10):
            date = today.addDays(random.randint(7, 60))
            for j in range(random.randint(1, MAX_BOOKINGS_PER_DAY)):
                # Rooms are 001..534 excl. 100, 200, ..., 500
                floor = random.randint(0, 5)
                room = random.randint(1, 34)
                bookings = Bookings[date.toPyDate()]
                if len(bookings) >= MAX_BOOKINGS_PER_DAY:
                    continue
                bisect.insort(bookings, "{0:1d}{1:02d}".format(
                              floor, room))
        printBookings()


app = QApplication(sys.argv)
form = BuildingServicesDlg()
form.show()
form.move(0, 0)
app.exec_()

