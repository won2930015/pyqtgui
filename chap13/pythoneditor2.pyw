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


__version__ = "1.1.0"


class PythonHighlighter(QSyntaxHighlighter):    # SyntaxHighlighter::语法高亮.

    Rules = []
    Formats = {}    #定义为字典.

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()    #格式_初始化

        #关键字
        KEYWORDS = ["and", "as", "assert", "break", "class",
                "continue", "def", "del", "elif", "else", "except",
                "exec", "finally", "for", "from", "global", "if",
                "import", "in", "is", "lambda", "not", "or", "pass",
                "print", "raise", "return", "try", "while", "with",
                "yield"]

        #内置函数
        BUILTINS = ["abs", "all", "any", "basestring", "bool",
                "callable", "chr", "classmethod", "cmp", "compile",
                "complex", "delattr", "dict", "dir", "divmod",
                "enumerate", "eval", "execfile", "exit", "file",
                "filter", "float", "frozenset", "getattr", "globals",
                "hasattr", "hex", "id", "int", "isinstance",
                "issubclass", "iter", "len", "list", "locals", "map",
                "max", "min", "object", "oct", "open", "ord", "pow",
                "property", "range", "reduce", "repr", "reversed",
                "round", "set", "setattr", "slice", "sorted",
                "staticmethod", "str", "sum", "super", "tuple", "type",
                "vars", "zip"] 

        #常量
        CONSTANTS = ["False", "True", "None", "NotImplemented",
                     "Ellipsis"]

        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % keyword for keyword in KEYWORDS])), "keyword"))   #关键字
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % builtin for builtin in BUILTINS])), "builtin"))   #内置函数
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % constant for constant in CONSTANTS])), "constant"))   #常量
        PythonHighlighter.Rules.append((QRegExp(
                r"\b[+-]?[0-9]+[lL]?\b"     #10进制数
                r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"     #16进制数
                r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"),  #浮点指数
                "number"))  #数值
        PythonHighlighter.Rules.append((QRegExp(
                r"\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b"), "pyqt"))        #\w+  匹配数字和字母下划线的多个字符
        PythonHighlighter.Rules.append((QRegExp(r"\b@\w+\b"),
                "decorator"))       #装饰器.
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")  #匹配字符串的正则表达式.
        stringRe.setMinimal(True)   #设置非贪婪匹配模式(小最匹配模式)
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")   ##设置三个'''或""""号的字符串匹配模式.
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        self.tripleSingleRe = QRegExp(r"""'''(?!")""")  #   匹配'''单引号,但前驱 != "  ::http://blog.csdn.net/sunhuaer123/article/details/16343313
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')  ##  匹配"""双引号,但前驱 != '


    @staticmethod
    def initializeFormats():    #格式_初始化
        baseFormat = QTextCharFormat()
        baseFormat.setFontFamily("courier") #设置_字体_家族
        baseFormat.setFontPointSize(12)     #设置_点_大小(字符大小)
        for name, color in (("normal", Qt.black),
                ("keyword", Qt.darkBlue), ("builtin", Qt.darkRed),
                ("constant", Qt.darkGreen),
                ("decorator", Qt.darkBlue), ("comment", Qt.darkGreen),
                ("string", Qt.darkYellow), ("number", Qt.darkMagenta),
                ("error", Qt.darkRed), ("pyqt", Qt.darkCyan)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(QColor(color))
            if name in ("keyword", "decorator"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            PythonHighlighter.Formats[name] = format    #设置字典key:value对::{"keyword":format,"builtin":format,...}


    def highlightBlock(self, text): #高亮_块
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE, ERROR = range(4)    #   0,1,2 ,3  NORMAL=正常 /标准, TRIPLESINGLE= ''' 模式, TRIPLEDOUBLE = """ 模式, ERROR=错误

        textLength = len(text)
        prevState = self.previousBlockState()   # 前置_块_状态

        self.setFormat(0, textLength, PythonHighlighter.Formats["normal"])

        if text.startswith("Traceback") or text.startswith("Error: "):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength, PythonHighlighter.Formats["error"])
            return
        if (prevState == ERROR and not (text.startswith(sys.ps1) or text.startswith("#"))):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength, PythonHighlighter.Formats["error"])
            return

        for regex, format in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()  #matchedLength::匹配_长度
                self.setFormat(i, length, PythonHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)

        # Slow but good quality highlighting for comments. For more
        # speed, comment this out and add the following to __init__:
        # PythonHighlighter.Rules.append((QRegExp(r"#.*"), "comment"))
        if not text:
            pass
        elif text[0] == "#":
            self.setFormat(0, len(text), PythonHighlighter.Formats["comment"])
        else:
            stack = []  # 堆栈
            for i, c in enumerate(text):
                if c in ('"', "'"):     #包含 " 或 ' 号时执行.
                    if stack and stack[-1] == c:
                        stack.pop()
                    else:
                        stack.append(c)
                elif c == "#" and len(stack) == 0:
                    self.setFormat(i, len(text),
                                   PythonHighlighter.Formats["comment"])
                    break

        self.setCurrentBlockState(NORMAL)

        if self.stringRe.indexIn(text) != -1:
            return
        # This is fooled by triple quotes inside single quoted strings
        for i, state in ((self.tripleSingleRe.indexIn(text),
                          TRIPLESINGLE),
                         (self.tripleDoubleRe.indexIn(text),
                          TRIPLEDOUBLE)):
            if self.previousBlockState() == state:
                if i == -1:
                    i = len(text)
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3,     
                               PythonHighlighter.Formats["string"])
            elif i > -1:
                self.setCurrentBlockState(state)
                self.setFormat(i, len(text),
                               PythonHighlighter.Formats["string"])


    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(
                                                    Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()


class TextEdit(QTextEdit):

    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)


    def event(self, event):
        if (event.type() == QEvent.KeyPress and
            event.key() == Qt.Key_Tab):
            cursor = self.textCursor()
            cursor.insertText("    ")
            return True
        return QTextEdit.event(self, event)


