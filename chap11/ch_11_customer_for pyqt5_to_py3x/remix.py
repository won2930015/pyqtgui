#!/usr/bin/env python3

from PyQt5.QtCore import (QPointF, QSize, Qt,pyqtSignal)
from PyQt5.QtWidgets import (QApplication,
        QFrame, QLabel,
        QSizePolicy, QSpinBox, QWidget)
from PyQt5.QtGui import QColor,QPainter,QFontMetricsF,QBrush,QLinearGradient,QPolygon,QPolygonF

class YPipeWidget(QWidget):
    signal_valuechanged = pyqtSignal(int,int)
    def __init__(self, leftFlow=0, rightFlow=0, maxFlow=100,
                 parent=None):
        super(YPipeWidget, self).__init__(parent)

        self.leftSpinBox = QSpinBox(self) # 因为不会对其进行布局，所以使用self将其父声明为YPipeWidget
        self.leftSpinBox.setRange(0, maxFlow)
        self.leftSpinBox.setValue(leftFlow)
        self.leftSpinBox.setSuffix(" 升每秒")
        self.leftSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.leftSpinBox.valueChanged.connect(self.valueChanged)
        self.rightSpinBox = QSpinBox(self)
        self.rightSpinBox.setRange(0, maxFlow)
        self.rightSpinBox.setValue(rightFlow)
        self.rightSpinBox.setSuffix(" 升每秒")
        self.rightSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.rightSpinBox.valueChanged.connect(self.valueChanged)

        self.label = QLabel(self)
        self.label.setFrameStyle(QFrame.WinPanel|QFrame.Raised) #其接受两个对象，第一个是frame sharp，第二个是shadow style。
        self.label.setLineWidth(2)
        self.label.setAlignment(Qt.AlignCenter)
        fm = QFontMetricsF(self.font())
        self.label.setMinimumWidth(fm.width(" 666999 升每秒666 "))#设置下方最大宽度

        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding))
        self.setMinimumSize(self.minimumSizeHint())
        self.valueChanged()


    def valueChanged(self):
        a = self.leftSpinBox.value()
        b = self.rightSpinBox.value()
        self.label.setText("{0} 升每秒".format(a + b))
        self.signal_valuechanged.emit(a,b) # 这句话不影响结果，但是调用此函数valuechanged()会促使发射signal——valuechanged信号，这个信号包含
        # 两个参数，在最后和Form.valueChanged连接起来，方便调用程序进行判断。
        self.update()


    def values(self):
        return self.leftSpinBox.value(), self.rightSpinBox.value()


    def minimumSizeHint(self):
        return QSize(self.leftSpinBox.width() * 3,
                     self.leftSpinBox.height() * 5)

    # 对于任何没有绑定layout的组件来说，resizeEvent会自动调用，十分重要。  
    def resizeEvent(self, event=None):
        fm = QFontMetricsF(self.font())
        x = (self.width() - self.label.width()) / 2
        y = self.height() - (fm.height() * 2)
        self.label.move(x, y)
        y = self.height() / 60.0
        x = (self.width() / 4.0) - self.leftSpinBox.width()
        self.leftSpinBox.move(x, y)
        x = self.width() - (self.width() / 4.0)
        self.rightSpinBox.move(x,y) # 左上角为（0，0）移动点以左上角为标准


    def paintEvent(self, event=None):
        LogicalSize = 100.0

        def logicalFromPhysical(length, side):
            return (length / side) * LogicalSize

        fm = QFontMetricsF(self.font())
        ymargin = ((LogicalSize / 30.0) +
                   logicalFromPhysical(self.leftSpinBox.height(),
                                       self.height()))
        ymax = (LogicalSize -
                logicalFromPhysical(fm.height() * 2, self.height()))
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
        painter.setRenderHint(QPainter.Antialiasing)
        side = min(self.width(), self.height())
        painter.setViewport((self.width() - side) / 2,
                            (self.height() - side) / 2, side, side)
        painter.setWindow(0, 0, LogicalSize, LogicalSize)

        painter.setPen(Qt.NoPen) # 因为不需要显示所有线条，因此最后进行绘制，这里写NoPen

        gradient = QLinearGradient(QPointF(0, 0),
                                         QPointF(0, 100))
        gradient.setColorAt(0, Qt.white)
        a = self.leftSpinBox.value()
        gradient.setColorAt(1, (Qt.red if a != 0 else Qt.white))
        painter.setBrush(QBrush(gradient)) # 其可以接受一个QColor对象，也可以接受一个QBrush实例。
        # QBrush可以接受QColor、QGlobalColor、QImage、gradient对象
        # painter.setBrush(Qt.red)
        painter.drawPolygon(QPolygonF([QPointF(ax, ay), QPointF(bx, by), QPointF(cx, cy), QPointF(ix, iy)]))

        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 100))
        # The QLinearGradient class is used in combination with QBrush to specify a linear gradient brush.
        # args(QPointF,QPointF): Constructs a linear gradient with interpolation area between the given start point and finalStop.

        gradient.setColorAt(0, Qt.white)
        # Creates a stop point at the given position with the given color. The given position must be in the range 0 to 1.

        b = self.rightSpinBox.value()
        gradient.setColorAt(1, (Qt.blue if b != 0
                                else Qt.white))
        painter.setBrush(QBrush(gradient))
        painter.drawPolygon(QPolygonF([QPointF(cx, cy), QPointF(dx, dy),QPointF(ex, ey),QPointF(fx, fy)]))

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
        painter.drawPolygon(QPolygonF(
                [QPointF(cx, cy),QPointF(fx, fy),QPointF(gx, gy), QPointF(hx, hy),QPointF(ix, iy)]))

        painter.setPen(Qt.black)
        painter.drawPolyline(QPolygonF([QPointF(ax, ay), QPointF(ix, iy),QPointF(hx, hy)]))
        painter.drawPolyline(QPolygonF([QPointF(gx, gy), QPointF(fx, fy), QPointF(ex, ey)]))
        painter.drawPolyline(QPolygonF([QPointF(bx, by), QPointF(cx, cy), QPointF(dx, dy)]))

if __name__ == "__main__":
    import sys

    def valueChanged(a, b):
        print(a, b)

    app = QApplication(sys.argv)
    form = YPipeWidget()
    form.signal_valuechanged.connect(valueChanged)
    form.setWindowTitle("YPipe液体混合器")
    form.move(0, 0)
    form.show()
    form.resize(400, 400)
    app.exec_()