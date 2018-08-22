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

import functools  # 函数_工具
import random  # 随机
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

MAC = "qt_mac_set_native_menubar" in dir()

# PageSize = (595, 842)  # A4 in points
PageSize = (612, 792)  # US Letter in points
PointSize = 10

MagicNumber = 0x70616765  # 魔数号
FileVersion = 1  # 文件号

Dirty = False  # 修改标志


class TextItemDlg(QDialog):  # 自定义的文本项对话框...

    def __init__(self, item=None, position=None, scene=None, parent=None):  # 下面是完整的定义.
    # def __init__(self, item: object = None, scene: object = None, position: object = None, parent: object = None) -> object:
        super(QDialog, self).__init__(parent)

        self.item = item  # 项
        self.position = position  # 位置
        self.scene = scene  # 场景

        self.editor = QTextEdit()
        self.editor.setAcceptRichText(False)  # 设置_接受_富文本 =False
        self.editor.setTabChangesFocus(True)  # 设置_Tab_改变_焦点 =True
        editorLabel = QLabel("&Text:")
        editorLabel.setBuddy(self.editor)
        self.fontComboBox = QFontComboBox()     # 创建 字体复合选择框 实例.
        self.fontComboBox.setCurrentFont(QFont("宋体", PointSize))    # 设置_当前_字体
        fontLabel = QLabel("&Font:")
        fontLabel.setBuddy(self.fontComboBox)
        self.fontSpinBox = QSpinBox()
        self.fontSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)    # .setAlignment:设置对齐
        self.fontSpinBox.setRange(6, 280)
        self.fontSpinBox.setValue(PointSize)
        fontSizeLabel = QLabel("&Size:")
        fontSizeLabel.setBuddy(self.fontSpinBox)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|    # DialogButtonBox::对话框_按钮_盒.
                                          QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        if self.item is not None:
            self.editor.setPlainText(self.item.toPlainText())  # setPlainText:设置_纯_文本
            self.fontComboBox.setCurrentFont(self.item.font())
            self.fontSpinBox.setValue(self.item.font().pointSize())

        layout = QGridLayout()
        layout.addWidget(editorLabel, 0, 0)
        layout.addWidget(self.editor, 1, 0, 1, 6)
        layout.addWidget(fontLabel, 2, 0)
        layout.addWidget(self.fontComboBox, 2, 1, 1, 2)
        layout.addWidget(fontSizeLabel, 2, 3)
        layout.addWidget(self.fontSpinBox, 2, 4, 1, 2)
        layout.addWidget(self.buttonBox, 3, 0, 1, 6)
        self.setLayout(layout)

        self.connect(self.fontComboBox,
                SIGNAL("currentFontChanged(QFont)"), self.updateUi)  # 字体复合框字体改变时...
        self.connect(self.fontSpinBox,
                SIGNAL("valueChanged(int)"), self.updateUi)  # 字号改变时...
        self.connect(self.editor, SIGNAL("textChanged()"),
                     self.updateUi)  # 文本编辑框,文本改变时...
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)  # OK按钮被单击时...
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)  # Cancel按钮被单击时...

        self.setWindowTitle("Page Designer - {} Text Item".format(
                "Add" if self.item is None else "Edit"))
        self.updateUi()


    def updateUi(self):
        font = self.fontComboBox.currentFont()
        font.setPointSize(self.fontSpinBox.value())
        self.editor.document().setDefaultFont(font)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
                bool(self.editor.toPlainText()))


    def accept(self):
        if self.item is None:
            self.item = TextItem("", self.position, self.scene)
        font = self.fontComboBox.currentFont()
        font.setPointSize(self.fontSpinBox.value())
        self.item.setFont(font)
        self.item.setPlainText(self.editor.toPlainText())   
        self.item.update()
        global Dirty    # Dirty:脏的(本文修改标志)
        Dirty = True
        QDialog.accept(self)


