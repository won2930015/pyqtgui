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


class YPipeWidget(QWidget):

    def __init__(self, leftFlow=0, rightFlow=0, maxFlow=100,
                 parent=None):  #Flow:流量.
        super(YPipeWidget, self).__init__(parent)

        self.leftSpinBox = QSpinBox(self)
        self.leftSpinBox.setRange(0, maxFlow)
        self.leftSpinBox.setValue(leftFlow)
        self.leftSpinBox.setSuffix(" l/s")  #setSuffix:设置后缀
        self.leftSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.connect(self.leftSpinBox, SIGNAL("valueChanged(int)"),
                     self.valueChanged)

        self.rightSpinBox = QSpinBox(self)
        self.rightSpinBox.setRange(0, maxFlow)
        self.rightSpinBox.setValue(rightFlow)
        self.rightSpinBox.setSuffix(" l/s")
        self.rightSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.connect(self.rightSpinBox, SIGNAL("valueChanged(int)"),
                     self.valueChanged)

        self.label = QLabel(self)
        self.label.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)  #设置边框样式.
        self.label.setAlignment(Qt.AlignCenter)
        fm = QFontMetricsF(self.font())#QFontMetricsF:返回'字符串'字体度量对象.尾缀F代表返回的是浮点数.无尾缀返回的是整数.
        self.label.setMinimumWidth(fm.width(" 999 l/s "))   #setMinimumWidth:设置最小宽度

        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding))  #setSizePolicy:设置尺寸策略(x:扩展,y:扩展)
        self.setMinimumSize(self.minimumSizeHint())
        self.valueChanged()


    def valueChanged(self):
        a = self.leftSpinBox.value()
        b = self.rightSpinBox.value()
        self.label.setText("{} l/s".format(a + b))
        self.emit(SIGNAL("valueChanged"), a, b)
        self.update()


    def values(self):
        return self.leftSpinBox.value(), self.rightSpinBox.value()


    def minimumSizeHint(self):
        return QSize(self.leftSpinBox.width() * 3,
                     self.leftSpinBox.height() * 5)


    def resizeEvent(self, event=None):  # resizeEvent:调整尺寸事件.
        fm = QFontMetricsF(self.font())
        x = (self.width() - self.label.width()) / 2
        y = self.height() - (fm.height() * 1.5)
        self.label.move(x, y)   #定位label到窗口底部中间.
        y = self.height() / 60.0
        x = (self.width() / 4.0) - self.leftSpinBox.width() #定位左则:leftSpinBox
        self.leftSpinBox.move(x, y)
        x = self.width() - (self.width() / 4.0) #定位右则:rightSpinBox
        self.rightSpinBox.move(x, y)


    def paintEvent(self, event=None):
        LogicalSize = 100.0 #罗辑尺寸.

        def logicalFromPhysical(length, side):
            return (length / side) * LogicalSize
        
        fm = QFontMetricsF(self.font())
        ymargin = ((LogicalSize / 30.0) +
                   logicalFromPhysical(self.leftSpinBox.height(),
                                       self.height()))  #ymargin: y边界(y轴上边界值)
        ymax = (LogicalSize -
                logicalFromPhysical(fm.height() * 2, self.height()))#y轴下边界值.
        width = LogicalSize / 4.0
        cx, cy = LogicalSize / 2.0, LogicalSize / 3.0
        ax, ay = cx - (2 * width), ymargin
        bx, by = cx - width, ay
        dx, dy = cx + width, ay
        ex, ey = cx + (2 * width), ymargin
        fx, fy = cx + (width / 2), cx + (LogicalSize / 24.0)
        gx, gy = fx, ymax
        hx, hy = cx - (width / 2), ymax
        ix, iy = hx, fy

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)    #设置渲染提示:反锯齿
        side = min(self.width(), self.height())
        painter.setViewport((self.width() - side) / 2,
                            (self.height() - side) / 2, side, side)
        painter.setWindow(0, 0, LogicalSize, LogicalSize)

        painter.setPen(Qt.NoPen)

        #上左通道颜色填充.
        gradient = QLinearGradient(QPointF(0, 0),
                                         QPointF(0, 100))   #LinearGradient:线性渐变
        gradient.setColorAt(0, Qt.white)    # Qt.white:白色
        a = self.leftSpinBox.value()
        gradient.setColorAt(1, (Qt.red if a != 0 else Qt.white))
        painter.setBrush(QBrush(gradient))
        painter.drawPolygon(QPolygon([ax, ay, bx, by, cx, cy, ix, iy])) #drawPolygon:绘制_多边形.

        #上右通道颜色填充.
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 100))
        gradient.setColorAt(0, Qt.white)
        b = self.rightSpinBox.value()
        gradient.setColorAt(1, (Qt.blue if b != 0
                                else Qt.white))
        painter.setBrush(QBrush(gradient))
        painter.drawPolygon(QPolygon([cx, cy, dx, dy, ex, ey, fx, fy]))

        #下中通道颜色填充.
        if (a + b) == 0:
            color = QColor(Qt.white)
        else:
            ashare = (a / (a + b)) * 255.0
            bshare = 255.0 - ashare
            color = QColor(ashare, 0, bshare)
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 100))
        gradient.setColorAt(0, Qt.white)
        gradient.setColorAt(1, color)
        painter.setBrush(QBrush(gradient))
        painter.drawPolygon(QPolygon(
                [cx, cy, fx, fy, gx, gy, hx, hy, ix, iy]))


        #画左中右三条黑色边线.
        painter.setPen(Qt.black)
        painter.drawPolyline(QPolygon([ax, ay, ix, iy, hx, hy]))
        painter.drawPolyline(QPolygon([gx, gy, fx, fy, ex, ey]))
        painter.drawPolyline(QPolygon([bx, by, cx, cy, dx, dy]))



if __name__ == "__main__":
    import sys

    def valueChanged(a, b):
        print(a, b)

    app = QApplication(sys.argv)
    form = YPipeWidget()
    form.connect(form, SIGNAL("valueChanged"), valueChanged)
    form.setWindowTitle("YPipe")
    form.move(0, 0)
    form.show()
    form.resize(400, 400)
    app.exec_()

