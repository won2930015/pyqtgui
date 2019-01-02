_author_ = 'Administrator'
_project_ = 'pyqtgui2'

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# <editor-fold desc="存在的问题">
# 解决了。继续更新。问题就出在text = unicode(self.lineedit.text())
# 这个地方。因为我安装的是python3.5，python3以上版本，默认都是unicode，所以把unicode去掉就OK了。pyqt5 + phython3的完整代码：
# </editor-fold>

from __future__ import division
import sys
from math import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.lineedit = QLineEdit("Type an expression and press Enter")
        self.lineedit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        #self.connect(self.lineedit, SIGNAL("returnPressed()"),
        #             self.updateUi)
        self.lineedit.returnPressed.connect(self.updateUi)
        self.setWindowTitle("Calculate")


    def updateUi(self):
        try:
            text = self.lineedit.text()
            self.browser.append("%s = <b>%s</b>" % (text, eval(text)))

        except:
            self.browser.append(
                    "<font color=red>%s is invalid!</font>" % text)



app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()