class TextItem(QGraphicsTextItem):  # GraphicsTextItem::图形_文本_项.

    def __init__(self, text, position, scene,
                font=QFont("宋体", PointSize), matrix=QMatrix()):  # matrix:矩阵
        super(TextItem, self).__init__(text)
        self.setFlags(QGraphicsItem.ItemIsSelectable|  # setFlags:设置标志, .ItemIsSelectable::项是可选择的...,.
                      QGraphicsItem.ItemIsMovable)     # ItemIsMovable::项是可移动的...
        self.setFont(font)
        self.setPos(position)
        self.setMatrix(matrix)
        scene.clearSelection()  # 清除_选择.
        scene.addItem(self)
        self.setSelected(True)
        global Dirty
        Dirty = True


    def parentWidget(self):  # 返回::父_控件 P272
        return self.scene().views()[0]  # 返回场景第一个视图(view)


    def itemChange(self, change, variant):  # 与项进行交互[移动/选择],就会调用此方法.P272
        if change != QGraphicsItem.ItemSelectedChange:  # change(改变) != 选择_变化 时执行...
            global Dirty
            Dirty = True
        return QGraphicsTextItem.itemChange(self, change, variant)


    def mouseDoubleClickEvent(self, event):
        dialog = TextItemDlg(self, self.parentWidget())
        dialog.exec_()


class BoxItem(QGraphicsItem):

    def __init__(self, position, scene, style=Qt.SolidLine,  # SolidLine::实线
                 rect=None, matrix=QMatrix()):
        super(BoxItem, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable|   # 项_可_选择
                      QGraphicsItem.ItemIsMovable|      # 项_可_移动
                      QGraphicsItem.ItemIsFocusable)    # 项_可_焦点
        if rect is None:
            rect = QRectF(-10 * PointSize, -PointSize, 20 * PointSize,
                          2 * PointSize)
        self.rect = rect
        self.style = style
        self.setPos(position)
        self.setMatrix(matrix)
        scene.clearSelection()
        scene.addItem(self)
        self.setSelected(True)
        self.setFocus()
        global Dirty
        Dirty = True


    def parentWidget(self):  # 返回父控件
        return self.scene().views()[0]  # 返回场景第一个视图.(view)


    def boundingRect(self):  # 边界框_矩形.
        return self.rect.adjusted(-2, -2, 2, 2)  # adjusted::调整


    def paint(self, painter, option, widget):
        pen = QPen(self.style)
        pen.setColor(Qt.black)
        pen.setWidth(1)
        if option.state & QStyle.State_Selected:  # 当option.state==选中状态(State_Selected) 时...
            pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawRect(self.rect)


    def itemChange(self, change, variant):  # 与项进行交互[移动/选择],就会调用些方法.
        if change != QGraphicsItem.ItemSelectedChange:  # 改变 != 选择改变 时执行.
            global Dirty
            Dirty = True
        return QGraphicsItem.itemChange(self, change, variant)


    def contextMenuEvent(self, event):  # 上下文菜单.
        wrapped = []
        menu = QMenu(self.parentWidget())
        for text, param in (
                ("&Solid", Qt.SolidLine),  # 实线
                ("&Dashed", Qt.DashLine),  # 破折线  _ _ _
                ("D&otted", Qt.DotLine),   # 点线  ...
                ("D&ashDotted", Qt.DashDotLine),  # 破折点线  _._._.
                ("DashDo&tDotted", Qt.DashDotDotLine)):  # 破折点点线  _.._.._..
            wrapper = functools.partial(self.setStyle, param)  # 偏函数:.partial(函数(), 参数1,参数2,...)
            wrapped.append(wrapper)
            menu.addAction(text, wrapper)
        menu.exec_(event.screenPos())  # event.screenPos()::事件.屏幕坐标点


    def setStyle(self, style):
        self.style = style
        self.update()
        global Dirty
        Dirty = True


    def keyPressEvent(self, event):
        factor = PointSize / 4  # factor::因数
        changed = False
        if event.modifiers() & Qt.ShiftModifier:  # event.modifiers():功能键被按下时->True,   Qt.ShiftModifier:Shift键被按下时->True
            if event.key() == Qt.Key_Left:  # ←键
                self.rect.setRight(self.rect.right() - factor)
                changed = True
            elif event.key() == Qt.Key_Right:   # →键
                self.rect.setRight(self.rect.right() + factor)
                changed = True
            elif event.key() == Qt.Key_Up:  # ↑键
                self.rect.setBottom(self.rect.bottom() - factor)
                changed = True
            elif event.key() == Qt.Key_Down:    # ↓键
                self.rect.setBottom(self.rect.bottom() + factor)
                changed = True
        if changed:
            self.update()
            global Dirty
            Dirty = True
        else:  # 除 SHIFT+ ↑↓←→按键事件外,所有keyPressEvent由父类QGraphicsItem.keyPressEvent()处理.
            QGraphicsItem.keyPressEvent(self, event)


