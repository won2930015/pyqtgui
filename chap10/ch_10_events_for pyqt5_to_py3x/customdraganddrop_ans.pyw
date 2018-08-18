#!/usr/bin/env python3
'''这是一个展示PyQt 5 Drag和 Drop能力的展示程序
Written by Corkine Ma (cm@marvinstudio.cn)
'''

import sys,os,traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CMDropLineEdit(QLineEdit):
    
    def __init__(self, parent=None):
        super(CMDropLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)
        # self.setDragEnabled(True) # 即便设置为True也无法拖拽


    def dragEnterEvent(self, event):
        # This event handler is called when a drag is in progress and the mouse enters this widget. The event is passed in the event parameter.
        # If the event is ignored, the widget won't receive any drag move events.
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        # 当用户在窗口上拖拽别的东西移动到想要drop的LineEdit的函数，设置拷贝策略
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # 此函数为拖拽到其上的处理方法，包括设置Copy策略，判断mimedata数据类型，从中读取数据设为stream并且读取text数据返回
        # event.mimeData()返回一个QMimeData()类型
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            data = event.mimeData().data("application/x-cm-96-data")
            stream = QDataStream(data,QIODevice.ReadOnly)
            text=''
            text = stream.readQString()
            self.setText(text)
            event.setDropAction(Qt.CopyAction) # 这里还要重新设置，不能因为在dragmove中设置过？？？？？？？？？？
            # 此外还有MoveAction LinkAction 等
            event.accept()
        else:
            event.ignore()

