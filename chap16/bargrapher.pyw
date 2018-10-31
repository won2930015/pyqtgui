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

import random
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


# List模型示列?
class BarGraphModel(QAbstractListModel):

    def __init__(self):
        super(BarGraphModel, self).__init__()
        self.__data = []
        self.__colors = {}
        self.minValue = 0
        self.maxValue = 0

    def rowCount(self, index=QModelIndex()):
        return len(self.__data)

    def insertRows(self, row, count):
        extra = row + count  # extra::额外(扩展)
        if extra >= len(self.__data):
            self.beginInsertRows(QModelIndex(), row, row + count - 1)
            self.__data.extend([0] * (extra - len(self.__data) + 1))
            self.endInsertRows()
            return True
        return False

    def flags(self, index):
        return (QAbstractTableModel.flags(self, index)
                | Qt.ItemIsEditable)   # ItemIsEditable::项_是_可编辑的

    def setData(self, index, value, role=Qt.DisplayRole):
        row = index.row()
        if not index.isValid() or 0 > row >= len(self.__data):
            return False
        changed = False  # changed::改变
        if role == Qt.DisplayRole:  # DisplayRole::显示_角色
            value = int(value)
            self.__data[row] = value
            if self.minValue > value:
                self.minValue = value
            if self.maxValue < value:
                self.maxValue = value
            changed = True
        elif role == Qt.UserRole:   # UserRole::用户_角色.与颜色相关???
            self.__colors[row] = value
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            changed = True
        if changed:
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
        return changed

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if not index.isValid() or 0 > row >= len(self.__data):
            return None
        if role == Qt.DisplayRole:
            return self.__data[row]
        if role == Qt.UserRole:
            return self.__colors.get(row, QColor(Qt.red))   # 当row没有设定颜色时,返回 red(红)色.
        if role == Qt.DecorationRole:   # 修饰_角色(图标).
            color = QColor(self.__colors.get(row, QColor(Qt.red)))
            pixmap = QPixmap(20, 20)
            pixmap.fill(color)
            return pixmap
        return None


class BarGraphDelegate(QStyledItemDelegate):

    def __init__(self, minimum=0, maximum=100, parent=None):
        super(BarGraphDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum

    def paint(self, painter, option, index):
        myoption = QStyleOptionViewItem(option)  # StyleOptionViewItem::样式_选项_视图_项
        myoption.displayAlignment |= (Qt.AlignRight|Qt.AlignVCenter)
        QStyledItemDelegate.paint(self, painter, myoption, index)

    def createEditor(self, parent, option, index):
        spinbox = QSpinBox(parent)
        spinbox.setRange(self.minimum, self.maximum)
        spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        return spinbox

    def setEditorData(self, editor, index):
        value = int(index.model().data(index, Qt.DisplayRole))
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        editor.interpretText()  # interpretText::解析_文本.(将文体值解释为合适的值,这里为int)
        model.setData(index, editor.value())


class BarGraphView(QWidget):

    WIDTH = 20

    def __init__(self, parent=None):
        super(BarGraphView, self).__init__(parent)
        self.model = None


    def setModel(self, model):
        self.model = model
        self.connect(self.model,
                SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.update)
        self.connect(self.model, SIGNAL("modelReset()"), self.update)   # modelReset::模型_重置


    def sizeHint(self):
        return self.minimumSizeHint()


    def minimumSizeHint(self):
        if self.model is None:
            return QSize(BarGraphView.WIDTH * 10, 100)
        return QSize(BarGraphView.WIDTH * self.model.rowCount(), 100)


    def paintEvent(self, event):
        if self.model is None:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)    # setRenderHint::设置_渲染_提示, Antialiasing::反锯齿
        span = self.model.maxValue - self.model.minValue
        painter.setWindow(0, 0, BarGraphView.WIDTH * self.model.rowCount(), span)   # 设置_window size.
        for row in range(self.model.rowCount()):
            x = row * BarGraphView.WIDTH
            index = self.model.index(row)
            color = QColor(self.model.data(index, Qt.UserRole))
            y = int(self.model.data(index))
            painter.fillRect(x, span - y, BarGraphView.WIDTH, y, color)


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = BarGraphModel()
        self.barGraphView = BarGraphView()
        self.barGraphView.setModel(self.model)
        self.listView = QListView()
        self.listView.setModel(self.model)
        self.listView.setItemDelegate(BarGraphDelegate(0, 1000, self))
        self.listView.setMaximumWidth(100)
        self.listView.setEditTriggers(QListView.DoubleClicked|   # setEditTriggers::设置_编辑_触发
                                      QListView.EditKeyPressed)  # EditKeyPressed::编辑_键_按下
        layout = QHBoxLayout()
        layout.addWidget(self.listView)
        layout.addWidget(self.barGraphView, 1)
        self.setLayout(layout)

        self.setWindowTitle("Bar Grapher")
        QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        # Generate fake data::生成_伪_数据
        count = 20
        self.model.insertRows(0, count - 1)
        for row in range(count):
            value = random.randint(1, 150)
            color = QColor(random.randint(0, 255), random.randint(0, 255),
                           random.randint(0, 255))
            index = self.model.index(row)
            self.model.setData(index, value)
            self.model.setData(index, color, Qt.UserRole)


app = QApplication(sys.argv)
form = MainForm()
form.resize(600, 400)
form.show()
app.exec_()

