#!/usr/bin/env python3
# Copyright (c) 2017 Marvin Studio. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ContactDlg(QDialog):

    StyleSheet = """
QComboBox { color: darkblue; }
QLineEdit { color: darkgreen; }
"""
    StyleSheet2 = """
QComboBox { color: darkblue; }
QLineEdit { color: black; }
QLineEdit[mandatory="true"]{
    background-color:rgb(111,233,123);
    color:black;
    }
QLineEdit[mandatory_edu="true"]{
    background-color:rgb(221,233,123);
    color:black;
    }

.QLineEdit{
    color:green;
}
QLineEdit{
    color:black;
}
QLineEdit#obj_mobileEdit{
    color:red;
}
QComboBox::drop-down{
    color:red;
}
QCheckBox:checked{
    color:yellow;
}
"""
# 对于样式表来说，如果有父样式和子样式，如果子样式被父样式覆盖，则子样式中那些在父样式中不存在的也会被重写。
#.QLineEdit 和 QLineEdit 前者针对特定的类而不包括子类，后者包括类和子类，如果均设置，且设置项冲突，则以更精准的为准，也就是.QLineEdit，在这个例子中为绿色而不是黑色
# QLineEdit#OBJNAME 为更精细的类，因此不论其写在CSS的哪一行，均不会被覆盖，其颜色均为红色。
# 对于伪状态，可以使用：表示，对于子组件，可以使用：：表示。但是上面两个好像并不好用
    def __init__(self, parent=None):
        super(ContactDlg, self).__init__(parent)

        forenameLabel = QLabel("姓名(&N)")
        self.forenameEdit = QLineEdit()
        forenameLabel.setBuddy(self.forenameEdit)
        surnameLabel = QLabel("曾用名(&U)")
        self.surnameEdit = QLineEdit()
        surnameLabel.setBuddy(self.surnameEdit)
        categoryLabel = QLabel("行业(&V)")
        self.categoryComboBox = QComboBox()
        categoryLabel.setBuddy(self.categoryComboBox)
        self.categoryComboBox.addItems(["商业", "教育",
                                        "其他"])
        companyLabel = QLabel("公司(&C)")
        self.companyEdit = QLineEdit()
        companyLabel.setBuddy(self.companyEdit)
        addressLabel = QLabel("地址(&A)")
        self.addressEdit = QLineEdit()
        addressLabel.setBuddy(self.addressEdit)
        phoneLabel = QLabel("固定电话(&P)")
        self.phoneEdit = QLineEdit()
        phoneLabel.setBuddy(self.phoneEdit)
        mobileLabel = QLabel("移动电话(&M)")
        self.mobileEdit = QLineEdit()
        self.mobileEdit.setObjectName('obj_mobileEdit')
        mobileLabel.setBuddy(self.mobileEdit)
        faxLabel = QLabel("传真(&F)")
        self.faxEdit = QLineEdit()
        faxLabel.setBuddy(self.faxEdit)
        emailLabel = QLabel("电子邮件(&E)")
        self.emailEdit = QLineEdit()
        emailLabel.setBuddy(self.emailEdit)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        addButton = self.buttonBox.button(QDialogButtonBox.Ok)
        addButton.setText("添加(&S)")
        addButton.setEnabled(False)

        testcombobox = QComboBox()
        testcheckbox = QCheckBox()

        grid = QGridLayout()
        grid.addWidget(forenameLabel, 0, 0)
        grid.addWidget(self.forenameEdit, 0, 1)
        grid.addWidget(surnameLabel, 0, 2)
        grid.addWidget(self.surnameEdit, 0, 3)
        grid.addWidget(categoryLabel, 1, 0)
        grid.addWidget(self.categoryComboBox, 1, 1)
        grid.addWidget(companyLabel, 1, 2)
        grid.addWidget(self.companyEdit, 1, 3)
        grid.addWidget(addressLabel, 2, 0)
        grid.addWidget(self.addressEdit, 2, 1, 1, 3)
        grid.addWidget(phoneLabel, 3, 0)
        grid.addWidget(self.phoneEdit, 3, 1)
        grid.addWidget(mobileLabel, 3, 2)
        grid.addWidget(self.mobileEdit, 3, 3)
        grid.addWidget(faxLabel, 4, 0)
        grid.addWidget(self.faxEdit, 4, 1)
        grid.addWidget(emailLabel, 4, 2)
        grid.addWidget(self.emailEdit, 4, 3)
        grid.addWidget(testcombobox,5,0)
        grid.addWidget(testcheckbox,5,2)
        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.lineedits = (self.forenameEdit, self.surnameEdit,
                self.companyEdit, self.phoneEdit, self.emailEdit)
        for lineEdit in self.lineedits:
            lineEdit.setProperty("mandatory", QVariant(True))
            # self.connect(lineEdit, SIGNAL("textEdited(QString)"),
            #              self.updateUi)
            lineEdit.textEdited.connect(self.updateUi)
        # self.connect(self.categoryComboBox, SIGNAL("activated(int)"),
        #              self.updateUi)
        self.categoryComboBox.activated.connect(self.updateUi)

        # self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        # self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        # self.buttonBox.button(QDialogButtonBox.Ok).connect(self.accept)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setStyleSheet(self.StyleSheet2)
        self.setWindowTitle("添加联系人")


    def updateUi(self):
        mandatory = self.companyEdit.property("mandatory") # 先对这个对象是否具有这个属性进行判断，使用property来访问Qt属性
        if self.categoryComboBox.currentText() == "商业":
            self.companyEdit.setProperty("mandatory_edu", QVariant(False))
            self.companyEdit.setProperty("mandatory", QVariant(True))
            for lineedit in self.lineedits:
                lineedit.setProperty("mandatory_edu",QVariant(False))
                lineedit.setProperty("mandatory",QVariant(True))
        elif self.categoryComboBox.currentText() == "教育":
            self.companyEdit.setProperty("mandatory", QVariant(False))
            self.companyEdit.setProperty("mandatory_edu", QVariant(True))
            for lineedit in self.lineedits:
                lineedit.setProperty("mandatory_edu",QVariant(True))
        elif self.categoryComboBox.currentText() == "其他":
            self.companyEdit.setProperty("mandatory", QVariant(False))
            self.companyEdit.setProperty("mandatory_edu", QVariant(False))
            for lineedit in self.lineedits:
                lineedit.setProperty("mandatory_edu",QVariant(False))
                lineedit.setProperty("mandatory",QVariant(False))

        self.setStyleSheet(self.StyleSheet2)
            # 必须更新样式表才能重新生效，但是，只有在必须的时候才进行更新，否则对运行较慢的机器不友好。
        enable = True
        for lineEdit in self.lineedits:
            if lineEdit.text() == '':
                enable = False
                break
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ContactDlg()
    form.show()
    app.exec_()
