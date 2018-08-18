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

import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DropLineEdit(QLineEdit):
    
    def __init__(self, parent=None):
        super(DropLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)  # 接受Drops(下降)

    # 拖拽进入事件(当拖拽进入到控件范围时发生。)
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    # 拖拽移动事件(在控件上拖拽移动时发生。)
    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.CopyAction)  # 设置 下降动作：复制
            event.accept()
        else:
            event.ignore()

    # 下降事件(拖动操作在控件上释放时发生。)
    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = stream.readQString()
            self.setText(text)
            event.setDropAction(Qt.CopyAction)  # 设置 下降动作：复制
            event.accept()
        else:
            event.ignore()


class DnDMenuListWidget(QListWidget):  # 弹出菜单选择拖放类型

    def __init__(self, parent=None):
        super(DnDMenuListWidget, self).__init__(parent)
        self.setAcceptDrops(True)   # 接受下降。
        self.setDragEnabled(True)   # 拖曳充许。
        self.dropAction = Qt.CopyAction
        
    # 拖曳进入件事(当拖拽进入到控件范围时发生。)
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    # 拖曳移动事件(在控件上拖拽移动时发生。)
    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.MoveAction)  # 设置 下降动作：移动
            event.accept()
        else:
            event.ignore()

    # 下降事件(拖动操作在控件上释放时发生。)
    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = stream.readQString()
            icon = QIcon()
            stream >> icon
            menu = QMenu(self)
            menu.addAction("&Copy", self.setCopyAction)
            menu.addAction("&Move", self.setMoveAction)
            if menu.exec_(QCursor.pos()):
                item = QListWidgetItem(text, self)
                item.setIcon(icon)
                event.setDropAction(self.dropAction)
                event.accept()
                return
            else:
                event.setDropAction(Qt.IgnoreAction)
        event.ignore()


    def setCopyAction(self):
        self.dropAction = Qt.CopyAction
        

    def setMoveAction(self):
        self.dropAction = Qt.MoveAction
        
    # 开始拖曳(有元素被拖曳时执行此事件。)
    def startDrag(self, dropActions):  # dropActions::下降动作
        item = self.currentItem()
        icon = item.icon()
        data = QByteArray()  # 字节数组(即保存二进制数据格式.)
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(item.text())
        stream << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)  # 设置自定义格式数据??
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))  # 设置热点（设置为drag的中点）
        drag.setPixmap(pixmap)
        if (drag.start(Qt.MoveAction|Qt.CopyAction) == Qt.MoveAction):  # 从QT4.3开如应当使用drag.exec_()而不是drag.start().
            self.takeItem(self.row(item))   # takeItem():拿走项


class DnDCtrlListWidget(QListWidget):  # 按Ctrl改变拖放类型

    def __init__(self, parent=None):
        super(DnDCtrlListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            action = Qt.MoveAction
            if event.keyboardModifiers() & Qt.ControlModifier:
                action = Qt.CopyAction
            event.setDropAction(action)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = stream.readQString()
            icon = QIcon()
            stream >> icon
            item = QListWidgetItem(text, self)
            item.setIcon(icon)
            action = Qt.MoveAction
            if event.keyboardModifiers() & Qt.ControlModifier:
                action = Qt.CopyAction
            event.setDropAction(action)  # 设置 下降动作：移动
            event.accept()
        else:
            event.ignore()


    def startDrag(self, dropActions):
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
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        if (drag.start(Qt.MoveAction|Qt.CopyAction) == Qt.MoveAction):
            self.takeItem(self.row(item))


class DnDWidget(QWidget):
    
    def __init__(self, text, icon=QIcon(), parent=None):
        super(DnDWidget, self).__init__(parent)
        self.setAcceptDrops(True)   # 设置 接受下降=True
        self.text = text
        self.icon = icon

    # 最小尺寸提示(控件的最小Size)
    def minimumSizeHint(self):
        fm = QFontMetricsF(self.font())  # FontMetrics:字体度量
        if self.icon.isNull():
            return QSize(fm.width(self.text), fm.height() * 1.5)
        return QSize(34 + fm.width(self.text), max(34, fm.height() * 1.5))


    def paintEvent(self, event):
        height = QFontMetricsF(self.font()).height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)    # setRenderHint:设置渲染指示,Antialiasing:反锯齿
        painter.setRenderHint(QPainter.TextAntialiasing)    # setRenderHint:设置渲染指示,TextAntialiasing:文字反锯齿
        painter.fillRect(self.rect(), QColor(Qt.yellow).light())  # fillRect::填充矩形.
        if self.icon.isNull():
            painter.drawText(10, height, self.text)
        else:
            pixmap = self.icon.pixmap(24, 24)
            painter.drawPixmap(0, 5, pixmap)
            painter.drawText(34, height,
                             self.text + " (Drag to or from me!)")

    # 拖拽进入事件(当拖拽进入到控件范围时发生。)
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    # 拖拽移动事件(在控件上拖拽移动时发生。)
    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    # 下降事件(拖动操作在控件上释放时发生。)
    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = stream.readQString()
            self.icon = QIcon()
            stream >> self.icon
            event.setDropAction(Qt.CopyAction)
            event.accept()
            self.updateGeometry()  # 更新几何(图形)
            self.update()  # 更新(触发执行paintEvent())
        else:
            event.ignore()

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        self.startDrag()
        QWidget.mouseMoveEvent(self, event)

    # 开始拖拽(有元素被拖动时执行此时件。)
    def startDrag(self):
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


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # 支持拖拽的列表窗口.
        dndListWidget = DnDMenuListWidget()
        path = os.path.dirname(__file__)
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png"):
                item = QListWidgetItem(image.split(".")[0].capitalize())
                item.setIcon(QIcon(os.path.join(path,
                                   "images/{}".format(image))))
                dndListWidget.addItem(item)
        # 支持拖拽的图标列表窗口.
        dndIconListWidget = DnDCtrlListWidget()
        dndIconListWidget.setViewMode(QListWidget.IconMode)
        # 支持拖拽的Widget控件.
        dndWidget = DnDWidget("Drag to me!")
        # 支持拖拽的LineEdit控件.
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

