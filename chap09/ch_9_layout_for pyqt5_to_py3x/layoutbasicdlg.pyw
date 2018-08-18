#！/usr/bin/env python3

import PyQt5,sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import ui_layoutbasicdlg

class Form(QDialog,ui_layoutbasicdlg.Ui_layoutBasicDlg):
    def __init__(self,parent=None):
        super(Form,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("布局测试")


if __name__=="__main__":
    app=QApplication(sys.argv)
    form=Form()
    form.show()
    app.exec_()
