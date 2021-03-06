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


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # 列表
        listWidget = QListWidget()
        listWidget.setAcceptDrops(True)  # 接受Drops
        listWidget.setDragEnabled(True)  # 拖曳允许
        path = os.path.dirname(__file__)
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png"):
                item = QListWidgetItem(image.split(".")[0].capitalize())
                item.setIcon(QIcon(os.path.join(path,
                                   "images/{}".format(image))))
                listWidget.addItem(item)
        # 图标列表
        iconListWidget = QListWidget()
        iconListWidget.setAcceptDrops(True)
        iconListWidget.setDragEnabled(True)
        iconListWidget.setViewMode(QListWidget.IconMode)    #setViewMode：设置视图模式
        # 创建表格
        tableWidget = QTableWidget()
        tableWidget.setRowCount(5)  # 行
        tableWidget.setColumnCount(2)  # 列
        tableWidget.setHorizontalHeaderLabels(["Column #1", "Column #2"])   #水平信头标签
        tableWidget.setAcceptDrops(True)
        tableWidget.setDragEnabled(True)

        splitter = QSplitter(Qt.Horizontal)  # 创建水平分裂器
        splitter.addWidget(listWidget)
        splitter.addWidget(iconListWidget)
        splitter.addWidget(tableWidget)
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.setWindowTitle("Drag and Drop")


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