class GraphicsView(QGraphicsView):  # 自定义 图形视图 类.

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)  # setDragMode::设置_拖拽_模式, RubberBandDrag::拖动时显示 橡皮筋边框
        self.setRenderHint(QPainter.Antialiasing)  # RenderHint::渲染_提示
        self.setRenderHint(QPainter.TextAntialiasing)

    # 鼠标滚轮事件.
    def wheelEvent(self, event):
        factor = 1.41 ** (-event.delta() / 240.0)   # delta:增量
        self.scale(factor, factor)


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.filename = ""
        self.copiedItem = QByteArray()  # copiedItem:复制_项
        self.pasteOffset = 5  # 粘贴_偏移
        self.prevPoint = QPoint()  # 前一个_节点
        self.addOffset = 5  # 加入_偏移
        self.borders = []  # 边框??

        self.printer = QPrinter(QPrinter.HighResolution)  # .HighResolution:高分辨率
        self.printer.setPageSize(QPrinter.Letter)

        self.view = GraphicsView()  # 创建视图对象.
        self.scene = QGraphicsScene(self)  # 创建场景
        self.scene.setSceneRect(0, 0, PageSize[0], PageSize[1])  # 设置场景范围.
        self.addBorders()  # 加入边界
        self.view.setScene(self.scene)

        buttonLayout = QVBoxLayout()
        for text, slot in (
                ("Add &Text", self.addText),
                ("Add &Box", self.addBox),
                ("Add Pi&xmap", self.addPixmap),
                ("&Copy", self.copy),
                ("C&ut", self.cut),
                ("&Paste", self.paste),
                ("&Delete...", self.delete),
                ("&Rotate", self.rotate),
                ("Pri&nt...", self.print_),
                ("&Open...", self.open),
                ("&Save", self.save),
                ("&Quit", self.accept)):
            button = QPushButton(text)
            if not MAC:
                button.setFocusPolicy(Qt.NoFocus)
            self.connect(button, SIGNAL("clicked()"), slot)
            if text == "Pri&nt...":
                buttonLayout.addStretch(5)  # 加入长度5的拉伸.
            if text == "&Quit":
                buttonLayout.addStretch(1)  # 加入长度1的拉伸.
            buttonLayout.addWidget(button)
        buttonLayout.addStretch()

        layout = QHBoxLayout()
        layout.addWidget(self.view, 1)  # 1 :代表可扩展的.
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        fm = QFontMetrics(self.font())  # FontMetrics::字体度量对象
        self.resize(self.scene.width() + fm.width(" Delete... ") + 50,
                    self.scene.height() + 50)
        self.setWindowTitle("Page Designer")

    # 加入边界线
    def addBorders(self):
        self.borders = []
        rect = QRectF(0, 0, PageSize[0], PageSize[1])
        self.borders.append(self.scene.addRect(rect, Qt.yellow))  # 页面大小指示线
        margin = 5.25 * PointSize
        self.borders.append(self.scene.addRect(
                rect.adjusted(margin, margin, -margin, -margin),
                Qt.yellow))  # 边距指示线


    def removeBorders(self):
        while self.borders:
            item = self.borders.pop()
            self.scene.removeItem(item)
            del item

        
    def reject(self):
        self.accept()


    def accept(self):
        self.offerSave()
        QDialog.accept(self)

    # 提议保存
    def offerSave(self):
        if (Dirty and QMessageBox.question(self,
                            "Page Designer - Unsaved Changes",
                            "Save unsaved changes?",
                            QMessageBox.Yes|QMessageBox.No) ==
            QMessageBox.Yes):
            self.save()


    def position(self):
        point = self.mapFromGlobal(QCursor.pos())   # 将光标当前位置坐标转换成物理坐标point.
        if not self.view.geometry().contains(point):    # geometry::几何图形,contains::包含, 当 视图.几何图形不包含point时执行...
            coord = random.randint(36, 144)
            point = QPoint(coord, coord)
        else:
            if point == self.prevPoint:
                point += QPoint(self.addOffset, self.addOffset)
                self.addOffset += 5
            else:
                self.addOffset = 5
                self.prevPoint = point
        return self.view.mapToScene(point)  # 将point物理坐标转换成Scene的逻辑坐标.


    def addText(self):
        dialog = TextItemDlg(position=self.position(),
                             scene=self.scene, parent=self)
        dialog.exec_()


    def addBox(self):
        BoxItem(self.position(), self.scene)


    def addPixmap(self):
        path = QFileInfo(self.filename).path() if self.filename else "."
        fname = QFileDialog.getOpenFileName(self,
                "Page Designer - Add Pixmap", path,
                "Pixmap Files (*.bmp *.jpg *.png *.xpm)")
        if not fname:
            return

        self.createPixmapItem(QPixmap(fname), self.position())

        # self.image=QImage()
        # self.image.load(fname)
        # self.createPixmapItem(QPixmap.fromImage(self.image), self.position())




    def createPixmapItem(self, pixmap, position, matrix=QMatrix()):

        # matrix.scale(0.8,0.8) #缩放图片http://www.voidcn.com/article/p-cwldonxv-er.html

        item = QGraphicsPixmapItem(pixmap)
        item.setFlags(QGraphicsItem.ItemIsSelectable|  # 可选择
                      QGraphicsItem.ItemIsMovable)  # 可移动
        item.setPos(position)
        item.setMatrix(matrix)  # QT4.3以后QMatrix()更名为QTranstform() http://blog.csdn.net/founderznd/article/details/51533777
        self.scene.clearSelection()
        self.scene.addItem(item)
        item.setSelected(True)
        global Dirty
        Dirty = True


    def selectedItem(self):
        items = self.scene.selectedItems()
        if len(items) == 1:
            return items[0]
        return None

    # 复制
    def copy(self):
        item = self.selectedItem()
        if item is None:
            return
        self.copiedItem.clear()
        self.pasteOffset = 5
        stream = QDataStream(self.copiedItem, QIODevice.WriteOnly)
        self.writeItemToStream(stream, item)  # 写项到→流::自定义函数方法.

    # 剪切
    def cut(self):
        item = self.selectedItem()
        if item is None:
            return
        self.copy()
        self.scene.removeItem(item)
        del item

    # 粘贴
    def paste(self):
        if self.copiedItem.isEmpty():
            return
        stream = QDataStream(self.copiedItem, QIODevice.ReadOnly)
        self.readItemFromStream(stream, self.pasteOffset)
        self.pasteOffset += 5

    # 旋转
    def rotate(self):
        for item in self.scene.selectedItems():
            item.rotate(30)

    # 删除
    def delete(self):
        items = self.scene.selectedItems()
        if (len(items) and QMessageBox.question(self,
                "Page Designer - Delete",
                "Delete {} item{}?".format(len(items),
                "s" if len(items) != 1 else ""),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
            while items:
                item = items.pop()
                self.scene.removeItem(item)
                del item
            global Dirty
            Dirty = True

    # 打印
    def print_(self):
        dialog = QPrintDialog(self.printer)
        if dialog.exec_():
            painter = QPainter(self.printer)  # 将绘图器初始化到打印机上.
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.TextAntialiasing)
            self.scene.clearSelection()
            self.removeBorders()
            self.scene.render(painter)  # render():渲染. PS:将 屏幕内容.渲染到[painter::绘图器]上→ 即打印输出屏幕内容.
            self.addBorders()


    def open(self):
        self.offerSave()
        path = QFileInfo(self.filename).path() if self.filename else "."
        fname = QFileDialog.getOpenFileName(self,
                "Page Designer - Open", path,
                "Page Designer Files (*.pgd)")
        if not fname:
            return
        self.filename = fname
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            items = self.scene.items()
            while items:
                item = items.pop()
                self.scene.removeItem(item)
                del item
            self.addBorders()
            stream = QDataStream(fh)
            stream.setVersion(QDataStream.Qt_4_2)
            magic = stream.readInt32()
            if magic != MagicNumber:
                raise IOError("not a valid .pgd file")
            fileVersion = stream.readInt16()
            if fileVersion != FileVersion:
                raise IOError("unrecognised .pgd file version")
            while not fh.atEnd():
                self.readItemFromStream(stream)
        except IOError as e:
            QMessageBox.warning(self, "Page Designer -- Open Error",
                    "Failed to open {}: {}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        global Dirty
        Dirty = False


    def save(self):
        if not self.filename:
            path = "."
            fname = QFileDialog.getSaveFileName(self,
                    "Page Designer - Save As", path,
                    "Page Designer Files (*.pgd)")
            if not fname:
                return
            if not fname.lower().endswith(".pgd"):
                fname += ".pgd"
            self.filename = fname
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            self.scene.clearSelection()
            stream = QDataStream(fh)
            stream.setVersion(QDataStream.Qt_4_2)
            stream.writeInt32(MagicNumber)
            stream.writeInt16(FileVersion)
            for item in self.scene.items():
                self.writeItemToStream(stream, item)
        except IOError as e:
            QMessageBox.warning(self, "Page Designer -- Save Error",
                    "Failed to save {}: {}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        global Dirty
        Dirty = False


    def readItemFromStream(self, stream, offset=0):
        type = ""
        position = QPointF()
        matrix = QMatrix()
        type = stream.readQString()  # readQString()::读出一段字符串类型.
        stream >> position >> matrix
        if offset:
            position += QPointF(offset, offset)
        if type == "Text":
            text = stream.readQString()
            font = QFont()
            stream >> font
            TextItem(text, position, self.scene, font, matrix)
        elif type == "Box":
            rect = QRectF()
            stream >> rect
            style = Qt.PenStyle(stream.readInt16())
            BoxItem(position, self.scene, style, rect, matrix)
        elif type == "Pixmap":
            pixmap = QPixmap()
            stream >> pixmap
            self.createPixmapItem(pixmap, position, matrix)


    def writeItemToStream(self, stream, item):
        if isinstance(item, QGraphicsTextItem):
            stream.writeQString("Text")
            stream << item.pos() << item.matrix()
            stream.writeQString(item.toPlainText())
            stream << item.font()
        elif isinstance(item, QGraphicsPixmapItem):
            stream.writeQString("Pixmap")
            stream << item.pos() << item.matrix() << item.pixmap()
        elif isinstance(item, BoxItem):
            stream.writeQString("Box")
            stream << item.pos() << item.matrix() << item.rect
            stream.writeInt16(item.style)


app = QApplication(sys.argv)
form = MainForm()
rect = QApplication.desktop().availableGeometry()   # :获取桌面().availableGeometry可用_几何矩形.
form.resize(int(rect.width() * 0.6), int(rect.height() * 0.9))
form.show()
app.exec_()

