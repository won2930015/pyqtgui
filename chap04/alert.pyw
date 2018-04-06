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
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *


app = QApplication(sys.argv)

try:
    due = QTime.currentTime()   #获得当前时间.
    message = "Alert!"
    if len(sys.argv) < 2:
        raise ValueError
    hours, mins = sys.argv[1].split(":")  # 如果参数1没有:号将触发ValueError异常.
    due = QTime(int(hours), int(mins))  # 如果int()转换的不是数值也触发ValueError异常.
    if not due.isValid():   #如果int()转换的数值超出有效时间范围会令due无效.需检查due的有效性,无效手动抛错.
        raise ValueError
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
except ValueError:
    message = "Usage: alert.pyw HH:MM [optional message]" # 24hr clock

while QTime.currentTime() < due:
    time.sleep(20) # 20 seconds

label = QLabel("<font color=red size=72><b>{}</b></font>"
               .format(message))
label.setWindowFlags(Qt.SplashScreen)   #设置label为闪屏窗口.类似PyCharm启动窗口.
label.show()  # 调用show(),show()会向QApplication对象的事件队列添加一个新事件,请求对特定窗口部件进行绘制.
QTimer.singleShot(60000, app.quit)  # 1 minute后,app.quit释放所有资源,干净地结束掉GUI应用程序.
app.exec_()  # 开始执行QApplication对象的事件循环. 循环伪代码如下↓:

'''
 # 事件循环伪代码:
while True:
   event =getNextEvent()
    if event:
        if event == Terminate:
            break
        processEvent(event)
'''