class CMDropListWidget(QListWidget):
    
    def __init__(self, parent=None):
        super(CMDropListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        # This event handler is called when a drag is in progress and the mouse enters this widget. The event is passed in the event parameter.
        # If the event is ignored, the widget won't receive any drag move events.
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        # 当用户在窗口上拖拽别的东西移动到想要drop的LineEdit的函数，设置拷贝策略
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        
        # 此函数为拖拽到其上的处理方法，包括设置Copy策略，判断mimedata数据类型，从中读取数据设为stream并且读取text数据返回
        # event.mimeData()返回一个QMimeData()类型
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            data = event.mimeData().data("application/x-cm-96-data")
            stream = QDataStream(data,QIODevice.ReadOnly)
            text=''
            icon = QIcon()
            text = stream.readQString()
            stream >> icon



            menu2 = QMenu()
            myCopyAction = menu2.addAction("&Copy")
            myMoveAction = menu2.addAction("&Move")
            myCopyAction.triggered.connect(self.setCopyAction)
            myMoveAction.triggered.connect(self.setMoveAction)
            
            if menu2.exec_(QCursor.pos()):
                item = QListWidgetItem(text,self) #???????????????
                item.setIcon(icon)
                event.setDropAction(self.dropAction)
                event.accept()
                return
            else:
                event.setDropAction(Qt.IgnoreAction)
        else:
            event.ignore()

    def setCopyAction(self):
        self.dropAction = Qt.CopyAction

    def setMoveAction(self):
        self.dropAction = Qt.MoveAction

    def startDrag(self,dropActions): 
        # Starts a drag by calling drag->exec() using the given supportedActions.
        # 是一个默认的原始函数，不需要调用即可使用
        # 对于不支持拖拽出去的组件，继承自QWidght，必须使用startDrag实例化一个QDrag对象，并且保证在合适的时候调用这个方法，比如，mouseMoveEvent（按钮按下才移动！！）
        item = self.currentItem() # 不用检查这个值，因为只要开始拖动，就必定是个元素
        icon = item.icon()

        # 声明一个字节文件，以及data流，将icon和text写入流
        data = QByteArray()
        stream = QDataStream(data,QIODevice.WriteOnly)
        stream.writeQString(item.text())
        stream << icon 
        
        # 将data写入到mimedata实例，mimedata不需要声明父类，类型为自定义类型
        mimeData = QMimeData()
        mimeData.setData("application/x-cm-96-data",data)

        # 写入mimedata到一个声明好的属于此widght的drag实例
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        
        # 控制外在表现
        pixmap=icon.pixmap(24,24)
        drag.setHotSpot(QPoint(12,12)) #设置图标的热点，一般来说和鼠标热点重合
        drag.setPixmap(pixmap) # 设置拖拽显示的那个图片
        
        # drag.start()/exec_()的调用会引发拖拽操作，可以将多个动作作为参数传递给它，如果拖拽成功，则返回发生的动作
        if drag.exec_(Qt.MoveAction|Qt.CopyAction) == Qt.MoveAction: # 如果取消掉actions只学moveaction，即便
        # 设定copy的menu菜单，但是系统依然只会move，因为在drag的命令中只有move，此事件最后执行，因此会覆盖之前的dropevent设置
            self.takeItem(self.row(item)) 

            
    # def mouseMoveEvent(self,event):
        
    #     self.startDrag()
    #     QWidget.mouseMoveEvent(self,event)
class CMCtrlDropListWidget(QListWidget):
    
    def __init__(self, parent=None):
        super(CMCtrlDropListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    # def keyPressEvent(self, event): # 在这里设置是无效的，因为这个时候已经开始拖拽了，所以需要在drag和drop的事件中判断
    #     if event.modifiers() and Qt.ControlModifier:
    #         print("123")
            
    #         return self.setCopyAction()
    #     else:
    #         QWidget.keyPressEvent(self,event)

    def dragEnterEvent(self, event):
        # Inherits: QDragMoveEvent
        # The drag enter event is always immediately followed by a drag move event.
        # This event handler is called when a drag is in progress and the mouse enters this widget. The event is passed in the event parameter.
        # If the event is ignored, the widget won't receive any drag move events.
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        # Inherits by QDropEvent
        # 当用户在窗口上拖拽别的东西移动到想要drop的LineEdit的函数，设置拷贝策略
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            if event.keyboardModifiers() & Qt.ControlModifier:
                event.setDropAction(Qt.CopyAction)
            else:
                event.setDropAction(Qt.MoveAction)
            # event.setDropAction(Qt.MoveAction) # 如果这里设置move，dropevent设置判断ctrl的话，按照时间顺序，dropevent先开始，但是
            # dropevent最后结束，因此其结果被dropevent覆盖。
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event): # 额u过遇到Event，则需要执行事件，所以必须有返回值
        # 其会影响到别人拖放到这个组件上的行为，而不是拖放出去的行为
        # 此函数为拖拽到其上的处理方法，包括设置Copy策略，判断mimedata数据类型，从中读取数据设为stream并且读取text数据返回
        # event.mimeData()返回一个QMimeData()类型
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            # if event.keyboardModifiers() & Qt.ControlModifier:
            #     event.setDropAction(Qt.CopyAction)
            # else:
            #     event.setDropAction(Qt.MoveAction)
            # event.setDropAction(Qt.MoveAction) 
            # 如果这里没有设置move，而是默认，则dragmoveevent中的选项会覆盖设置（时间在后）
            # 如果这里设置了dropaction为move，则即便是dragmoveevent中再进行设置也改变不了exec的结果
            # 上一个问题的原因可能是：dropevent虽然和dragmoveevent是父子关系，但是没有复写设置(像python)，
            # 其由drag开始到drag.exec结束，在这个过程中，dropevent持续时间和其两个子类（dragmoveevent）一样长，
            # 因此没有进行子对父的覆盖，详见400行的图
            data = event.mimeData().data("application/x-cm-96-data")
            stream = QDataStream(data,QIODevice.ReadOnly)
            text=''
            icon = QIcon()
            text = stream.readQString()
            stream >> icon
            
            item = QListWidgetItem(text,self) #???????????????
            item.setIcon(icon)
            event.accept()
        else:
            event.ignore()

    def setCopyAction(self):
        self.dropAction = Qt.CopyAction


    def startDrag(self,dropActions): # 照这个dropactions参数哪里用到了？？？？？？？？？？？？？？？
        # Starts a drag by calling drag->exec() using the given supportedActions.
        # 对于不支持拖拽出去的组件，继承自QWidght，必须使用startDrag实例化一个QDrag对象，并且保证在合适的时候调用这个方法，比如，mouseMoveEvent（按钮按下才移动！！）
        item = self.currentItem() # 不用检查这个值，因为只要开始拖动，就必定是个元素
        icon = item.icon()

        # 声明一个字节文件，以及data流，将icon和text写入流
        data = QByteArray()
        stream = QDataStream(data,QIODevice.WriteOnly)
        stream.writeQString(item.text())
        stream << icon 
        
        # 将data写入到mimedata实例，mimedata不需要声明父类，类型为自定义类型
        mimeData = QMimeData()
        mimeData.setData("application/x-cm-96-data",data)

        # 写入mimedata到一个声明好的属于此widght的drag实例
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        
        # 控制外在表现
        pixmap=icon.pixmap(24,24)
        drag.setHotSpot(QPoint(12,12)) #设置图标的热点，一般来说和鼠标热点重合
        drag.setPixmap(pixmap) # 设置拖拽显示的那个图片
        
        # drag.start()/exec_()的调用会引发拖拽操作，可以将多个动作作为参数传递给它，如果拖拽成功，则返回发生的动作
        if drag.exec_(Qt.MoveAction|Qt.CopyAction) == Qt.MoveAction: # 如果取消掉actions只学moveaction，即便
        # 设定copy的menu菜单，但是系统依然只会move，因为在drag的命令中只有move，此事件最后执行，因此会覆盖之前的dropevent设置
            self.takeItem(self.row(item)) 

            
    # def mouseMoveEvent(self,event):
        
    #     self.startDrag()
    #     QWidget.mouseMoveEvent(self,event)


class CMDropWidget(QWidget):
    
    def __init__(self, text, icon=QIcon(), parent=None):
        super(CMDropWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.text = str(text)
        self.icon = icon

    def minimumSizeHint(self):
        # This property holds the recommended minimum size for the widget
        fm = QFontMetricsF(self.font())
        # QFontMetricsF functions calculate the size of characters and strings for a given font. 
        # You can construct a QFontMetricsF object with an existing QFont to obtain metrics for that font. 
        # If the font is changed later, the font metrics object is not updated.
        if self.icon.isNull():
            return QSize(fm.width(self.text), fm.height() * 1.5)
        return QSize(34 + fm.width(self.text), max(34, fm.height() * 1.5))
        
    def paintEvent(self, event):
        height = QFontMetricsF(self.font()).height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) #Indicates that the engine should antialias edges of primitives if possible.
        painter.setRenderHint(QPainter.TextAntialiasing) # 字体抗锯齿
        painter.fillRect(self.rect(),QColor(Qt.yellow).lighter()) #Fills the given rectangle with the brush specified.
        if self.icon.isNull():
            painter.drawText(10,height,self.text)
        else:
            pixmap = self.icon.pixmap(24,24)
            painter.drawPixmap(0,5,pixmap) #QPainter::drawPixmap(int x, int y, const QPixmap &pixmap
            painter.drawText(34,height,self.text+"(继续扔！！！)")


    def dragEnterEvent(self, event):
        # This event handler is called when a drag is in progress and the mouse enters this widget. The event is passed in the event parameter.
        # If the event is ignored, the widget won't receive any drag move events.
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        # 当用户在窗口上拖拽别的东西移动到想要drop的LineEdit的函数，设置拷贝策略
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # 此函数为拖拽到其上的处理方法，包括设置Copy策略，判断mimedata数据类型，从中读取数据设为stream并且读取text数据返回
        # event.mimeData()返回一个QMimeData()类型
        if event.mimeData().hasFormat("application/x-cm-96-data"):
            data = event.mimeData().data("application/x-cm-96-data")
            stream = QDataStream(data,QIODevice.ReadOnly)
            self.text=''
            self.icon =QIcon()
            self.text = stream.readQString()
            stream >> self.icon


            event.setDropAction(Qt.CopyAction)
            event.accept()
            self.update() # This version updates a rectangle rect inside the widget.
            self.updateGeometry() # Notifies the layout system that this widget has changed and may need to change geometry.
        else:
            event.ignore()

    def startDrag(self): # 照这个dropactions参数哪里用到了？？？？？？？？？？？？？？？
        # Starts a drag by calling drag->exec() using the given supportedActions.
        # 对于不支持拖拽出去的组件，继承自QWidght，必须使用startDrag实例化一个QDrag对象，并且保证在合适的时候调用这个方法，比如，mouseMoveEvent（按钮按下才移动！！）
        icon = self.icon
        if icon.isNull():
            return 

        # 声明一个字节文件，以及data流，将icon和text写入流
        data = QByteArray()
        stream = QDataStream(data,QIODevice.WriteOnly)
        stream.writeQString(self.text)
        stream << icon 
        
        # 将data写入到mimedata实例，mimedata不需要声明父类，类型为自定义类型
        mimeData = QMimeData()
        mimeData.setData("application/x-cm-96-data",data)

        # 写入mimedata到一个声明好的属于此widght的drag实例
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        
        # 控制外在表现
        pixmap=icon.pixmap(24,24)
        drag.setHotSpot(QPoint(12,12)) #设置图标的热点，一般来说和鼠标热点重合
        drag.setPixmap(pixmap) # 设置拖拽显示的那个图片
        
        # drag.start()/exec_()的调用会引发拖拽操作，可以将多个动作作为参数传递给它，如果拖拽成功，则返回发生的动作
        drag.exec_(Qt.CopyAction)

    def mouseMoveEvent(self,event):
        
        self.startDrag()
        QWidget.mouseMoveEvent(self,event)

class Form(QDialog):
    def __init__(self,parent=None):
        super(Form,self).__init__(parent)

        # cmdropListWidget = CMDropListWidget()
        cmdropListWidget = CMDropListWidget()

        path = os.path.dirname(__file__)
        for image in sorted(os.listdir(os.path.join(path,"images"))):
            if image[-4:] == ".png":
                item = QListWidgetItem(image.split(".")[0].capitalize())
                item.setIcon(QIcon(os.path.join(path,"images/%s"%image)))
                cmdropListWidget.addItem(item)
        
        # cmIconListWidght = CMDropListWidget()
        cmIconListWidght = CMCtrlDropListWidget()
        cmIconListWidght.setViewMode(QListWidget.IconMode)

        cmDropWidget = CMDropWidget("扔到这里")

        cmDropLineEdit = CMDropLineEdit()

        layout = QGridLayout()
        layout.addWidget(cmdropListWidget,0,0)
        layout.addWidget(cmIconListWidght,0,1)
        layout.addWidget(cmDropWidget,1,0)
        layout.addWidget(cmDropLineEdit,1,1)
        self.setLayout(layout)

        self.setWindowTitle("自定义拖拽和放置示例程序")
    
if __name__=="__main__":

    app=QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()

        

'''

drag start —————————————————————————————EVENT——————————————————————————————————————————>drag end
drag.exec()-----event start--------------------------------dropEvent()----------------->Return Result
(在StartDtag()中对不能Drag的对象赋予Drag能力)
                               child event start  ---------dragMoveEvent()------------->
                                        (继承自dropEvent,但前者持续时间和自己一样长，因此不能覆盖设置)
                                       child event start ----dragEnterEvent()---------->
                                                            (继承自dropMoveEvent)

'''
