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

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *   #包含QTcpSocket(),QUdpSocket()等网络模块.

MAC = "qt_mac_set_native_menubar" in dir()

PORT = 9407     #端口号
SIZEOF_UINT16 = 2   #2表示两字节


class BuildingServicesClient(QWidget):  #构建_服务_客户端

    def __init__(self, parent=None):
        super(BuildingServicesClient, self).__init__(parent)

        self.socket = QTcpSocket()  #TcpSocket::Tcp套接字
        self.nextBlockSize = 0  #下一_块_尺寸
        self.request = None #请求

        roomLabel = QLabel("&Room")
        self.roomEdit = QLineEdit()
        roomLabel.setBuddy(self.roomEdit)
        regex = QRegExp(r"[0-9](?:0[1-9]|[12][0-9]|3[0-4])")
        self.roomEdit.setValidator(QRegExpValidator(regex, self))   #setValidator::设置_验证器
        self.roomEdit.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        dateLabel = QLabel("&Date")
        self.dateEdit = QDateEdit() #创建日期编缉控件.
        dateLabel.setBuddy(self.dateEdit)
        self.dateEdit.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.dateEdit.setDate(QDate.currentDate().addDays(1))   #设置日期是当前日期+1天.
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")    #setDisplayFormat::设置_显示_格式

        responseLabel = QLabel("Response")  #Response::响应
        self.responseLabel = QLabel()
        self.responseLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)  #setFrameStyle::设置_框架_样式, StyledPanel::可变面板, Sunken::凹陷

        self.bookButton = QPushButton("&Book")  #Book::预订[这里解'预订',别一解是 '书']
        self.bookButton.setEnabled(False)
        self.unBookButton = QPushButton("&Unbook")  #Unbook::取消预订
        self.unBookButton.setEnabled(False)
        quitButton = QPushButton("&Quit")
        if not MAC:
            self.bookButton.setFocusPolicy(Qt.NoFocus)
            self.unBookButton.setFocusPolicy(Qt.NoFocus)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.bookButton)
        buttonLayout.addWidget(self.unBookButton)
        buttonLayout.addStretch()   #addStretch::加入_拉伸 控件
        buttonLayout.addWidget(quitButton)
        layout = QGridLayout()
        layout.addWidget(roomLabel, 0, 0)
        layout.addWidget(self.roomEdit, 0, 1)
        layout.addWidget(dateLabel, 0, 2)
        layout.addWidget(self.dateEdit, 0, 3)
        layout.addWidget(responseLabel, 1, 0)
        layout.addWidget(self.responseLabel, 1, 1, 1, 3)
        layout.addLayout(buttonLayout, 2, 1, 1, 4)
        self.setLayout(layout)

        self.connect(self.socket, SIGNAL("connected()"), self.sendRequest)  #connected::连接
        self.connect(self.socket, SIGNAL("readyRead()"), self.readResponse) #readyRead::准备_读
        self.connect(self.socket, SIGNAL("disconnected()"),     #disconnected::断开
                     self.serverHasStopped) #serverHasStopped::服务_在_停止
        self.connect(self.socket,
                     SIGNAL("error(QAbstractSocket::SocketError)"),
                     self.serverHasError)   #serverHasError::服务_在_错误
        self.connect(self.roomEdit, SIGNAL("textEdited(QString)"),  #textEdited::文本_编缉时
                     self.updateUi)
        self.connect(self.dateEdit, SIGNAL("dateChanged(QDate)"),   #dateChanged::时间_改变时
                     self.updateUi)
        self.connect(self.bookButton, SIGNAL("clicked()"), self.book)
        self.connect(self.unBookButton, SIGNAL("clicked()"), self.unBook)
        self.connect(quitButton, SIGNAL("clicked()"), self.close)

        self.setWindowTitle("Building Services")


    def updateUi(self): #更新Ui
        enabled = False #enabled::启用(ed::时)
        if (self.roomEdit.text() and
            self.dateEdit.date() > QDate.currentDate()):
            enabled = True
        if self.request is not None:    #request::请求
            enabled = False
        self.bookButton.setEnabled(enabled)
        self.unBookButton.setEnabled(enabled)


    def closeEvent(self, event):
        self.socket.close() #套接字.关闭
        event.accept()


    def book(self):
        self.issueRequest("BOOK", self.roomEdit.text(), #issueRequest::发出_请求
                          self.dateEdit.date())


    def unBook(self):
        self.issueRequest("UNBOOK", self.roomEdit.text(),
                          self.dateEdit.date())


    def issueRequest(self, action, room, date): #issueRequest::发出_请求, action::动作, room::房号, date::日期
        self.request = QByteArray() #request::请求, QByteArray()::字节_数组[PS:保存在内存的数据格式,能像其他IODevice一样进行读写操作]
        stream = QDataStream(self.request, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt16(0)   #P397② 写入'两字节无符号整数'.
        stream.writeQString(action) #写入 动作
        stream.writeQString(room)   #写入 房号
        stream << date      #加入 日期
        stream.device().seek(0) #P398③
        stream.writeUInt16(self.request.size() - SIZEOF_UINT16) #size()::返回值以字节为单位.P398④
        self.updateUi()
        if self.socket.isOpen():    #isOpen()::套接字是否打开.P398⑤
            self.socket.close()
        self.responseLabel.setText("Connecting to server...")
        self.socket.connectToHost("localhost", PORT)    #执行connectToHost::连接_到_主机/宿主
                                                        #触发socket::connected信号ROW:74↑,执行sendRequest()方法↓


    def sendRequest(self):      #当该方法完成时会执行serverHasStopped()/serverHasError()
        self.responseLabel.setText("Sending request...")
        self.nextBlockSize = 0
        self.socket.write(self.request) #向 套接字 写入 请求.
        self.request = None
        

    def readResponse(self):
        stream = QDataStream(self.socket)
        stream.setVersion(QDataStream.Qt_4_2)

        while True:
            if self.nextBlockSize == 0:
                if self.socket.bytesAvailable() < SIZEOF_UINT16:    #bytesAvailable::可用_字节
                    break
                self.nextBlockSize = stream.readUInt16()
            if self.socket.bytesAvailable() < self.nextBlockSize:
                break
            action = stream.readQString()
            room = stream.readQString()
            date = QDate()
            if action != "ERROR":
                stream >> date
            if action == "ERROR":
                msg = "Error: {}".format(room)
            elif action == "BOOK":
                msg = "Booked room {} for {}".format(room,
                        date.toString(Qt.ISODate))
            elif action == "UNBOOK":
                msg = "Unbooked room {} for {}".format(room,
                        date.toString(Qt.ISODate))
            self.responseLabel.setText(msg)
            self.updateUi()
            self.nextBlockSize = 0


    def serverHasStopped(self):
        self.responseLabel.setText(
                "Error: Connection closed by server")
        self.socket.close()


    def serverHasError(self, error):
        self.responseLabel.setText("Error: {}".format(
                self.socket.errorString()))
        self.socket.close()


app = QApplication(sys.argv)
form = BuildingServicesClient()
form.show()
app.exec_()

