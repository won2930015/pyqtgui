#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DropLineEdit(QLineEdit):
    
    def __init__(self, parent=None):
        super(DropLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)   #接受放下


    def dragEnterEvent(self, event): #当拖拽进入到控件范围时发生。
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event): #在控件上拖拽移动时发生。
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.CopyAction) #拖拽动作：复制
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event): ##在控件上拖动时发生。
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = stream.readQString()
            self.setText(text)
            event.setDropAction(Qt.CopyAction) #拖拽动作：复制
            event.accept()
        else:
            event.ignore()


class DnDListWidget(QListWidget):

    def __init__(self, parent=None):
        super(DnDListWidget, self).__init__(parent)
        self.setAcceptDrops(True)   #接受放下。
        self.setDragEnabled(True)   #接受拖动。
        

    def dragEnterEvent(self, event):    #当拖拽进入到控件范围时发生。
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event): #在控件上拖拽移动时发生。
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.MoveAction)  #拖拽动作：移动
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):  #在控件上发生拖动时
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = stream.readQString()
            icon = QIcon()
            stream >> icon
            item = QListWidgetItem(text, self)
            item.setIcon(icon)
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()


    def startDrag(self, dropActions):   #有元素被拖动时执行此时件。
        item = self.currentItem()
        icon = item.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(item.text())
        stream << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12)) #设置热点（设置为drag的中点）
        drag.setPixmap(pixmap)
        if drag.start(Qt.MoveAction) == Qt.MoveAction: #从QT4.3开如应当使用drag.exec_()而不是drag.start().
            self.takeItem(self.row(item))   #takeItem():拿走项


class DnDWidget(QWidget):
    
    def __init__(self, text, icon=QIcon(), parent=None):
        super(DnDWidget, self).__init__(parent)
        self.setAcceptDrops(True)   #同意拖拽=True
        self.text = text
        self.icon = icon


    def minimumSizeHint(self):
        fm = QFontMetricsF(self.font()) #FontMetrics:字体度量
        if self.icon.isNull():
            return QSize(fm.width(self.text), fm.height() * 1.5)
        return QSize(34 + fm.width(self.text), max(34, fm.height() * 1.5))


    def paintEvent(self, event):
        height = QFontMetricsF(self.font()).height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)    #setRenderHint:设置渲染提示,Antialiasing:反锯齿
        painter.setRenderHint(QPainter.TextAntialiasing)    #setRenderHint:设置渲染提示,TextAntialiasing:文字反锯齿
        painter.fillRect(self.rect(), QColor(Qt.yellow).light())
        if self.icon.isNull():
            painter.drawText(10, height, self.text)
        else:
            pixmap = self.icon.pixmap(24, 24)
            painter.drawPixmap(0, 5, pixmap)
            painter.drawText(34, height,
                             self.text + " (Drag to or from me!)")


    def dragEnterEvent(self, event):    #当拖拽进入到控件范围时发生。
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event): #在控件上拖拽移动时发生。
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event): #在控件上拖动时发生。
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = stream.readQString()
            self.icon = QIcon()
            stream >> self.icon
            event.setDropAction(Qt.CopyAction)
            event.accept()
            self.updateGeometry()
            self.update()
        else:
            event.ignore()


    def mouseMoveEvent(self, event):
        self.startDrag()
        QWidget.mouseMoveEvent(self, event)


    def startDrag(self):    #有元素被拖动时执行此时件。
        icon = self.icon
        if icon.isNull():
            return
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(self.text)
        stream << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        drag.start(Qt.CopyAction)
        # drag.start(Qt.MoveAction)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        dndListWidget = DnDListWidget()
        path = os.path.dirname(__file__)
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png"):
                item = QListWidgetItem(image.split(".")[0].capitalize())
                item.setIcon(QIcon(os.path.join(path,
                                   "images/{}".format(image))))
                dndListWidget.addItem(item)
        dndIconListWidget = DnDListWidget()
        dndIconListWidget.setViewMode(QListWidget.IconMode)
        dndWidget = DnDWidget("Drag to me!")
        dropLineEdit = DropLineEdit()

        layout = QGridLayout()
        layout.addWidget(dndListWidget, 0, 0)
        layout.addWidget(dndIconListWidget, 0, 1)
        layout.addWidget(dndWidget, 1, 0)
        layout.addWidget(dropLineEdit, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle("Custom Drag and Drop")


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

