_author_ = 'Administrator'
_project_ = 'pyqtgui2'

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import random
import string
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numberformatdlg1
import numberformatdlg2
import numberformatdlg3


class Form(QDialog):

    X_MAX = 26
    Y_MAX = 60

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.numberFormatDlg = None
        self.format = dict(thousandsseparator=",",
                           decimalmarker=".", decimalplaces=2,
                           rednegatives=False)
        self.numbers = {}
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                self.numbers[(x, y)] = (10000 * random.random()) - 5000

        self.table = QTableWidget()
        formatButton1 = QPushButton("Set Number Format... "
                                    "(&Modal)")

        formatButton2 = QPushButton("Set Number Format... "
                                    "(Modele&ss)")

        formatButton3 = QPushButton("Set Number Format... "
                                    "(`&Live')")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(formatButton1)
        buttonLayout.addWidget(formatButton2)
        buttonLayout.addWidget(formatButton3)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        formatButton1.clicked.connect(self.setNumberFormat1)
        formatButton2.clicked.connect(self.setNumberFormat2)
        formatButton3.clicked.connect(self.setNumberFormat3)
        self.setWindowTitle("Numbers")
        self.refreshTable()


    def refreshTable(self):
        self.table.clear()
        self.table.setColumnCount(self.X_MAX)
        self.table.setRowCount(self.Y_MAX)
        self.table.setHorizontalHeaderLabels(
                list(string.ascii_uppercase))#设置表头， list(string.ascii_uppercase)表示将引入的string模块的从A到Z的字母作为列表，设置成表头
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                fraction, whole = math.modf(self.numbers[(x, y)])#modf() 方法返回整数部分与小数部分，两部分的数值符号与x相同，整数部分以浮点型表示。
                sign = "-" if whole < 0 else ""
                whole = "%d" % math.floor(abs(whole))# "%d" % 表示对数字进行格式化，得到的是一个十进制整数的字符串
                digits = []
                for i, digit in enumerate(reversed(whole)):#reversed()函数是返回序列seq的反向访问的迭代子，enumerate可以同时获得索引和值
                    if i and i % 3 == 0:
                        digits.insert(0, self.format["thousandsseparator"])
                    digits.insert(0, digit)
                if self.format["decimalplaces"]:
                    fraction = "%0.7f" % abs(fraction)
                    fraction = (self.format["decimalmarker"] +
                                fraction[2:self.format["decimalplaces"]
                                + 2])
                else:
                    fraction = ""
                text = "%s%s%s" % (sign, "".join(digits), fraction)
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                if sign and self.format["rednegatives"]:
                    item.setBackground(Qt.red)#setBackgroundColor已变成了setBackground
                self.table.setItem(y, x, item)



    def setNumberFormat1(self):
        dialog = numberformatdlg1.NumberFormatDlg(self.format, self)
        if dialog.exec_():
            self.format = dialog.numberFormat()
            self.refreshTable()


    def setNumberFormat2(self):
        dialog = numberformatdlg2.NumberFormatDlg(self.format, self)
        #self.connect(dialog, SIGNAL("changed"), self.refreshTable)
        dialog.changed.connect(self.refreshTable)
        dialog.show()


    def setNumberFormat3(self):
        if self.numberFormatDlg is None:
            self.numberFormatDlg = numberformatdlg3.NumberFormatDlg(
                    self.format, self.refreshTable, self)
        self.numberFormatDlg.show()
        self.numberFormatDlg.raise_()
        self.numberFormatDlg.activateWindow()



app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()