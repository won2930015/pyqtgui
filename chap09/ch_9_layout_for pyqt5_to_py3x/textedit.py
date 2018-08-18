#!/usr/bin/env python3
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TextEdit(QTextEdit):

    NextId = 1

    def __init__(self, filename='', parent=None):
        super(TextEdit, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.filename = filename
        if self.filename=='':
            self.filename = str("未命名-{0}".format(
                                    TextEdit.NextId))
            TextEdit.NextId += 1
        self.document().setModified(False)
        self.setWindowTitle(QFileInfo(self.filename).fileName())

    
    def closeEvent(self, event):
        if (self.document().isModified() and 
            QMessageBox.question(self,
                   "文本编辑器 - 未保存的更改",
                   "保存在 {0} 文件中所做出的更改?".format(self.filename),
                   QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
            try:
                self.save()
            except EnvironmentError as e:
                QMessageBox.warning(self,
                        "文本编辑器 - 保存错误",
                        "保存失败 {0}: {1}".format(self.filename, e))


    def isModified(self):
        return self.document().isModified()


    def save(self):
        if self.filename[:3]=='未命名':
            if self.filename[-4:]==".txt":
                self.filename=self.filename[:-4]
            filename = QFileDialog.getSaveFileName(self,
                    "文本编辑器 - 另存为", self.filename,
                    "cm Text files (*.cmt *.*)")
            if filename[0]=='':
                return
            self.filename = filename[0]
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.toPlainText()
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


    def load(self):
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            self.setPlainText(stream.readAll())
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

if __name__=="__main__":
    app=QApplication(sys.argv)
    form=TextEdit()
    form.show()
    app.exec_()
