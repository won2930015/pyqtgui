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
import treeoftable


class ServerModel(treeoftable.TreeOfTableModel):

    def __init__(self, parent=None):
        super(ServerModel, self).__init__(parent)


    def data(self, index, role):
        if role == Qt.DecorationRole:  # DecorationRole::修饰角色(图标)
            node = self.nodeFromIndex(index)
            if node is None:
                return None
            if isinstance(node, treeoftable.BranchNode):
                if index.column() != 0:
                    return None
                filename = node.toString().replace(" ", "_")
                parent = node.parent.toString()
                if parent and parent != "USA":
                    return None
                if parent == "USA":
                    filename = "USA_" + filename
                filename = os.path.join(os.path.dirname(__file__),  #"...\chap16\flags\" +filename +".png"
                                        "flags", filename + ".png")
                pixmap = QPixmap(filename)
                if pixmap.isNull():
                    return None
                return pixmap
        return treeoftable.TreeOfTableModel.data(self, index, role)


class TreeOfTableWidget(QTreeView):

    def __init__(self, filename, nesting, separator, parent=None):  # nesting::嵌套, separator:分隔符
        super(TreeOfTableWidget, self).__init__(parent)
        self.setSelectionBehavior(QTreeView.SelectItems)    # setSelectionBehavior::设置_选择_行为, SelectItems::选择_项
        self.setUniformRowHeights(True)  # setUniformRowHeights::设置_统一_行_高度
        model = ServerModel(self)   # 服务器_模型 ↑row_19
        self.setModel(model)
        try:
            model.load(filename, nesting, separator)
        except IOError as e:
            QMessageBox.warning(self, "Server Info - Error", e)
        self.connect(self, SIGNAL("activated(QModelIndex)"),    # ???activated::激活(双击项时) P375
                     self.activated)
        self.connect(self, SIGNAL("expanded(QModelIndex)"),     # ???expanded::扩展(节点被展开时) P375
                     self.expanded)
        self.expanded()


    def currentFields(self):
        return self.model().asRecord(self.currentIndex())   # 返回 root 到 叶节点的所有路径.


    def activated(self, index):
        self.emit(SIGNAL("activated"), self.model().asRecord(index))


    def expanded(self):
        for column in range(self.model().columnCount(
                            QModelIndex())):
            self.resizeColumnToContents(column)


class MainForm(QMainWindow):

    def __init__(self, filename, nesting, separator, parent=None):
        super(MainForm, self).__init__(parent)
        headers = ["Country/State (US)/City/Provider", "Server", "IP"]
        if nesting != 3:
            if nesting == 1:
                headers = ["Country/State (US)", "City", "Provider",
                           "Server"]
            elif nesting == 2:
                headers = ["Country/State (US)/City", "Provider",
                           "Server"]
            elif nesting == 4:
                headers = ["Country/State (US)/City/Provider/Server"]
            headers.append("IP")

        self.treeWidget = TreeOfTableWidget(filename, nesting,
                                            separator)
        self.treeWidget.model().headers = headers
        self.setCentralWidget(self.treeWidget)  # setCentralWidget::设置_中心_控件

        QShortcut(QKeySequence("Escape"), self, self.close)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)

        self.connect(self.treeWidget, SIGNAL("activated"),
                     self.activated)

        self.setWindowTitle("Server Info")
        self.statusBar().showMessage("Ready...", 5000)


    def picked(self):   # 摘要
        return self.treeWidget.currentFields()  # currentFields::当前_域|字段


    def activated(self, fields):
        self.statusBar().showMessage("*".join(fields), 60000)


app = QApplication(sys.argv)
nesting = 3
if len(sys.argv) > 1:
    try:
        nesting = int(sys.argv[1])
    except:
        pass
    if nesting not in (1, 2, 3, 4):
        nesting = 3

form = MainForm(os.path.join(os.path.dirname(__file__), "servers.txt"), nesting, "*")
form.resize(750, 550)
form.show()
app.exec_()
print("*".join(form.picked()))

