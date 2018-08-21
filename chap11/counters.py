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

BLANK, RED, YELLOW = range(3)   # 0,1,2


class CountersWidget(QWidget):

    def __init__(self, parent=None):
        super(CountersWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding))
        self.grid = [[BLANK] * 3 for i in range(3)] # grid = [[0,0,0],[0,0,0],[0,0,0]]
        self.selected = [0, 0]
        self.setMinimumSize(self.minimumSizeHint())


    def sizeHint(self):
        return QSize(200, 200)


    def minimumSizeHint(self):
        return QSize(100, 100)


    def mousePressEvent(self, event):
        xOffset = self.width() / 3
        yOffset = self.height() / 3
        if event.x() < xOffset:     # 小于xOffset(x偏移),鼠标位于0列.
            x = 0
        elif event.x() < 2 * xOffset:   # 小于2*xOffset(x偏移),鼠标位于1列.
            x = 1
        else:   # 鼠标位于2列
            x = 2
        if event.y() < yOffset:     # 小于yOffset(y轴偏移),鼠标位于0行.
            y = 0
        elif event.y() < 2 * yOffset:   # 小于2*yOffset(y轴偏移),鼠标位于1行
            y = 1
        else:   # 鼠标位于2行.
            y = 2
        cell = self.grid[x][y]
        if cell == BLANK:
            cell = RED
        elif cell == RED:
            cell = YELLOW
        else:
            cell = BLANK
        self.grid[x][y] = cell
        self.selected = [x, y]
        self.update()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.selected[0] = (2 if self.selected[0] == 0
                                else self.selected[0] - 1)
        elif event.key() == Qt.Key_Right:
            self.selected[0] = (0 if self.selected[0] == 2
                                else self.selected[0] + 1)
        elif event.key() == Qt.Key_Up:
            self.selected[1] = (2 if self.selected[1] == 0
                                else self.selected[1] - 1)
        elif event.key() == Qt.Key_Down:
            self.selected[1] = (0 if self.selected[1] == 2
                                else self.selected[1] + 1)
        elif event.key() == Qt.Key_Space:
            x, y = self.selected
            cell = self.grid[x][y]
            if cell == BLANK:
                cell = RED
            elif cell == RED:
                cell = YELLOW
            else:
                cell = BLANK
            self.grid[x][y] = cell
        self.update()


    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        xOffset = self.width() / 3
        yOffset = self.height() / 3
        for x in range(3):
            for y in range(3):
                cell = self.grid[x][y]
                rect = (QRectF(x * xOffset, y * yOffset,
                        xOffset, yOffset).adjusted(0.5, 0.5, -0.5, -0.5))   # adjusted:调整
                color = None
                if cell == RED:
                    color = Qt.red
                elif cell == YELLOW:
                    color = Qt.yellow
                if color is not None:
                    painter.save()  # save()用于保存 QPainter 的状态. https://blog.csdn.net/TemetNosce/article/details/78059042
                    painter.setPen(Qt.black)
                    painter.setBrush(color)
                    painter.drawEllipse(rect.adjusted(2, 2, -2, -2))
                    painter.restore()  # restore() 用于恢复 QPainter 的状态，save() 和 restore() 一般都是成对使用的.
                if [x, y] == self.selected:
                    painter.setPen(QPen(Qt.blue, 3))
                else:
                    painter.setPen(Qt.black)
                painter.drawRect(rect)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = CountersWidget()
    form.setWindowTitle("Counters")
    form.show()
    app.exec_()

