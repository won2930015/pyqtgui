#!/usr/bin/env python3
'''这是一个关于PyQt事件函数的实例程序
Written by Corkine Ma (cm@marvinstudio.cn)
'''
import sys,traceback
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class Form(QWidget):
    def __init__(self,parent=None):
        super(Form,self).__init__(parent)
        self.haveDoubleChecked=False
        self.key=''
        self.message=''
        self.text=''
        self.setWindowTitle("PyQt5 Events Example")
    
    def closeEvent(self,event):
        print("这是关闭窗口前的提示")

    def mouseDoubleClickEvent(self,event):
        self.haveDoubleChecked=True
        self.text="你刚才双击了鼠标/TrackPad"
        self.update()
        # This is an overloaded function. This version updates a rectangle rect inside the widget.

    def contextMenuEvent(self,event):
        menu1=QMenu()
        oneAction=menu1.addAction("&One")
        twoAction=menu1.addAction("&Two")
        oneAction.triggered.connect(self.one)
        twoAction.triggered.connect(self.two)
        if not self.message:
            menu1.addSeparator()
            threeAction=menu1.addAction("&Three")
            threeAction.triggered.connect(self.three)
        menu1.exec_(event.globalPos()) # 这个是必须的，否则不会显示上下文菜单

    def one(self):
        self.message = "上下文菜单One"
        self.update()

    def two(self):
        self.message = "上下文菜单Two"
        self.update()

    def three(self):
        self.message = "上下文菜单Three!"
        self.update()

    def mouseMoveEvent(self,event):
        # If mouse tracking is switched off, mouse move events only occur if a mouse button is pressed while the mouse is being moved. 
        # If mouse tracking is switched on, mouse move events occur even if no mouse button is pressed.

        if not self.haveDoubleChecked:
            globalPos=self.mapToGlobal(event.pos()) # 返回值是QPoint()因此，没有event中的pos属性，只有QPoint的x()和y()的属性
            self.text="窗口的鼠标坐标：%d,%d\n桌面的鼠标坐标：%d,%d"%(event.pos().x(),event.pos().y(),globalPos.x(),globalPos.y())
        self.update()
        # except:
        #     QMessageBox.warning(self,"WARN",traceback.format_exc())

    def mouseReleaseEvent(self,event):
        if self.haveDoubleChecked:
            self.haveDoubleChecked =False
        else:
            self.setMouseTracking(not self.hasMouseTracking()) # 为什么切换不了到关闭鼠标追踪呢？
            if self.hasMouseTracking():
                self.text="鼠标追踪已打开\n按住鼠标左键并且移动鼠标试试\n单击鼠标关闭鼠标追踪"
            else:
                self.text="鼠标追踪已关闭\n按住鼠标左键并且移动鼠标试试\n单击鼠标打开鼠标追踪"
            self.update()

    def paintEvent(self,event): # 这个东西恐怕是会在__init__之后，生成画面之前触发运行，因此可以使用self.update()更新rect
        text=self.text
        if self.key:
            text+="\n\n按下了按键 %s"%(str(self.key))
        painter=QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        # 平滑字体，设置painter的renderhint
        painter.drawText(self.rect(),Qt.AlignCenter,text)
        # Draws the given text within the provided rectangle. The rectangle along with alignment flags defines the anchors for the text.
        # Qrect: This property holds the internal geometry of the widget excluding any window frame
        if self.message:
            painter.drawText(self.rect(),Qt.AlignBottom|Qt.AlignHCenter,self.message)
            QTimer.singleShot(5000,self.messageClear)
            QTimer.singleShot(5000,self.update)

    def messageClear(self):
        self.message=''

    def keyPressEvent(self,event):
        self.key=''
        if event.key() == Qt.Key_Home:
            self.key="Home"
        elif event.key() == Qt.Key_End:
            self.key="End"
        elif event.key() == Qt.Key_PageUp:
            if event.modifiers() & Qt.ControlModifier:
                # 这个就是 event.modifiers() == Qt.ControlModifier, 取共集，判断bool值
                self.key="Ctrl+PageUp"
            else:
                self.key="PageUp"
        elif Qt.Key_A <= event.key() <= Qt.Key_Z: # 这是一个很有趣的表示方法,不能够写=> 只能写 <= 比如下面一句不能执行
        # elif Qt.Key_Z => event.key() => Qt.Key_A:
        # elif Qt.Key_Z <= event.key() <= Qt.Key_A: # 同理，不能写成从A到Z，只能写成从Z到A，否则不会报错，但是，不会执行判断
            # if event.modifiers() & Qt.ShiftModifier:
            #     self.key="Shift+"
            #     if event.modifiers() & Qt.ControlModifier:
            #         self.key+="Ctrl+"
            #         if event.modifiers() & Qt.AltModifier:
            #             self.key+="Alt+"
            # else:
            #     if event.modifiers() & Qt.ControlModifier:
            #         self.key="Ctrl+"
            #         if event.modifiers() & Qt.AltModifier:
            #             self.key+="Alt+"
            #     elif event.modifiers() & Qt.AltModifier:
            #         self.key="Alt+"
            # self.realkey=event.text()
            if event.modifiers() & Qt.ShiftModifier:
                self.key="Shift+"
            # if event.modifiers() & Qt.ControlModifier:
            #     self.key="Ctrl+%s"%str(event.key())
            # 所有涉及Ctrl的部分都不能够检测到按键，可能是因为其和shotcut冲突。。。。。。。。。
            if event.modifiers() & Qt.AltModifier:
                self.key="Alt+"
            self.key+=event.text()
        if self.key:
            self.key=str(self.key)
            self.update()
        else:
            QWidget.keyPressEvent(self,event)

    def resizeEvent(self,event):
        self.text=str('窗口大小为：%d × %d'%(event.size().width(),event.size().height()))
        self.update() #为什么需要update？不需要也可以运行

    def event(self,event):
        # 调用这个函数的意义在于，比如像收集“Tab”这种event的时候，它会忽略捕获而转向下一个组件，正比如之前那个“ctrl”修饰按键，在基类进行捕获可以避免这种情况。
        if event.type()==QEvent.KeyPress and event.key()==Qt.Key_Tab:
            self.key="Tab" # 因为在printer中进行了绘制，因此写Tab就好
            self.update()
            return True # 返回任意一个东西都行，因为不返回的话，会卡在这里影响下一句QWidget的event数据处理。必须返回一个int或者bool值，推荐true
        # 返回True后就告诉自己的基类，这个事件已经被处理过，不需要继续处理。

        if event.type()==QEvent.KeyPress and Qt.Key_A <= event.key() <= Qt.Key_Z:
            if event.modifiers() & Qt.ControlModifier:
                print("AAAAA")
                self.key="Ctrl+%s"%event.key() #event.text()在这里依旧不能捕获内容，但是在前面的子event中就可以捕获。
                self.update()
                return True # 这里的ruturn到底要如何返回？？？？？？？？？？？？？？？？？
            # return False #如果这里ruturn t or f 都不能够对ctrl进行处理，系统在这里直接跳过if到达最后一句传递给自己的子类处理
        return QWidget.event(self,event) #传递给更高级的父组件进行处理
        # 如果调用了event函数而不进行返回，那么会报错：invalid result from Form.event(), an integer is required (got type NoneType)

if __name__=="__main__":
    app=QApplication(sys.argv)
    form=Form()
    form.show()
    app.exec_()