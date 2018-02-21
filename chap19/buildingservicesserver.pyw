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
from PyQt4.QtNetwork import *   #包含QTcpSocket(),QUdpSocket()等网络模块.

PORT = 9407         #端口号
SIZEOF_UINT16 = 2   #2表示两字节
MAX_BOOKINGS_PER_DAY = 5    #最大_预订_每_天[一天最大预订房间数]

# Key = date, value = list of room IDs
Bookings = collections.defaultdict(list)        #https://www.cnblogs.com/herbert/archive/2013/01/09/2852843.html
                                                #collections::集合, defaultdict(list)::默认_字典(KEY:value对),list::value值的默认类型是list.
                                                #创建Bookings为一个字典列表. -.-????
def printBookings():
    for key in sorted(Bookings):
        print(key, Bookings[key])
    print()


class Thread(QThread):

    lock = QReadWriteLock() #QReadWriteLock::写_读_锁

    def __init__(self, socketId, parent):
        super(Thread, self).__init__(parent)
        self.socketId = socketId

        
    def run(self):
        socket = QTcpSocket()
        if not socket.setSocketDescriptor(self.socketId):   #setSocketDescriptor::设置_套接字_描述符
            self.emit(SIGNAL("error(int)"), socket.error())
            return
        while socket.state() == QAbstractSocket.ConnectedState: #QAbstractSocket::抽像套按字, ConnectedState::连接_状态
            nextBlockSize = 0
            stream = QDataStream(socket)
            stream.setVersion(QDataStream.Qt_4_2)
            if (socket.waitForReadyRead() and       #waitForReadyRead::等候_为_准备_读[在内置默认的时间内,进行阻塞并接收数据]
                socket.bytesAvailable() >= SIZEOF_UINT16):      #bytesAvailable::有效_字节
                nextBlockSize = stream.readUInt16()
            else:
                self.sendError(socket, "Cannot read client request")        #无法读客户端请求
                return
            if socket.bytesAvailable() < nextBlockSize:     #bytesAvailable::有效_字节 < 读取字节
                if (not socket.waitForReadyRead(60000) or   #waitForReadyRead(60000)::在最多60秒的时间内,进行阻塞并接收数据.
                    socket.bytesAvailable() < nextBlockSize):
                    self.sendError(socket, "Cannot read client data")   #无法读客户端数据.
                    return
            action = stream.readQString()
            date = QDate()
            if action in ("BOOK", "UNBOOK"):
                room = stream.readQString()
                stream >> date
                try:
                    Thread.lock.lockForRead()       #锁定_为_读
                    bookings = Bookings.get(date.toPyDate())    #在多线程中Bookings为共享字典变量为防冲突读取前先加 读锁定.
                finally:
                    Thread.lock.unlock()
                uroom = room
            if action == "BOOK":
                newlist = False
                try:
                    Thread.lock.lockForRead()       #锁定_为_读
                    if bookings is None:
                        newlist = True
                finally:
                    Thread.lock.unlock()
                if newlist:
                    try:
                        Thread.lock.lockForWrite()  #锁定_为_写
                        bookings = Bookings[date.toPyDate()]
                    finally:
                        Thread.lock.unlock()
                error = None
                insert = False      #insert::插入
                try:
                    Thread.lock.lockForRead()
                    if len(bookings) < MAX_BOOKINGS_PER_DAY:
                        if uroom in bookings:
                            error = "Cannot accept duplicate booking"
                        else:
                            insert = True
                    else:
                        error = "{} is fully booked".format(
                                date.toString(Qt.ISODate))
                finally:
                    Thread.lock.unlock()
                if insert:
                    try:
                        Thread.lock.lockForWrite()
                        bisect.insort(bookings, uroom)
                    finally:
                        Thread.lock.unlock()
                    self.sendReply(socket, action, room, date)
                else:
                    self.sendError(socket, error)
            elif action == "UNBOOK":
                error = None
                remove = False
                try:
                    Thread.lock.lockForRead()
                    if bookings is None or uroom not in bookings:
                        error = "Cannot unbook nonexistent booking"     #不能取消不存在的预订
                    else:
                        remove = True
                finally:
                    Thread.lock.unlock()
                if remove:
                    try:
                        Thread.lock.lockForWrite()
                        bookings.remove(uroom)
                    finally:
                        Thread.lock.unlock()
                    self.sendReply(socket, action, room, date)
                else:
                    self.sendError(socket, error)
            else:
                self.sendError(socket, "Unrecognized request")
            socket.waitForDisconnected()    #waitForDisconnected::等候_断开:执行后触发finished信号(row173)所有的读写锁会解除.
            try:
                Thread.lock.lockForRead()
                printBookings()
            finally:
                Thread.lock.unlock()


    def sendError(self, socket, msg):
        reply = QByteArray()    #reply::答复
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString("ERROR")
        stream.writeQString(msg)
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        socket.write(reply)


    def sendReply(self, socket, action, room, date):
        reply = QByteArray()    #reply::答复
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString(action)
        stream.writeQString(room)
        stream << date
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        socket.write(reply)


class TcpServer(QTcpServer):

    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)


    def incomingConnection(self, socketId): #incomingConnection::进入_连接
        thread = Thread(socketId, self)
        self.connect(thread, SIGNAL("finished()"),      #finished::完成 -->Thread.run方法完成发射此信号
                     thread, SLOT("deleteLater()"))     #deleteLater::册除_后
        thread.start()
        

class BuildingServicesDlg(QPushButton):     #构建_服务_窗口

    def __init__(self, parent=None):
        super(BuildingServicesDlg, self).__init__(
                "&Close Server", parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)    #WindowStaysOnTopHint::窗口_停留_到_顶部_提示[窗口顶置提示]

        self.loadBookings()
        self.tcpServer = TcpServer(self)
        if not self.tcpServer.listen(QHostAddress("0.0.0.0"), PORT):    #listen::监听
            QMessageBox.critical(self, "Building Services Server",      #critical::危险[危险窗口]
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
                floor = random.randint(0, 5)    #floor::层
                room = random.randint(1, 34)    #room::房号
                bookings = Bookings[date.toPyDate()]
                if len(bookings) >= MAX_BOOKINGS_PER_DAY:
                    continue
                bisect.insort(bookings, "{0:1d}{1:02d}".format(     #{0:1d}::一位整数, {1:02d}::两位整数前面不足位数用0填充.
                              floor, room))
        printBookings()


app = QApplication(sys.argv)
form = BuildingServicesDlg()
form.show()
form.move(0, 0)
app.exec_()

