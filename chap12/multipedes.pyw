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

import math  # 数学
import random  # 随机
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


SCENESIZE = 500  # 场景SIZE
INTERVAL = 200  # 间隔

Running = False  # 运转


class Head(QGraphicsItem):  # 头部

    Rect = QRectF(-30, -20, 60, 40)

    def __init__(self, color, angle, position):
        super(Head, self).__init__()
        self.color = color
        self.angle = angle  # 角度
        self.setPos(position)
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"), self.timeout)
        self.timer.start(INTERVAL)

    # 边界范围
    def boundingRect(self):
        return Head.Rect

    # 形状:根据返回的形状检测碰撞项.
    def shape(self):
        path = QPainterPath()   # PainterPath : 涂(画)路径|涂(画)范围.
        path.addEllipse(Head.Rect)  # addEllipse:加入椭圆
        return path

    #   涂(画)
    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(Head.Rect)  # 绘制头部
        if option.levelOfDetail > 0.5:  # Outer eyes:外眼(眼白部分). levelOfDetail:级别of细节 > 原图50%时.执行... P282
            painter.setBrush(QBrush(Qt.yellow))  # yellow:黄
            painter.drawEllipse(-12, -19, 8, 8)
            painter.drawEllipse(-12, 11, 8, 8)
            if option.levelOfDetail > 0.9:  # Inner eyes:内眼(瞳孔部分).
                painter.setBrush(QBrush(Qt.darkBlue))   #darkBlue:深蓝
                painter.drawEllipse(-12, -19, 4, 4)
                painter.drawEllipse(-12, 11, 4, 4)
                if option.levelOfDetail > 1.3: # Nostrils:鼻孔
                    painter.setBrush(QBrush(Qt.white))
                    painter.drawEllipse(-27, -5, 2, 2)
                    painter.drawEllipse(-27, 3, 2, 2)


    def timeout(self):
        if not Running:
            return
        angle = self.angle
        while True:
            angle += random.randint(-9, 9)
            offset = random.randint(3, 15)
            x = self.x() + (offset * math.sin(math.radians(angle)))  # sin:正弦,radians:弧度
            y = self.y() + (offset * math.cos(math.radians(angle)))  # cos:余弦
            if 0 <= x <= SCENESIZE and 0 <= y <= SCENESIZE:
                break
        self.angle = angle
        self.rotate(random.randint(-5, 5))  # rotate:旋转
        self.setPos(QPointF(x, y))
        for item in self.scene().collidingItems(self):  # collidingItems:碰撞_项
            if isinstance(item, Head):  # 当碰撞项是Head Class时...
                self.color.setRed(min(255, self.color.red() + 5))   # 碰撞时头部红色成分增加.
            else:
                item.color.setBlue(min(255, item.color.blue() + 5))  # 没有碰撞时头部蓝色成分增加.


# 构造蜈蚣身体
class Segment(QGraphicsItem):

    def __init__(self, color, offset, parent):
        super(Segment, self).__init__(parent)
        self.color = color
        self.rect = QRectF(offset, -20, 30, 40)
        self.path = QPainterPath()
        self.path.addEllipse(self.rect)
        x = offset + 15
        y = -20
        self.path.addPolygon(QPolygonF([QPointF(x, y),
                QPointF(x - 5, y - 12), QPointF(x - 5, y)]))  # 蜈蚣左脚
        self.path.closeSubpath()  # closeSubpath:结束子路径
        y = 20
        self.path.addPolygon(QPolygonF([QPointF(x, y),
                QPointF(x - 5, y + 12), QPointF(x - 5, y)]))  # 蜈蚣右脚
        self.path.closeSubpath()
        self.change = 1
        self.angle = 0
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"), self.timeout)
        self.timer.start(INTERVAL)

    # 边界范围
    def boundingRect(self):
        return self.path.boundingRect()

    # 形状:根据返回的形状检测碰撞项.
    def shape(self):
        return self.path

    # 涂(画)
    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        if option.levelOfDetail < 0.9:   # levelOfDetail:级别of细节 < 90% 时执行...
            painter.drawEllipse(self.rect)
        else:
            painter.drawPath(self.path)


    def timeout(self):
        if not Running:
            return
        matrix = self.matrix()
        matrix.reset()
        self.setMatrix(matrix)
        self.angle += self.change
        if self.angle > 5:
            self.change = -1
            self.angle -= 1
        elif self.angle < -5:
            self.change = 1
            self.angle += 1
        self.rotate(self.angle)


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, SCENESIZE, SCENESIZE)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)   # setItemIndexMethod:设置_项_索引_方法 ?NoIndex:没索引???
        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setScene(self.scene)
        self.view.setFocusPolicy(Qt.NoFocus)   # 设置焦点策略::没焦点
        zoomSlider = QSlider(Qt.Horizontal)  # QSlider:滑块控件, Qt.Horizontal:水平方向
        zoomSlider.setRange(5, 200)
        zoomSlider.setValue(100)
        self.pauseButton = QPushButton("Pa&use")
        quitButton = QPushButton("&Quit")
        quitButton.setFocusPolicy(Qt.NoFocus)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.pauseButton)
        bottomLayout.addWidget(zoomSlider)
        bottomLayout.addWidget(quitButton)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

        self.connect(zoomSlider, SIGNAL("valueChanged(int)"), self.zoom)
        self.connect(self.pauseButton, SIGNAL("clicked()"),
                     self.pauseOrResume)
        self.connect(quitButton, SIGNAL("clicked()"), self.accept)

        self.populate()
        self.startTimer(INTERVAL)
        self.setWindowTitle("Multipedes")


    def zoom(self, value):
        factor = value / 100.0
        matrix = self.view.matrix()
        matrix.reset()
        matrix.scale(factor, factor)
        self.view.setMatrix(matrix)


    def pauseOrResume(self):
        global Running
        Running = not Running
        self.pauseButton.setText("Pa&use" if Running else "Res&ume")


    def populate(self):
        red, green, blue = 0, 150, 0
        for i in range(random.randint(6, 10)):
            angle = random.randint(0, 360)
            offset = random.randint(0, SCENESIZE // 2)
            half = SCENESIZE / 2    # 一半
            x = half + (offset * math.sin(math.radians(angle)))
            y = half + (offset * math.cos(math.radians(angle)))
            color = QColor(red, green, blue)
            head = Head(color, angle, QPointF(x, y))
            color = QColor(red, green + random.randint(10, 60), blue)
            offset = 25
            segment = Segment(color, offset, head)
            for j in range(random.randint(3, 7)):
                offset += 25
                segment = Segment(color, offset, segment)
            head.rotate(random.randint(0, 360))
            self.scene.addItem(head)
        global Running
        Running = True

    # QDialog类自带timer控件.
    def timerEvent(self, event):
        if not Running:
            return
        dead = set()    # dead::死亡的...
        items = self.scene.items()
        if len(items) == 0:
            self.populate()
            return
        heads = set()   # 头???
        for item in items:
            if isinstance(item, Head):
                heads.add(item)
                if item.color.red() == 255:
                    dead.add(item)
        if len(heads) == 1:
            dead = heads
        del heads
        while dead:
            item = dead.pop()
            self.scene.removeItem(item)
            del item


app = QApplication(sys.argv)
form = MainForm()
rect = QApplication.desktop().availableGeometry()   # QApplication::应用程序, desktop::桌面, .availableGeometry::可用_几何(范围).
form.resize(int(rect.width() * 0.75), int(rect.height() * 0.9))
form.show()
app.exec_()

