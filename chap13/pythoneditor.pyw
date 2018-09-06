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

import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qrc_resources


__version__ = "1.0.1"


class PythonHighlighter(QSyntaxHighlighter):  # SyntaxHighlighter::语法高亮.

    Rules = []

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()   # QTextCharFormat::文本_字符_格式.
        keywordFormat.setForeground(Qt.darkBlue)    # Foreground::前景
        keywordFormat.setFontWeight(QFont.Bold) # FontWeight::字型粗细, QFont.Bold::粗体
        for pattern in ((r"\band\b", r"\bas\b", r"\bassert\b",      # https://zhidao.baidu.com/question/446577778.html
                r"\bbreak\b", r"\bclass\b", r"\bcontinue\b",        # \b ::正则表达式界定词.例: r"\b...\b"
                r"\bdef\b", r"\bdel\b", r"\belif\b", r"\belse\b",
                r"\bexcept\b", r"\bexec\b", r"\bfinally\b", r"\bfor\b",
                r"\bfrom\b", r"\bglobal\b", r"\bif\b", r"\bimport\b",
                r"\bin\b", r"\bis\b", r"\blambda\b", r"\bnot\b",
                r"\bor\b", r"\bpass\b", r"\bprint\b", r"\braise\b",
                r"\breturn\b", r"\btry\b", r"\bwhile\b", r"\bwith\b",
                r"\byield\b")):
            PythonHighlighter.Rules.append((QRegExp(pattern), keywordFormat))

        commentFormat = QTextCharFormat()   # commentFormat::注释_格式,QTextCharFormat::文本_字符_格式.
        commentFormat.setForeground(QColor(0, 127, 0))    # Foreground::前景
        commentFormat.setFontItalic(True)   # Italic::斜体
        PythonHighlighter.Rules.append((QRegExp(r"#.*"), commentFormat))

        self.stringFormat = QTextCharFormat()
        self.stringFormat.setForeground(Qt.darkYellow)
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)   # Minimal::最小的...(设置为非贪婪模式)
        PythonHighlighter.Rules.append((stringRe, self.stringFormat))

        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, self.stringFormat))

        self.tripleSingleRe = QRegExp(r"""'''(?!")""")  # '''单引号模式::http://blog.csdn.net/sunhuaer123/article/details/16343313
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')  # """双引号模式::http://www.imkevinyang.com/2009/08/%E4%BD%BF%E7%94%A8%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%89%BE%E5%87%BA%E4%B8%8D%E5%8C%85%E5%90%AB%E7%89%B9%E5%AE%9A%E5%AD%97%E7%AC%A6%E4%B8%B2%E7%9A%84%E6%9D%A1%E7%9B%AE.html

    # 匹配当前text行所有 关键字 ,及字符串.
    def highlightBlock(self, text):  # 高亮块
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE = range(3)  #   0,1,2   NORMAL=正常 /标准, TRIPLESINGLE= ''' 模式, TRIPLEDOUBLE = """ 模式

        # 匹配当前text行所有 关键字 ,及字符串.
        for regex, format in PythonHighlighter.Rules:  # 对所有适配模式的关键字进行格式操作.
            i = regex.indexIn(text)  # 注:text以一行文本为单位.
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, format)
                i = regex.indexIn(text, i + length)

        # 设置当前块状态为 正常状态:NORMAL =0 [ '''状态TRIPLESINGLE =1 , """状态TRIPLEDOUBLE =2 ]
        self.setCurrentBlockState(NORMAL)  # 设置_当前_'块'_状态 ??????????

        # text有"""string......."""格式的字符串时返回.
        if self.stringRe.indexIn(text) != -1:
            return

        # text为 '''/ """ 区块格式的字符串.
        for i, state in ((self.tripleSingleRe.indexIn(text),TRIPLESINGLE),(self.tripleDoubleRe.indexIn(text),TRIPLEDOUBLE)):
            if self.previousBlockState() == state:  # previousBlockState::前一个片状态.
                if i == -1:
                    # i = text.length()
                    i = len(text)
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3, self.stringFormat)
            elif i > -1:
                self.setCurrentBlockState(state)
                # self.setFormat(i, text.length(), self.stringFormat)
                self.setFormat(i, len(text), self.stringFormat)


class TextEdit(QTextEdit):

    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)

    # 修改TAB键按下时输出为四个空格.
    def event(self, event):
        if (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab):
            cursor = self.textCursor()
            cursor.insertText("    ")
            return True
        return QTextEdit.event(self, event)


