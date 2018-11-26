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

import math
import random
import string
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numberformatdlg1
import numberformatdlg2
import numberformatdlg3


class Form(QDialog):

    X_MAX = 26
    Y_MAX = 60

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.numberFormatDlg = None
        self.format = dict(thousandsseparator=",", decimalmarker=".",  # thousands_separator:千位分隔符号,decimal_marker:小数点标识
                decimalplaces=2, rednegatives=False)  # decimal_places::小数保留位数 ,red_negatives::红名否定
        self.numbers = {}
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                self.numbers[(x, y)] = (10000 * random.random()) - 5000  # 生成26*60的随机数值表

        self.table = QTableWidget()
        formatButton1 = QPushButton("Set Number Format... (&Modal)")
        formatButton2 = QPushButton("Set Number Format... (Modele&ss)")
        formatButton3 = QPushButton("Set Number Format... (`&Live')")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(formatButton1)
        buttonLayout.addWidget(formatButton2)
        buttonLayout.addWidget(formatButton3)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(formatButton1, SIGNAL("clicked()"),
                     self.setNumberFormat1)
        self.connect(formatButton2, SIGNAL("clicked()"),
                     self.setNumberFormat2)
        self.connect(formatButton3, SIGNAL("clicked()"),
                     self.setNumberFormat3)
        self.setWindowTitle("Numbers")
        self.refreshTable()  # 更新_表


    def refreshTable(self):
        """更新_表"""

        self.table.clear()
        self.table.setColumnCount(self.X_MAX)  # 设置_列
        self.table.setRowCount(self.Y_MAX)  # 设置_行
        self.table.setHorizontalHeaderLabels(  # 设置_水平_头标签
                list(string.ascii_uppercase))  # uppercase::大写字母::返回26个大写字母[A,B,C,D,E,F,...]作为头标签.
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                fraction, whole = math.modf(self.numbers[(x, y)])  # fraction::分数, whole::整数 ,modf()::浮点数分解函数
                sign = "-" if whole < 0 else ""  # sign:符号, 整数是负数时加 -号.
                whole = "{}".format(int(math.floor(abs(whole))))  # 向下取整::math.floor(3.9999)==3
                digits = []
                for i, digit in enumerate(reversed(whole)):  # 遍历整数部份加入千位分隔符.
                    if i and i % 3 == 0:
                        digits.insert(0, self.format["thousandsseparator"])
                    digits.insert(0, digit)
                if self.format["decimalplaces"]:  # 小数保留位数大于 0 时执行.
                    fraction = "{0:.7f}".format(abs(fraction))
                    fraction = (self.format["decimalmarker"] +
                            fraction[2:self.format["decimalplaces"] + 2])  # 因从2开始截取所以后面要加2才是正确的要保留的小数位
                else:
                    fraction = ""
                text = "{}{}{}".format(sign, "".join(digits), fraction)
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignRight|
                                      Qt.AlignVCenter)
                if sign and self.format["rednegatives"]:  # 开启负数红名时执行.
                    item.setBackgroundColor(Qt.red)
                self.table.setItem(y, x, item)


    def setNumberFormat1(self):
        """应用模态弹出窗设置表格数据的显示样式"""
        dialog = numberformatdlg1.NumberFormatDlg(self.format, self)
        if dialog.exec_():  # 使用模态方式弹出标准对话框.
            self.format = dialog.numberFormat()  # 返回标准对话框的设置内容.
            self.refreshTable()  # 填充表格.


    def setNumberFormat2(self):
        """非模态弹出窗口+提交后更新"""
        dialog = numberformatdlg2.NumberFormatDlg(self.format, self)
        self.connect(dialog, SIGNAL("changed"), self.refreshTable)
        dialog.show()


    def setNumberFormat3(self):
        if self.numberFormatDlg is None:
            self.numberFormatDlg = numberformatdlg3.NumberFormatDlg(
                    self.format, self.refreshTable, self)
        self.numberFormatDlg.show()
        self.numberFormatDlg.raise_()  # raise_::提升?提升为顶层窗口???
        self.numberFormatDlg.activateWindow()  # 激活窗口,获得光标.


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

