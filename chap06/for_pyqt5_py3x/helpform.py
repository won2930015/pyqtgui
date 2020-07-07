#!/usr/bin/env python3


try:
    from tkinter import Tk
    from tkinter.messagebox import showwarning
    from PyQt5.QtGui import *
    import PyQt5
    from PyQt5.QtCore import *
    import qrc_resources
    from PyQt5.QtWidgets import *
except Exception as _err:
    Tk().withdraw()
    warn=showwarning("WARNING","WARNING Info:\n%s"%_err)

class HelpForm(QDialog):
    def __init__(self,page,parent=None):
        super(HelpForm,self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_GroupLeader)

        backAction = QAction(QIcon(":/back.png"), "&Back", self)
        backAction.setShortcut(QKeySequence.Back)
        homeAction = QAction(QIcon(":/home.png"), "&Home", self)
        homeAction.setShortcut("Home")
        self.pageLabel = QLabel()

        toolBar = QToolBar()
        toolBar.addAction(backAction)
        toolBar.addAction(homeAction)
        toolBar.addWidget(self.pageLabel)
        self.textBrowser = QTextBrowser()

        layout = QVBoxLayout()
        layout.addWidget(toolBar)
        layout.addWidget(self.textBrowser, 1)
        self.setLayout(layout)

        backAction.triggered.connect(self.textBrowser.backward)
        homeAction.triggered.connect(self.textBrowser.home)

        self.textBrowser.sourceChanged.connect(self.updatePageTitle)

        self.textBrowser.setSearchPaths([":/help"])
        self.textBrowser.setSource(QUrl(page))
        self.resize(400,600)
        self.setWindowTitle("%s Help"%QApplication.applicationName())
    def updatePageTitle(self):
        self.pageLabel.setText(self.textBrowser.documentTitle())

if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    form=HelpForm("index.html")
    form.show()