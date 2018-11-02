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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qrc_resources


class HelpForm(QDialog):

    def __init__(self, page, parent=None):
        super(HelpForm, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)  # setAttribute::设置_属性
        # 如果widget设置了Qt.WA_DeleteOnClose属性，widget将会被释放。
        # 不管widget是否可见，关闭事件都会传递给widget。即接收到QCloseEvent事件后，
        # 除了调用hide()方法将窗口隐藏，同时会调用deleteLater()方法将窗口释放掉，不会再占用资源。
        self.setAttribute(Qt.WA_GroupLeader)    # P386

        backAction = QAction(QIcon(":/back.png"), self.tr("&Back"), self)
        backAction.setShortcut(QKeySequence.Back)   # setShortcut::设置_快捷键
        homeAction = QAction(QIcon(":/home.png"), self.tr("&Home"), self)
        homeAction.setShortcut(self.tr("Home"))
        self.pageLabel = QLabel()

        toolBar = QToolBar()
        toolBar.addAction(backAction)
        toolBar.addAction(homeAction)
        toolBar.addWidget(self.pageLabel)
        self.textBrowser = QTextBrowser()

        layout = QVBoxLayout()
        layout.addWidget(toolBar)
        layout.addWidget(self.textBrowser, 1)   # 第二参数::stretch:伸展(表示控件的伸展方式.)
        self.setLayout(layout)

        self.connect(backAction, SIGNAL("triggered()"),
                     self.textBrowser, SLOT("backward()"))  # backward--QTextBrowser的内置方法???
        self.connect(homeAction, SIGNAL("triggered()"),
                     self.textBrowser, SLOT("home()"))
        self.connect(self.textBrowser, SIGNAL("sourceChanged(QUrl)"),
                     self.updatePageTitle)

        self.textBrowser.setSearchPaths([":/"])  # setSearchPaths::设置_搜索_路径.p386
        self.textBrowser.setSource(QUrl(page))  # setSource::设置_源
        self.resize(400, 600)
        self.setWindowTitle(self.tr("{} Help").format(QApplication.applicationName()))


    def updatePageTitle(self):
        self.pageLabel.setText(self.textBrowser.documentTitle())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = HelpForm("index.html")
    form.show()
    app.exec_()