class MainWindow(QMainWindow):

    def __init__(self, filename=None, parent=None):
        super(MainWindow, self).__init__(parent)

        font = QFont("Courier", 11)
        font.setFixedPitch(True)
        self.editor = TextEdit()
        self.editor.setFont(font)
        self.highlighter = PythonHighlighter(self.editor.document())
        self.setCentralWidget(self.editor)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        fileNewAction = self.createAction("&New...", self.fileNew,
                QKeySequence.New, "filenew", "Create a Python file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing Python file")
        self.fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save the file")
        self.fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save the file using a new name")
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
        self.editCopyAction = self.createAction("&Copy",
                self.editor.copy, QKeySequence.Copy, "editcopy",
                "Copy text to the clipboard")
        self.editCutAction = self.createAction("Cu&t", self.editor.cut,
                QKeySequence.Cut, "editcut",
                "Cut text to the clipboard")
        self.editPasteAction = self.createAction("&Paste",
                self.editor.paste, QKeySequence.Paste, "editpaste",
                "Paste in the clipboard's text")
        self.editIndentAction = self.createAction("&Indent",
                self.editIndent, "Ctrl+]", "editindent",
                "Indent the current line or selection")
        self.editUnindentAction = self.createAction("&Unindent",
                self.editUnindent, "Ctrl+[", "editunindent",
                "Unindent the current line or selection")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                self.fileSaveAction, self.fileSaveAsAction, None,
                fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (self.editCopyAction,
                self.editCutAction, self.editPasteAction, None,
                self.editIndentAction, self.editUnindentAction))
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      self.fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (self.editCopyAction,
                self.editCutAction, self.editPasteAction, None,
                self.editIndentAction, self.editUnindentAction))

        self.connect(self.editor,
                SIGNAL("selectionChanged()"), self.updateUi)
        self.connect(self.editor.document(),
                SIGNAL("modificationChanged(bool)"), self.updateUi)
        self.connect(QApplication.clipboard(),
                SIGNAL("dataChanged()"), self.updateUi)

        self.resize(800, 600)
        self.setWindowTitle("Python Editor")
        self.filename = filename
        if self.filename is not None:
            self.loadFile()
        self.updateUi()


    def updateUi(self, arg=None):
        self.fileSaveAction.setEnabled(
                self.editor.document().isModified())
        enable = not self.editor.document().isEmpty()
        self.fileSaveAsAction.setEnabled(enable)
        self.editIndentAction.setEnabled(enable)
        self.editUnindentAction.setEnabled(enable)
        enable = self.editor.textCursor().hasSelection()
        self.editCopyAction.setEnabled(enable)
        self.editCutAction.setEnabled(enable)
        self.editPasteAction.setEnabled(self.editor.canPaste())


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
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
            action.setCheckable(True)
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
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            self.editor.setPlainText(stream.readAll())
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self, "Python Editor -- Load Error",
                    "Failed to load {}: {}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        self.setWindowTitle("Python Editor - {}".format(
                QFileInfo(self.filename).fileName()))


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


    def editIndent(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.clearSelection()
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.StartOfLine)
            while pos <= end:
                cursor.insertText("    ")
                cursor.movePosition(QTextCursor.Down)
                cursor.movePosition(QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, end - start)
        else:
            pos = cursor.position()
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.insertText("    ")
            cursor.setPosition(pos + 4)
        cursor.endEditBlock()


    def editUnindent(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.StartOfLine)
            while pos <= end:
                cursor.clearSelection()
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.KeepAnchor, 4)
                if cursor.selectedText() == "    ":
                    cursor.removeSelectedText()
                cursor.movePosition(QTextCursor.Down)
                cursor.movePosition(QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, end - start)
        else:
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, 4)
            if cursor.selectedText() == "    ":
                cursor.removeSelectedText()
        cursor.endEditBlock()


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

