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

import platform  #platform::平台：获取系统及python一些信息.
from PyQt4.QtCore import *
from PyQt4.QtGui import *

X11 = True
try:
    from PyQt4.QtGui import qt_x11_wait_for_window_manager
except ImportError:
    X11 = False


class FractionSlider(QWidget):#分数滑动器.

    XMARGIN = 12.0  #X边缘
    YMARGIN = 5.0   #边缘
    WSTRING = "999" #字符串 宽

    def __init__(self, numerator=0, denominator=10, parent=None):   #numerator=分子, denominator=分母。
        super(FractionSlider, self).__init__(parent)
        self.__numerator = numerator
        self.__denominator = denominator
        self.setFocusPolicy(Qt.WheelFocus)  #setFocusPolicy:设焦点策略,Qt.WheelFocus:切换到,点击,使用滚轮,多能获得焦点.
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                       QSizePolicy.Fixed))  #setSizePolicy:设置尺寸策略（X:最小可扩展，Y:固定）


    def decimal(self):  #小数：分数/分母 == 3/10 = 0.3.
        return self.__numerator / float(self.__denominator)


    def fraction(self): #return(分数,分母)
        return self.__numerator, self.__denominator


    def sizeHint(self): #尺寸提示
        return self.minimumSizeHint()


    def minimumSizeHint(self):  #最小尺寸提示
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1) #setPointSize:设置字体节点尺寸(字号大小).
        fm = QFontMetricsF(font)    #获得字体度量对象(用于设置字体的宽/高).
        return QSize(fm.width(FractionSlider.WSTRING) *
                     self.__denominator,
                     (fm.height() * 4) + FractionSlider.YMARGIN)


    def setFraction(self, numerator, denominator=None): #设置分数
        if denominator is not None:
            if 3 <= denominator <= 60:
                self.__denominator = denominator
            else:
                raise ValueError("denominator out of range")
        if 0 <= numerator <= self.__denominator:
            self.__numerator = numerator
        else:
            raise ValueError("numerator out of range")
        self.update()   #执行update()方法,触发paintEvent事件
        self.updateGeometry() #刷新控件几何位置.


    def mousePressEvent(self, event):   #鼠标按下事件
        if event.button() == Qt.LeftButton:
            self.moveSlider(event.x())
            event.accept()
        else:
            QWidget.mousePressEvent(self, event)


    def mouseMoveEvent(self, event):    #鼠标移动事件(鼠标跟踪为:False时拖动鼠标才执行该事件.)
        self.moveSlider(event.x())


    def moveSlider(self, x):    #移动△滑块
        span = self.width() - (FractionSlider.XMARGIN * 2)
        offset = span - x + FractionSlider.XMARGIN
        numerator = int(round(self.__denominator *
                        (1.0 - (offset / span))))   #计算分子的值,round:圆正(四舍五入)
        numerator = max(0, min(numerator, self.__denominator))
        if numerator != self.__numerator:
            self.__numerator = numerator
            self.emit(SIGNAL("valueChanged(int,int)"),
                      self.__numerator, self.__denominator)
            self.update()


    def keyPressEvent(self, event): #键按下事件
        change = 0
        if event.key() == Qt.Key_Home:
            change = -self.__denominator
        elif event.key() in (Qt.Key_Up, Qt.Key_Right):
            change = 1
        elif event.key() == Qt.Key_PageUp:
            change = (self.__denominator // 10) + 1
        elif event.key() in (Qt.Key_Down, Qt.Key_Left):
            change = -1
        elif event.key() == Qt.Key_PageDown:
            change = -((self.__denominator // 10) + 1)
        elif event.key() == Qt.Key_End:
            change = self.__denominator
        if change:
            numerator = self.__numerator
            numerator += change
            numerator = max(0, min(numerator, self.__denominator))
            if numerator != self.__numerator:
                self.__numerator = numerator
                self.emit(SIGNAL("valueChanged(int,int)"),
                          self.__numerator, self.__denominator)
                self.update()
            event.accept()
        else:
            QWidget.keyPressEvent(self, event)


    def paintEvent(self, event=None):   #绘画事件
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)  #setPointSize:设置字体(节点)尺寸:字号大小.
        fm = QFontMetricsF(font)    #获得字体度量对象(用于设置字体的宽/高)
        fracWidth = fm.width(FractionSlider.WSTRING)
        indent = fm.boundingRect("9").width() / 2.0 #.boundingRect:边界框
        if not X11:
            fracWidth *= 1.5
        span = self.width() - (FractionSlider.XMARGIN * 2)
        value = self.__numerator / float(self.__denominator)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)    #setRenderHint:设置渲染提示,Antialiasing:反锯齿
        painter.setRenderHint(QPainter.TextAntialiasing)    #TextAntialiasing:文本反锯齿
        painter.setPen(self.palette().color(QPalette.Mid))  #设置Pen画笔,用于形状轮廓和文本绘制.
        painter.setBrush(self.palette().brush(
                QPalette.AlternateBase))#设置Brush画刷为填充底色.
        painter.drawRect(self.rect())   #绘制矩形.
        segColor = QColor(Qt.green).dark(120)   #创建颜色对象 绿色 色深120
        segLineColor = segColor.dark()
        painter.setPen(segLineColor)    #设置画笔
        painter.setBrush(segColor)  #设置画刷,用于填充.
        painter.drawRect(FractionSlider.XMARGIN,
                         FractionSlider.YMARGIN, span, fm.height()) #创建一字高绿底色矩形.
        textColor = self.palette().color(QPalette.Text) #用调色板创建文体颜色对象.
        segWidth = span / self.__denominator    #求出间隔宽
        segHeight = fm.height() * 2 #间隔条高度
        nRect = fm.boundingRect(FractionSlider.WSTRING) #单个间隔边框矩形
        x = FractionSlider.XMARGIN
        yOffset = segHeight + fm.height()   # y轴偏移
        for i in range(self.__denominator + 1):
            painter.setPen(segLineColor)
            painter.drawLine(x, FractionSlider.YMARGIN, x, segHeight)
            painter.setPen(textColor)
            y = segHeight
            rect = QRectF(nRect)
            rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
            painter.drawText(rect, Qt.AlignCenter, "{}".format(i))
            y = yOffset
            rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
            painter.drawText(rect, Qt.AlignCenter,
                             "{}".format(self.__denominator))
            painter.drawLine(QPointF(rect.left() + indent, y),
                             QPointF(rect.right() - indent, y))
            x += segWidth
        span = int(span)
        y = FractionSlider.YMARGIN - 0.5
        triangle = [QPointF(value * span, y),
                    QPointF((value * span) +
                            (2 * FractionSlider.XMARGIN), y),
                    QPointF((value * span) +
                            FractionSlider.XMARGIN, fm.height())]   #创建三角形
        painter.setPen(Qt.yellow)   #Pen设置为标准黄
        painter.setBrush(Qt.darkYellow) #Brush设置为深黄
        painter.drawPolygon(QPolygonF(triangle))    #画多边形.


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = QDialog()
    sliderLabel = QLabel("&Fraction")
    slider = FractionSlider(numerator=2,denominator=20)
    sliderLabel.setBuddy(slider)
    denominatorLabel = QLabel("&Denominator")
    denominatorSpinBox = QSpinBox()
    denominatorLabel.setBuddy(denominatorSpinBox)
    denominatorSpinBox.setRange(3, 60)
    denominatorSpinBox.setValue(slider.fraction()[1])   #取分母值.
    denominatorSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
    numeratorLabel = QLabel("Numerator")
    numeratorLCD = QLCDNumber()
    numeratorLCD.setSegmentStyle(QLCDNumber.Flat)   #setSegmentStyle:线段 样式
    numeratorLabel. setBuddy(numeratorLCD)
    layout = QGridLayout()
    layout.addWidget(sliderLabel, 0, 0)
    layout.addWidget(slider, 0, 1, 1, 5)
    layout.addWidget(numeratorLabel, 1, 0)
    layout.addWidget(numeratorLCD, 1, 1)
    layout.addWidget(denominatorLabel, 1, 2)
    layout.addWidget(denominatorSpinBox, 1, 3)
    form.setLayout(layout)

    def valueChanged(denominator):  #值改变
        numerator = int(slider.decimal() * denominator)
        slider.setFraction(numerator, denominator)
        numeratorLCD.display(numerator)
        
    form.connect(slider, SIGNAL("valueChanged(int,int)"),
                 numeratorLCD, SLOT("display(int)"))    #触发slider的valueChanged信号时触发.
    form.connect(denominatorSpinBox, SIGNAL("valueChanged(int)"),
                 valueChanged)  #触发denominatorSpinBox的valueChanged信号时触发.
    form.setWindowTitle("Fraction Slider")
    form.show()
    app.exec_()

