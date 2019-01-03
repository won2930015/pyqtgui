_author_ = 'Administrator'
_project_ = 'pyqtgui2'

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# <editor-fold desc="QApplication 定位在PyQt5.QtWidgets中">
# 如果用PyQt5，在原码的基础上，将from PyQt4.QtCore import * 改成from PyQt5.QtCore import *，from PyQt5.QtGui import *，
# 程序是无法正确运行的。运行之后，没有任何反应。原因在于，QApplication 已经定位到PyQt5.QtWidgets这个模块了。所以，要加入from PyQt5.QtWidgets import *。完整的代码为：
# </editor-fold>

import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)

try:
    due = QTime.currentTime()
    message = "Alert!"
    if len(sys.argv) < 2:
        raise ValueError

    hours,mins = sys.argv[1].split(":")
    due = QTime(int(hours),int(mins))
    if not due.isValid():
        raise ValueError

    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])

except ValueError:
    message = "Usage:alert.pyw HH:MM [optional message]"

while QTime.currentTime() < due:
    time.sleep(20)

label = QLabel("<font color=red size=72><b>" + message + "</b></font>")

label.setWindowFlags(Qt.SplashScreen)
label.show()
QTimer.singleShot(60000,app.quit)
app.exec_()