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

LEFT, ABOVE = range(2)  # 分别赋值 LEFT=0 (左), ABOVE=1 (上方)

# 带标签头的行编辑框
class LabelledLineEdit(QWidget):

    def __init__(self, labelText="", position=LEFT,
                 parent=None):
        super(LabelledLineEdit, self).__init__(parent)
        self.label = QLabel(labelText)
        self.lineEdit = QLineEdit()
        self.label.setBuddy(self.lineEdit)
        # todo::https://blog.csdn.net/heaven_evil/article/details/78307261
        layout = QBoxLayout(QBoxLayout.LeftToRight
                if position == LEFT else QBoxLayout.TopToBottom)  # 创建布局(QBoxLayout):如果==LEFT,从左至右排列,否则从上至下排列.
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

# 带标签头的文本编辑框
class LabelledTextEdit(QWidget):

    def __init__(self, labelText="", position=LEFT,
                 parent=None):
        super(LabelledTextEdit, self).__init__(parent)
        self.label = QLabel(labelText)
        self.textEdit = QTextEdit()
        self.label.setBuddy(self.textEdit)
        layout = QBoxLayout(QBoxLayout.LeftToRight
                if position == LEFT else QBoxLayout.TopToBottom)
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)


class Dialog(QDialog):

    def __init__(self, address=None, parent=None):
        super(Dialog, self).__init__(parent)
        # 街道
        self.street = LabelledLineEdit("&Street:")
        # 城市
        self.city = LabelledLineEdit("&City:")
        # 国家
        self.state = LabelledLineEdit("St&ate:")
        # 邮编
        self.zipcode = LabelledLineEdit("&Zipcode:")
        # 备注
        self.notes = LabelledTextEdit("&Notes:", ABOVE)  # ABOVE:在上方 ,定义标签在上方.
        if address is not None:  # address:字典类型

            self.street.lineEdit.setText(address.get("street", ""))
            self.city.lineEdit.setText(address.get("city", ""))
            self.state.lineEdit.setText(address.get("state", ""))
            self.zipcode.lineEdit.setText(address.get("zipcode", ""))
            self.notes.textEdit.setPlainText(address.get("notes", ""))  # PlainText::纯文本.
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                     QDialogButtonBox.Cancel)

        grid = QGridLayout()    # 栅格布局
        grid.addWidget(self.street, 0, 0)
        grid.addWidget(self.city, 0, 1)
        grid.addWidget(self.state, 1, 0)
        grid.addWidget(self.zipcode, 1, 1)
        grid.addWidget(self.notes, 2, 0, 1, 2)
        layout = QVBoxLayout()  # 垂直布局
        layout.addLayout(grid)  # addLayout:加入布局
        layout.addWidget(buttonBox)  # addWidget:加入饰件
        self.setLayout(layout)
        
        self.connect(buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, SIGNAL("rejected()"), self.reject)

        self.setWindowTitle("Labelled Widgets")


if __name__ == "__main__":
    fakeAddress = dict(street="3200 Mount Vernon Memorial Highway",
                       city="Mount Vernon", state="Virginia",
                       zipcode="22121")
    app = QApplication(sys.argv)
    form = Dialog(fakeAddress)
    form.show()
    app.exec_()
    print("Street:", form.street.lineEdit.text())
    print("City:", form.city.lineEdit.text())
    print("State:", form.state.lineEdit.text())
    print("Notes:")
    print(form.notes.textEdit.toPlainText())

