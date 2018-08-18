#!/usr/bin/env python3
import sys,traceback
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

BLANK, RED, YELLOW = range(3)

class Counters(QWidget):
    def __init__(self,parent = None):
        super(Counters,self).__init__(parent)
        # self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                    #    QSizePolicy.Fixed))
        self.setMinimumSize(self.minimumSizeHint())
        # self.setMinimumSize(QSize(200,200))
        self.grid = [[BLANK]*3 for i in range(3)]
        self.select = [1,1]
        sizepolicy = QSizePolicy()
        sizepolicy.setWidthForHeight(True) # 只在QGraphicsWidget下有用，但是使用resizeEvent的话，绘制有延迟
        self.setSizePolicy(sizepolicy)

    # def resizeEvent(self, event):
    #     # self.resize(self.width(),self.width())
    #     # self.update()
    #     pass

    def minimumSizeHint(self):
        # miniSizeHint 会返回一个最小size的底线，layout不会比此规定更小，但是除非你使用setminsize()强制设定尺寸
        # 通常在此设定自定义widght的最小规则，然后传递给setminsize规定。
        # 传入——> If the value of this property is an invalid size, no minimum size is recommended.
        # 调用——> The default implementation of minimumSizeHint() returns an invalid size if there is no layout for this widget, 
        #         and returns the layout's minimum size otherwise. Most built-in widgets reimplement minimumSizeHint().
        return QSize(400,400)

    def sizeHint(self):
        # 具体用法和上面那个一样，如果这里不返回minSizeHINT，那么默认组件不会以最小值显示，如果在这里设置后，就会按这里的值进行设定。
        return self.minimumSizeHint()
        # return QSize(800,600)

    def mousePressEvent(self, event):
        side = min(self.height(),self.width())
        x_3 = side/3
        y_3 = side/3
        if event.x() < x_3:
            if event.y() < y_3:
                self.select = [0,0]
            elif event.y() < 2*y_3:
                self.select = [0,1]
            else:
                self.select = [0,2]
        elif event.x() < 2*x_3:
            if event.y() < y_3:
                self.select = [1,0]
            elif event.y() < 2*y_3:
                self.select = [1,1]
            else:
                self.select = [1,2]
        else:
            if event.y() < y_3:
                self.select = [2,0]
            elif event.y() < 2*y_3:
                self.select = [2,1]
            else:
                self.select = [2,2] 

        if self.grid[self.select[0]][self.select[1]] == BLANK:
            self.grid[self.select[0]][self.select[1]] = RED
        elif self.grid[self.select[0]][self.select[1]] == RED:
            self.grid[self.select[0]][self.select[1]] = YELLOW
        else:
            self.grid[self.select[0]][self.select[1]] = BLANK

        self.update()
            
    
    def paintEvent(self, event):
        logicalSize = 400
        x_3 = logicalSize/3
        y_3 = logicalSize/3
        x_a = logicalSize
        y_a = logicalSize
        painter = QPainter(self)
        painter.setWindow(0,0,logicalSize,logicalSize)
        side = min(self.width(),self.height())
        painter.setViewport((self.width()-side)/2,(self.height()-side)/2,side,side)
        painter.setRenderHint(QPainter.Antialiasing,True)
        for x in range(3):
            for y in range(3):
                rect = QRectF(x_3*x,y_3*y,x_3,y_3).adjusted(0.5,0.5,-0.5,-0.5)
                color = self.grid[x][y]
                
                painter.save()
                if color == RED:    
                    painter.setBrush(Qt.red)
                elif color == YELLOW:
                    painter.setBrush(Qt.yellow)
                else:
                    painter.setBrush(Qt.NoBrush)
                painter.setPen(Qt.black)
                painter.drawEllipse(rect.adjusted(2,2,-2,-2))
                painter.restore()
                if [x,y] == self.select:
                    painter.setPen(QPen(Qt.blue,3))
                else:
                    painter.setPen(Qt.black)
                painter.drawRect(rect)
        # self.resize(self.width(),self.width())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Counters()
    form.setWindowTitle("Counter by Corkine")
    form.show()
    app.exec_()