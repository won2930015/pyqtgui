#!/usr/bin/env python3
'''
实现难点：
1、滑块定位问题
2、Painter绘制问题
3、跨系统兼容问题
'''
import platform
from PyQt5.QtCore import (QPointF, QRectF, QSize, Qt,pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QDialog,QSizePolicy,
         QGridLayout, QLCDNumber, QLabel,
        QSpinBox, QWidget)
from PyQt5.QtGui import QColor,QFont,QPainter,QFontMetricsF,QPalette, QPolygonF
# linux X11兼容性代码判断
X11 = True
try:
    from PyQt5.QtGui import qt_x11_wait_for_window_manager
except ImportError:
    X11 = False


class FractionSlider(QWidget):

    XMARGIN = 12.0
    YMARGIN = 5.0
    WSTRING = "999" # 一个表示每个字母宽度的固定值，用在fm.width()中
    # 重写信号，接受或者传递两个参数
    valueChanged = pyqtSignal(int,int)  
    # 接受两个参数，分子和分母，初始化要求对其赋有默认值
    def __init__(self, numerator=0, denominator=10, parent=None):
        super(FractionSlider, self).__init__(parent)
        self.__numerator = numerator
        self.__denominator = denominator
        self.setFocusPolicy(Qt.WheelFocus)
        # 据说最强大的一个Focus类型，不论是窗口被切换、按键还是滚轮都可以被激活。激活此部件
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                       QSizePolicy.Fixed))


    def decimal(self):
        '''分子除分母，得出一个浮点数,用于显示'''
        return self.__numerator / float(self.__denominator)


    def fraction(self):
        '''返回一个元组，两个元素分别是分子和分母'''
        return self.__numerator, self.__denominator


    def sizeHint(self):
        '''默认Size策略，导向到minimumSizeHint'''
        return self.minimumSizeHint()


    def minimumSizeHint(self):
        '''定义字体、字体大小、根据字体Metrics的大小返回一个QSize对象，设置最小的尺寸'''
        font = QFont(self.font()) # 这声明了和没有声明有什么区别？Constructs a font that is a copy of font.
        # self.font() This property describes the widget's requested font.
        # font = QFont() # 只需要一个实例，因为此函数的目的是返回一个QSize
        font.setPointSize(font.pointSize() - 1) # The point size must be greater than zero. 
        # pointSize() Returns -1 if the font size was specified in pixels.
        fm = QFontMetricsF(font) 
        # print(fm.height(),fm.width(FractionSlider.WSTRING),fm.width(FractionSlider.WSTRING+'666')) # Return 11.0 18.0 36.0
        return QSize(fm.width(FractionSlider.WSTRING) *
                     self.__denominator,
                     (fm.height() * 4) + FractionSlider.YMARGIN)
        # fm.width(self,str) Returns the width in pixels of the characters in the given text.
        # fm.height(self) Returns the height of the font. 这个和qWidget无关，只是这个字体的高度，一般来说一个字母的高度为11.0，宽度6.0。


    def setFraction(self, numerator, denominator=None):
        '''用于接收分子和分母的数值，并且对其进行判断，如果不合要求(超出范围)，则抛出异常，否则，更新画布并且重设窗口大小'''
        if denominator is not None:
            if 3 <= denominator <= 60:
                self.__denominator = denominator
            else:
                raise ValueError("denominator out of range")
        if 0 <= numerator <= self.__denominator:
            self.__numerator = numerator
        else:
            raise ValueError("numerator out of range")
        self.update()
        self.updateGeometry()


    def mousePressEvent(self, event):
        '''对应实现在滑块上点击即可跳转的功能'''
        if event.button() == Qt.LeftButton:
            self.moveSlider(event.x())
            event.accept()
        else:
            QWidget.mousePressEvent(self, event)


    def mouseMoveEvent(self, event):
        '''对应实现鼠标左键点击并且滑动实现滑块跳转的功能'''
        # self.setMouseTracking(True)
        self.moveSlider(event.x())


    def moveSlider(self, x):
        '''给予一个移动距离的参数，更新滑块并且更新现在的参数'''
        span = self.width() - (FractionSlider.XMARGIN * 2) # 计算出尺子的总长度
        offset = span - x + FractionSlider.XMARGIN # 剩余的尺子的长度
        numerator = int(round(self.__denominator * 
                        (1.0 - (offset / span)))) # 已用尺子的长度 = 格子数目 * 已用尺子的百分比
        numerator = max(0, min(numerator, self.__denominator))
        if numerator != self.__numerator:
            self.__numerator = numerator
            #self.emit(SIGNAL("valueChanged(int,int)"),
            #         self.__numerator, self.__denominator)
            self.valueChanged.emit(self.__numerator, self.__denominator) # 信号绑定 重新传入的时候改变并触发
            self.update()


    def keyPressEvent(self, event):
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
                #self.emit(SIGNAL("valueChanged(int,int)"),
                #          self.__numerator, self.__denominator)
                self.valueChanged.emit(self.__numerator, self.__denominator)
                self.update()
            event.accept()
        else:
            QWidget.keyPressEvent(self, event)


    def paintEvent(self, event=None):
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        # Returns -1 if the font size was specified in pixels.
        fm = QFontMetricsF(font)
        fracWidth = fm.width(FractionSlider.WSTRING) # 一个字母所占的宽度
        indent = fm.boundingRect("9").width() / 2.0 # 半个字母的宽度
        # Returns the bounding rectangle of the characters in the string specified by text. 
        if not X11:
            fracWidth *= 1.5
        span = self.width() - (FractionSlider.XMARGIN * 2) # 尺子的宽度
        value = self.__numerator / float(self.__denominator) # 当前滑块的值

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # 设置抗锯齿
        painter.setRenderHint(QPainter.TextAntialiasing) # 设置字体抗锯齿
        painter.setPen(self.palette().color(QPalette.Midlight)) # setPen 可以接受Pen、PenStyle、Color对象 这里指的是Color
        # painter.setPen(QColor(220,100,100)) # 这里设置的是QWidght的边框
        painter.setBrush(self.palette().brush(
                QPalette.AlternateBase))
        # setBrush() : Sets the brush for the given color role to the specified brush for all groups in the palette.
        # [Color Role] QPalette.AlternateBase : Used as the alternate background color in views with alternating row colors
        # self.palette() This property holds the widget's palette 其会和默认的调色版混合呈现，但是其一般不能传递到窗口，需要特殊设置，推荐使用CSS 
        painter.drawRect(self.rect())
        segColor = QColor(Qt.gray).lighter(80) # 尺度条颜色:lighter(factor) 150表示50%亮，对于darker(factor) 300表示3倍暗
        segLineColor = segColor.darker() # 默认200 lighter默认 150
        painter.setPen(segLineColor)
        painter.setBrush(segColor)
        painter.drawRect(FractionSlider.XMARGIN,
                         FractionSlider.YMARGIN, span, fm.height())
        textColor = self.palette().color(QPalette.Text)
        segWidth = span / self.__denominator
        segHeight = fm.height() * 2
        nRect = fm.boundingRect(FractionSlider.WSTRING)
        x = FractionSlider.XMARGIN
        yOffset = segHeight + fm.height()
        for i in range(self.__denominator + 1):
            painter.setPen(segLineColor) # 设置线的颜色作为Pen
            painter.drawLine(x, FractionSlider.YMARGIN, x, segHeight) # 划竖线，从（x，ymargin）开始，到（x，segheight）为止。
            painter.setPen(textColor)
            y = segHeight
            rect = QRectF(nRect)
            rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
            #painter.drawText(rect, Qt.AlignCenter,
                             #QString.number(i))
            painter.drawText(rect, Qt.AlignCenter,str(i))            
            y = yOffset
            rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
            painter.drawText(rect, Qt.AlignCenter,
                             str(self.__denominator))
            painter.drawLine(QPointF(rect.left() + indent, y),
                             QPointF(rect.right() - indent, y))
            x += segWidth
        span = int(span)
        y = FractionSlider.YMARGIN - 0.5
        triangle = [QPointF(value * span, y),
                    QPointF((value * span) +
                            (2 * FractionSlider.XMARGIN), y),
                    QPointF((value * span) +
                            FractionSlider.XMARGIN, fm.height())]
        triangledict = (QPointF(value * span, y),
                    QPointF((value * span) +
                            (2 * FractionSlider.XMARGIN), y),
                    QPointF((value * span) +
                            FractionSlider.XMARGIN, fm.height()))
        painter.setPen(QColor(Qt.yellow).darker(100))
        # painter.setBrush(Qt.darkYellow)
        painter.setBrush(QColor(Qt.yellow).darker(200))
        painter.drawPolygon(QPolygonF(triangle))
        # painter.drawPolygon(triangledict,3) # 不可行，因为第一个参数必须接受QPoint，而这种类型在PyQt中不支持。

        # The first point is implicitly connected to the last point, and the polygon is filled with the current brush().
        # void QPainter::drawPolygon(const QPolygonF &points, Qt::FillRule fillRule = Qt::OddEvenFill)
        # void QPainter::drawPolygon(const QPoint *points, int pointCount, Qt::FillRule fillRule = Qt::OddEvenFill)
        # QPolygonF接受QPointF对象，在PyQt中传入了三个QPointF对象，使用了一个迭代的列表写入到QPolygonF中。


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = QDialog()
    sliderLabel = QLabel("&Fraction")
    slider = FractionSlider(denominator=12)
    sliderLabel.setBuddy(slider)
    denominatorLabel = QLabel("&Denominator")
    denominatorSpinBox = QSpinBox()
    denominatorLabel.setBuddy(denominatorSpinBox)
    denominatorSpinBox.setRange(3, 60)
    denominatorSpinBox.setValue(slider.fraction()[1])
    denominatorSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
    numeratorLabel = QLabel("Numerator")
    numeratorLCD = QLCDNumber()
    numeratorLCD.setSegmentStyle(QLCDNumber.Flat)
    layout = QGridLayout()
    layout.addWidget(sliderLabel, 0, 0)
    layout.addWidget(slider, 0, 1, 1, 5)
    layout.addWidget(numeratorLabel, 1, 0)
    layout.addWidget(numeratorLCD, 1, 1)
    layout.addWidget(denominatorLabel, 1, 2)  
    layout.addWidget(denominatorSpinBox, 1, 3)
    form.setLayout(layout)

    def valueChanged(denominator):
        numerator = int(slider.decimal() * denominator)
        slider.setFraction(numerator, denominator)
        numeratorLCD.display(numerator)

    #form.connect(slider, SIGNAL("valueChanged(int,int)"),
                 #numeratorLCD, SLOT("display(int)"))
    slider.valueChanged[int,int].connect(numeratorLCD.display) # 滑块的更改的自定义valueChanged Singal传递给显示器显示，这时候不涉及分数改变，因此不用重设doubelspinbox
    #form.connect(denominatorSpinBox, SIGNAL("valueChanged(int)"),
                 #valueChanged)
    denominatorSpinBox.valueChanged[int].connect(valueChanged) # 选择分数的默认valueChanged Singal 传递给valueChanged函数，此函数设置滑块和显示器
    form.setWindowTitle("Fraction Slider")
    form.show()
    app.exec_()