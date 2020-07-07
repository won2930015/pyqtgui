#!/usr/bin/env python
'''
这是新建图案窗口对话框，作者使用了UI布局，生成的布局在ui_newimagedlg.py文件中。此文件中的代码兼容Py3和PyQt5，除此之外不需要安装其他模块。
'''


try:
    from tkinter import Tk
    from tkinter.messagebox import showwarning
    from PyQt5.QtCore import (QVariant, Qt)
    from PyQt5.QtWidgets import (QApplication, QColorDialog, QDialog)
    from PyQt5.QtGui import QBrush, QPixmap, QPainter
    from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
    import ui_newimagedlg
except Exception as _err:
    Tk().withdraw()
    warn=showwarning("WARNING","WARNING Info:\n%s"%_err)


class NewImageDlg(QDialog, ui_newimagedlg.Ui_NewImageDlg):
# UI文件作为一个参数传入NewImageDlg，其中包含布局和翻译，以及键盘导航等等。
    def __init__(self, parent=None):
        super(NewImageDlg, self).__init__(parent)
        self.setupUi(self)
        # 相当于使用GUI生成代码器生成了一个py文件，取代了这一步，直接使用setupUI导入。
        self.color = Qt.red # 默认颜色红色
        for value, text in (
                (Qt.SolidPattern, "Solid"),
                (Qt.Dense1Pattern, "Dense #1"),
                (Qt.Dense2Pattern, "Dense #2"),
                (Qt.Dense3Pattern, "Dense #3"),
                (Qt.Dense4Pattern, "Dense #4"),
                (Qt.Dense5Pattern, "Dense #5"),
                (Qt.Dense6Pattern, "Dense #6"),
                (Qt.Dense7Pattern, "Dense #7"),
                (Qt.HorPattern, "Horizontal"),
                (Qt.VerPattern, "Vertical"),
                (Qt.CrossPattern, "Cross"),
                (Qt.BDiagPattern, "Backward Diagonal"),
                (Qt.FDiagPattern, "Forward Diagonal"),
                (Qt.DiagCrossPattern, "Diagonal Cross")):
            self.brushComboBox.addItem(text, QVariant(value)) #Qt的BrushStyle常量和名称，添加到brushCBox

        self.colorButton.clicked.connect(self.getColor)
        self.brushComboBox.activated.connect(self.setColor) #下拉菜单选中激活

        self.setColor()
        self.widthSpinBox.setFocus()


    def getColor(self):
        color = QColorDialog.getColor(Qt.black, self) #打开平台默认的ColorSelect模块
        if color.isValid(): # 如果颜色返回正确的值，则传递给setColor函数
            self.color = color
            self.setColor()


    def setColor(self):
        pixmap = self._makePixmap(60, 20)
        self.colorLabel.setPixmap(pixmap) # 对一个Label中施加Pixmap对象

    def image(self): #根据SpinBox的值来生成一个位图QImage对象
        pixmap = self._makePixmap(self.widthSpinBox.value(),
                                  self.heightSpinBox.value())
        return QPixmap.toImage(pixmap)


    def _makePixmap(self, width, height): # setColor的子对象 函数调用 第一个问题就是大小
        pixmap = QPixmap(width, height) #Pixmap似乎是专门搞这种笔刷显示工具的，为什么不让Painter进行大小设置？？
        style = self.brushComboBox.itemData(
                self.brushComboBox.currentIndex()) # 获取次目数据，然后获取该index的Data数据（text,text data）
        brush = QBrush(self.color, Qt.BrushStyle(style)) #将花纹和颜色添加到笔刷上
        painter = QPainter(pixmap) #画布内嵌地图
        painter.fillRect(pixmap.rect(), Qt.white) # 底纹背景颜色，将其铺满画布 作为背景 其必须保持在前面而不是后面
        painter.fillRect(pixmap.rect(), brush) # 将笔刷添加到Painter类的pixmap类型的画布中
        
        return pixmap


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = NewImageDlg()
    form.show()
    app.exec_()

