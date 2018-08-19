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

import re
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


# 从十进制整数转换到罗马数字
def romanFromInt(integer):
    """
    Code taken from Raymond Hettinger's code in Victor Yang's "Decimal
    to Roman Numerals" recipe in the Python Cookbook.

    >>> r = [romanFromInt(x) for x in range(1, 4000)]
    >>> i = [intFromRoman(x) for x in r]
    >>> i == [x for x in range(1, 4000)]
    True
    """
    coding = zip(
        [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1], 
        ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V",
         "IV", "I"])
    if integer <= 0 or integer >= 4000 or int(integer) != integer:  # 0或负数 ,4000及以上 和 非整数 的抛错.
        raise ValueError("expecting an integer between 1 and 3999")
    result = []
    for decimal, roman in coding:   # decimal:十进制数, roman：罗马数字
        while integer >= decimal:
            result.append(roman)
            integer -= decimal
    return "".join(result)

# 从罗马数字转换到十进制整数
def intFromRoman(roman):
    """
    Code taken from Paul Winkler's "Roman Numerals" recipe in the Python
    Cookbook.
    """
    roman = roman.upper()
    coding = (("M",  1000, 3), ("CM", 900, 1), ("D",  500, 1),
              ("CD", 400, 1), ("C",  100, 3), ("XC", 90, 1),
              ("L",  50, 1), ("XL", 40, 1), ("X",  10, 3),
              ("IX", 9, 1), ("V",  5, 1),  ("IV", 4, 1), ("I",  1, 3))  # 格式::(罗马数,十进制数,该数值最大可重复的次数)
    integer, index = 0, 0
    for numeral, value, maxrepeat in coding:
        count = 0
        while roman[index: index +len(numeral)] == numeral:  # roman[index: index +len(numeral)] :切片(提取字符).
            count += 1
            if count > maxrepeat:
                raise ValueError("not a valid roman number: {}".format(
                        roman))
            integer += value
            index += len(numeral)
    if index != len(roman):
        raise ValueError("not a valid roman number: {}".format(roman))
    return integer


# Regex adapted from Mark Pilgrim's "Dive Into Python" book
class RomanSpinBox(QSpinBox):   # 自定义 罗马数值SpinBox控件.

    def __init__(self, parent=None):
        super(RomanSpinBox, self).__init__(parent)
        regex = QRegExp(r"^M?M?M?(?:CM|CD|D?C?C?C?)"
                        r"(?:XC|XL|L?X?X?X?)(?:IX|IV|V?I?I?I?)$")  # 例M?:适配0或1个M
        # 设置正则表达式模式为 非贪婪匹配.
        regex.setCaseSensitivity(Qt.CaseInsensitive)  # setCaseSensitivity::设置 案件 敏感度 ,Qt.CaseInsensitive::案件 不敏感的
        self.validator = QRegExpValidator(regex, self)  # validator：验证器
        self.setRange(1, 3999)
        self.connect(self.lineEdit(), SIGNAL("textEdited(QString)"),
                     self.fixCase)


    def fixCase(self, text):
        self.lineEdit().setText(text.upper())

    # 验证:用于防止在微调框中输入无效数据。这个方法会在用户修改文本时被自动调用
    def validate(self, text, pos):
        return self.validator.validate(text, pos)

    # 罗马数字转换为整数,内置方法:当调节数值时会被自动调用
    def valueFromText(self, text):
        return intFromRoman(text)

    # 整数转换为罗马数字,内置方法:当调节数值时会被自动调用
    def textFromValue(self, value):
        return romanFromInt(value)


if __name__ == "__main__":
    def report(value):
        print("{0:4d} {1}".format(value, romanFromInt(value)))

    app = QApplication(sys.argv)
    spinbox = RomanSpinBox()
    spinbox.show()
    spinbox.setWindowTitle("Roman")
    spinbox.connect(spinbox, SIGNAL("valueChanged(int)"), report)
    app.exec_()