class MainWindow(QMainWindow):

    def __init__(self, filename=None, parent=None):
        super(MainWindow, self).__init__(parent)

        font = QFont("Courier", 11)
        font.setFixedPitch(True)    # 设置_固定_间距
        self.editor = TextEdit()
        self.editor.setFont(font)
        self.highlighter = PythonHighlighter(self.editor.document())  # parent == self.editor.document()
        self.setCentralWidget(self.editor)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        fileNewAction = self.createAction("&New...", self.fileNew, QKeySequence.New, "filenew", "Create a Python file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen, QKeySequence.Open, "fileopen", "Open an existing Python file")

        self.fileSaveAction = self.createAction("&Save", self.fileSave, QKeySequence.Save, "filesave", "Save the file")
        self.fileSaveAsAction = self.createAction("Save &As...", self.fileSaveAs, icon="filesaveas", tip="Save the file using a new name")

        fileQuitAction = self.createAction("&Quit", self.close, "Ctrl+Q", "filequit", "Close the application")

        self.editCopyAction = self.createAction("&Copy", self.editor.copy, QKeySequence.Copy, "editcopy", "Copy text to the clipboard")
        self.editCutAction = self.createAction("Cu&t", self.editor.cut, QKeySequence.Cut, "editcut", "Cut text to the clipboard")
        self.editPasteAction = self.createAction("&Paste", self.editor.paste, QKeySequence.Paste, "editpaste", "Paste in the clipboard's text")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction, self.fileSaveAction, self.fileSaveAsAction, None, fileQuitAction))

        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (self.editCopyAction, self.editCutAction, self.editPasteAction))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction, self.fileSaveAction))

        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (self.editCopyAction, self.editCutAction, self.editPasteAction))

        self.connect(self.editor, SIGNAL("selectionChanged()"), self.updateUi)  # 获得焦点 / 失去焦点 时...
        self.connect(self.editor.document(), SIGNAL("modificationChanged(bool)"), self.updateUi)  # modificationChanged::发生 修正_改变 时...
        self.connect(QApplication.clipboard(), SIGNAL("dataChanged()"), self.updateUi)  # QApplication.clipboard()::应用.粘贴板

        self.resize(800, 600)
        self.setWindowTitle("Python Editor")
        self.filename = filename
        if self.filename is not None:
            self.loadFile()
        self.updateUi()


    def updateUi(self, arg=None):
        self.fileSaveAction.setEnabled(self.editor.document().isModified())
        self.fileSaveAsAction.setEnabled(not self.editor.document().isEmpty())

        enable = self.editor.textCursor().hasSelection()
        self.editCopyAction.setEnabled(enable)
        self.editCutAction.setEnabled(enable)
        self.editPasteAction.setEnabled(self.editor.canPaste())  # canPaste()::是否允许从剪贴板粘贴


    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)   # 设置动作为可复选.
        return action


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def closeEvent(self, event):
        if not self.okToContinue():
            event.ignore()


    def okToContinue(self):
        if self.editor.document().isModified():
            reply = QMessageBox.question(self,
                            "Python Editor - Unsaved Changes",
                            "Save unsaved changes?",
                            QMessageBox.Yes|QMessageBox.No|
                            QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True


    def fileNew(self):
        if not self.okToContinue():
            return
        document = self.editor.document()
        document.clear()
        document.setModified(False)
        self.filename = None
        self.setWindowTitle("Python Editor - Unnamed")
        self.updateUi()


    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        fname = QFileDialog.getOpenFileName(self,
                "Python Editor - Choose File", dir,
                "Python files (*.py *.pyw)")
        if fname:
            self.filename = fname
            self.loadFile()


    def loadFile(self):
        fh = None
        try:
            fh = QFile(self.filename)   # 实例化文件对像.
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QTextStream(fh)    # 文本流..
            stream.setCodec("UTF-8")
            self.editor.setPlainText(stream.readAll())  # PlainText::纯文本.
            self.editor.document().setModified(False)
            self.setWindowTitle("Python Editor - {}".format(
                    QFileInfo(self.filename).fileName()))
        except EnvironmentError as e:   # EnvironmentError::环境_错误
            QMessageBox.warning(self, "Python Editor -- Load Error",
                    "Failed to load {}: {}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()


    def fileSave(self):
        if self.filename is None:
            return self.fileSaveAs()
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.editor.toPlainText()
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self, "Python Editor -- Save Error",
                    "Failed to save {}: {}".format(self.filename, e))
            return False
        finally:
            if fh is not None:
                fh.close()
        return True


    def fileSaveAs(self):
        filename = self.filename if self.filename is not None else "."
        filename = QFileDialog.getSaveFileName(self,
                "Python Editor -- Save File As", filename,
                "Python files (*.py *.pyw)")
        if filename:
            self.filename = filename
            self.setWindowTitle("Python Editor - {}".format(
                    QFileInfo(self.filename).fileName()))
            return self.fileSave()
        return False


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icon.png"))
    fname = None
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    form = MainWindow(fname)
    form.show()
    app.exec_()


main()

