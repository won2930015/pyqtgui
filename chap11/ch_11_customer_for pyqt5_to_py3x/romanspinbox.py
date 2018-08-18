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

import re
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


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
         "IV", "I"]) # 返回一个元组
    if integer <= 0 or integer >= 4000 or int(integer) != integer:
        raise ValueError("expecting an integer between 1 and 3999")
    result = []
    for decimal, roman in coding:
        while integer >= decimal:
            result.append(roman)
            integer -= decimal
    return "".join(result)


def intFromRoman(roman):
    """
    Code taken from Paul Winkler's "Roman Numerals" recipe in the Python
    Cookbook.
    """
    roman = roman.upper()
    coding = (("M",  1000, 3), ("CM", 900, 1), ("D",  500, 1),
              ("CD", 400, 1), ("C",  100, 3), ("XC", 90, 1),
              ("L",  50, 1), ("XL", 40, 1), ("X",  10, 3),
              ("IX", 9, 1), ("V",  5, 1),  ("IV", 4, 1), ("I",  1, 3))
    integer, index = 0, 0
    for numeral, value, maxrepeat in coding:
        count = 0
        while roman[index: index +len(numeral)] == numeral:
            count += 1
            if count > maxrepeat:
                raise ValueError("not a valid roman number: {0}".format(
                        roman))
            integer += value
            index += len(numeral)
    if index != len(roman):
        raise ValueError("not a valid roman number: {0}".format(roman))
    return integer


# Regex adapted from Mark Pilgrim's "Dive Into Python" book
class RomanSpinBox(QSpinBox): # 子类化一个新的类

    def __init__(self, parent=None):
        super(RomanSpinBox, self).__init__(parent)
        regex = QRegExp(r"^M?M?M?(?:CM|CD|D?C?C?C?)"
                        r"(?:XC|XL|L?X?X?X?)(?:IX|IV|V?I?I?I?)$") #只接受罗马数字的输入 Qt的正则表达不支持贪婪量词
        regex.setCaseSensitivity(Qt.CaseInsensitive) # 大小写敏感 \.txt$ matches readme.txt but not README.TXT.
        self.validator = QRegExpValidator(regex, self)
        self.setRange(1, 3999)
        # self.connect(self.lineEdit(), SIGNAL("textEdited(QString)"),
        #              self.fixCase)
        self.lineEdit().textEdited.connect(self.fixCase)
        # 因为是实例化的子类，所以在这里使用self.lineEdit()而不使用self.lineEdit


    def fixCase(self, text):
        self.lineEdit().setText(text.upper())


    def validate(self, text, pos):
        # This virtual function is called by the QAbstractSpinBox to determine whether input is valid. 
        # The pos parameter indicates the position in the string. Reimplemented in the various subclasses.
        return self.validator.validate(text, pos)
        # This virtual function returns Invalid if input is invalid according to this validator's rules, 
        # Intermediate if it is likely that a little more editing will make the input acceptable 
        # (e.g. the user types "4" into a widget which accepts integers between 10 and 99), and Acceptable if the input is valid.


    def valueFromText(self, text):
        return intFromRoman(str(text))


    def textFromValue(self, value):
        return romanFromInt(value)


if __name__ == "__main__":
    def report(value):
        print("{0:4d} {1}".format(value, romanFromInt(value)))

    app = QApplication(sys.argv)
    spinbox = RomanSpinBox()
    spinbox.show()
    spinbox.setWindowTitle("罗马数字转换")
    # spinbox.connect(spinbox, SIGNAL("valueChanged(int)"), report)
    spinbox.valueChanged.connect(report)
    app.exec_()
