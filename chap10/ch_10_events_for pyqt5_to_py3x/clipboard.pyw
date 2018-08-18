#!/usr/bin/env python3
'''这是一个PyQt 5 剪贴板示例程序
Written by Corkine Ma (cm@marvinstudio.cn)'''

import os,traceback
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        textCopyButton = QPushButton("&Copy Text")
        textPasteButton = QPushButton("Paste &Text")
        htmlCopyButton = QPushButton("C&opy HTML")
        htmlPasteButton = QPushButton("Paste &HTML")
        imageCopyButton = QPushButton("Co&py Image")
        imagePasteButton = QPushButton("Paste &Image")
        self.textLabel = QLabel("Original text")
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap(os.path.join(
                os.path.dirname(__file__), "images/usb.png")))

        layout = QGridLayout()
        layout.addWidget(textCopyButton, 0, 0)
        layout.addWidget(imageCopyButton, 0, 1)
        layout.addWidget(htmlCopyButton, 0, 2)
        layout.addWidget(textPasteButton, 1, 0)
        layout.addWidget(imagePasteButton, 1, 1)
        layout.addWidget(htmlPasteButton, 1, 2)
        layout.addWidget(self.textLabel, 2, 0, 1, 2)
        layout.addWidget(self.imageLabel, 2, 2)
        self.setLayout(layout)

        # self.connect(textCopyButton, SIGNAL("clicked()"), self.copyText)
        # self.connect(textPasteButton, SIGNAL("clicked()"), self.pasteText)
        # self.connect(htmlCopyButton, SIGNAL("clicked()"), self.copyHtml)
        # self.connect(htmlPasteButton, SIGNAL("clicked()"), self.pasteHtml)
        # self.connect(imageCopyButton, SIGNAL("clicked()"), self.copyImage)
        # self.connect(imagePasteButton, SIGNAL("clicked()"),
        #              self.pasteImage)
        textCopyButton.clicked.connect(self.copyText)
        textPasteButton.clicked.connect(self.pasteText)
        htmlCopyButton.clicked.connect(self.copyHtml)
        htmlPasteButton.clicked.connect(self.pasteHtml)
        imageCopyButton.clicked.connect(self.copyImage)
        imagePasteButton.clicked.connect(self.pasteImage)
        
        self.setWindowTitle("Clipboard")

    def copyText(self):
        clipboard=QGuiApplication.clipboard()
        clipboard.setText("这就是你复制的东西，什么也没有...")

    def pasteText(self):
        clipboard=QGuiApplication.clipboard()
        self.textLabel.setText(clipboard.text())

    def copyHtml(self):
        mimedata=QMimeData()
        mimedata.setHtml("<b>Hello</b> <font color=gray>Corkine</font>")
        clipboard=QGuiApplication.clipboard()
        clipboard.setMimeData(mimedata)

    def pasteHtml(self):
        # mimedata=QMimeData()
        clipboard=QGuiApplication.clipboard()
        mimedata=clipboard.mimeData()
        if mimedata.hasHtml():
            self.textLabel.setText(mimedata.html())

    def copyImage(self):
        clipboard=QGuiApplication.clipboard()
        clipboard.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__),"images/gv.png")))
        # clipboard.setPixmap(QPixmap("images/gv.png")) # 设置QPixmap必须使用绝对路径

    def pasteImage(self):
        clipboard=QGuiApplication.clipboard()
        self.imageLabel.setPixmap(clipboard.pixmap())


if __name__=="__main__":
        app=QApplication(sys.argv)
        form=Form()
        form.show()
        app.exec_()
