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

import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class RichTextLineEdit(QTextEdit):

    (Bold, Italic, Underline, StrikeOut, Monospaced, Sans, Serif,
     NoSuperOrSubscript, Subscript, Superscript) = range(10)


    def __init__(self, parent=None):
        super(RichTextLineEdit, self).__init__(parent)

        self.monofamily = "courier" #等宽字体
        self.sansfamily = "helvetica"   #无衬线字体
        self.seriffamily = "times"  #有衬线字体
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setTabChangesFocus(True)   #设置_Tab_变化_焦点=True
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  #setVerticalScrollBarPolicy::设置_垂直_滚动_条_策略 ,Qt.ScrollBarAlwaysOff::滚动_条_总是_关闭
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)    #setHorizontalScrollBarPolicy::设置_水平_滚动_条_策略
        fm = QFontMetrics(self.font())      #创建 字体_度量 对象.
        h = int(fm.height() * (1.4 if platform.system() == "Windows"
                                   else 1.2))
        self.setMinimumHeight(h) #设置 LineEdit 最小高度
        self.setMaximumHeight(int(h * 1.2)) ##设置 LineEdit 最大高度
        self.setToolTip("Press <b>Ctrl+M</b> for the text effects " #Ctrl+M == 文本效果
                "menu and <b>Ctrl+K</b> for the color menu")    #Ctrl+k == 颜色

    
    def toggleItalic(self): #斜体
        self.setFontItalic(not self.fontItalic())


    def toggleUnderline(self):  #下划线
        self.setFontUnderline(not self.fontUnderline())


    def toggleBold(self):   #粗体
        self.setFontWeight(QFont.Normal
                if self.fontWeight() > QFont.Normal else QFont.Bold)    #字体类形之间可以比较.


    def sizeHint(self): #大小提示
        return QSize(self.document().idealWidth() + 5,  #idealWidth::理想_宽度   (宽/高)
                     self.maximumHeight())


    def minimumSizeHint(self):  # 最小值提示
        fm = QFontMetrics(self.font())
        return QSize(fm.width("WWWW"), self.minimumHeight())


    def contextMenuEvent(self, event):  # 环境/上下文 菜单事件
        self.textEffectMenu()   #文本_效果_菜单

        
    def keyPressEvent(self, event): # 键按下事件
        if event.modifiers() & Qt.ControlModifier:
            handled = False     # handled::处理
            if event.key() == Qt.Key_B:
                self.toggleBold()
                handled = True
            elif event.key() == Qt.Key_I:
                self.toggleItalic()
                handled = True
            elif event.key() == Qt.Key_K:
                self.colorMenu()
                handled = True
            elif event.key() == Qt.Key_M:
                self.textEffectMenu()
                handled = True
            elif event.key() == Qt.Key_U:
                self.toggleUnderline()
                handled = True
            if handled:
                event.accept()
                return
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.emit(SIGNAL("returnPressed()"))
            event.accept()
        else:
            QTextEdit.keyPressEvent(self, event)


    def colorMenu(self):    #颜色菜单
        pixmap = QPixmap(22, 22)
        menu = QMenu("Colour")
        for text, color in (
                ("&Black", Qt.black),
                ("B&lue", Qt.blue),
                ("Dark Bl&ue", Qt.darkBlue),
                ("&Cyan", Qt.cyan),
                ("Dar&k Cyan", Qt.darkCyan),
                ("&Green", Qt.green),
                ("Dark Gr&een", Qt.darkGreen),
                ("M&agenta", Qt.magenta),
                ("Dark Mage&nta", Qt.darkMagenta),
                ("&Red", Qt.red),
                ("&Dark Red", Qt.darkRed)):
            color = QColor(color)
            pixmap.fill(color)
            action = menu.addAction(QIcon(pixmap), text, self.setColor)
            action.setData(color)
        self.ensureCursorVisible()  #确保_光标_可见()
        menu.exec_(self.viewport().mapToGlobal(self.cursorRect().center()))


    def setColor(self):
        action = self.sender()  #将当前被触发的动作 关联到 action对象.
        if action is not None and isinstance(action, QAction):
            color = QColor(action.data())
            if color.isValid(): #is_有效的....
                self.setTextColor(color)


    def textEffectMenu(self):   # 文本_效果_菜单.
        format = self.currentCharFormat()   # 创键 当前_字符_格式 对象.
        menu = QMenu("Text Effect")
        for text, shortcut, data, checked in (
                ("&Bold", "Ctrl+B", RichTextLineEdit.Bold,  #粗体
                 self.fontWeight() > QFont.Normal),
                ("&Italic", "Ctrl+I", RichTextLineEdit.Italic,  #斜体
                 self.fontItalic()),
                ("Strike &out", None, RichTextLineEdit.StrikeOut,   #删除线
                 format.fontStrikeOut()),
                ("&Underline", "Ctrl+U", RichTextLineEdit.Underline,    #下划线
                 self.fontUnderline()),
                ("&Monospaced", None, RichTextLineEdit.Monospaced,  #等宽字体
                 format.fontFamily() == self.monofamily),
                ("&Serifed", None, RichTextLineEdit.Serif,  #衬线体
                 format.fontFamily() == self.seriffamily),
                ("S&ans Serif", None, RichTextLineEdit.Sans,    #无衬线体
                 format.fontFamily() == self.sansfamily),
                ("&No super or subscript", None,        # 没有超级或下标???
                 RichTextLineEdit.NoSuperOrSubscript,
                 format.verticalAlignment() ==  #verticalAlignment::垂直_对齐
                 QTextCharFormat.AlignNormal),  #AlignNormal::对齐_标准
                ("Su&perscript", None, RichTextLineEdit.Superscript,    #上标
                 format.verticalAlignment() ==
                 QTextCharFormat.AlignSuperScript),
                ("Subs&cript", None, RichTextLineEdit.Subscript,    #下标
                 format.verticalAlignment() ==
                 QTextCharFormat.AlignSubScript)):
            action = menu.addAction(text, self.setTextEffect)
            if shortcut is not None:
                action.setShortcut(QKeySequence(shortcut))
            action.setData(data)
            action.setCheckable(True)   #设置成复选
            action.setChecked(checked)
            self.ensureCursorVisible()  #确保_光标_可见()
        menu.exec_(self.viewport().mapToGlobal(
                   self.cursorRect().center()))


    def setTextEffect(self):    #设置_文本_效果
        action = self.sender()  #将当前触发的动作关联action对象.
        if action is not None and isinstance(action, QAction):
            what = int(action.data())
            if what == RichTextLineEdit.Bold:
                self.toggleBold()
                return
            if what == RichTextLineEdit.Italic:
                self.toggleItalic()
                return
            if what == RichTextLineEdit.Underline:
                self.toggleUnderline()
                return
            format = self.currentCharFormat()
            if what == RichTextLineEdit.Monospaced:
                format.setFontFamily(self.monofamily)
            elif what == RichTextLineEdit.Serif:
                format.setFontFamily(self.seriffamily)
            elif what == RichTextLineEdit.Sans:
                format.setFontFamily(self.sansfamily)
            if what == RichTextLineEdit.StrikeOut:
                format.setFontStrikeOut(not format.fontStrikeOut())
            if what == RichTextLineEdit.NoSuperOrSubscript:
                format.setVerticalAlignment(
                        QTextCharFormat.AlignNormal)
            elif what == RichTextLineEdit.Superscript:
                format.setVerticalAlignment(
                        QTextCharFormat.AlignSuperScript)
            elif what == RichTextLineEdit.Subscript:
                format.setVerticalAlignment(
                        QTextCharFormat.AlignSubScript)
            self.mergeCurrentCharFormat(format) #mergeCurrentCharFormat::合并_当前_字符_格式.


    def toSimpleHtml(self): # to_简单_Html
        html = ""
        black = QColor(Qt.black)
        block = self.document().begin()
        while block.isValid():
            iterator = block.begin()
            while iterator != block.end():
                fragment = iterator.fragment()  #fragment::片段
                if fragment.isValid():
                    format = fragment.charFormat()
                    family = format.fontFamily()
                    color = format.foreground().color()
                    text = Qt.escape(fragment.text())
                    if (format.verticalAlignment() ==
                        QTextCharFormat.AlignSubScript):
                        text = "<sub>{}</sub>".format(text)
                    elif (format.verticalAlignment() ==
                          QTextCharFormat.AlignSuperScript):
                        text = "<sup>{}</sup>".format(text)
                    if format.fontUnderline():
                        text = "<u>{}</u>".format(text)
                    if format.fontItalic():
                        text = "<i>{}</i>".format(text)
                    if format.fontWeight() > QFont.Normal:
                        text = "<b>{}</b>".format(text)
                    if format.fontStrikeOut():
                        text = "<s>{}</s>".format(text)
                    if color != black or family:
                        attribs = ""
                        if color != black:
                            attribs += ' color="{}"'.format(color.name())
                        if family:
                            attribs += ' face="{}"'.format(family)
                        text = "<font{}>{}</font>".format(attribs, text)
                    html += text
                iterator += 1
            block = block.next()
        return html


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lineedit = RichTextLineEdit()
    lineedit.show()
    lineedit.setWindowTitle("RichTextEdit")
    app.exec_()
    print(lineedit.toHtml())
    print(lineedit.toPlainText())
    print(lineedit.toSimpleHtml())


