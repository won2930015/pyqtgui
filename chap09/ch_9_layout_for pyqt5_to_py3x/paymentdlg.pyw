#!/usr/bin/env python3

import PyQt5,sys,traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import ui_paymentdlg

class Form(QDialog,ui_paymentdlg.Ui_paymentDlg):
    def __init__(self,parent=None):
        super(Form,self).__init__(parent)
        self.setupUi(self)
        self.stackedWidget.setHidden(True)
        self.radioButton_5.setChecked(True)
        self.goodsGroup.setVisible(False)
        self.radioButton_6.toggled.connect(self.updateUI)
        self.comboBox_4.currentIndexChanged.connect(self.updateUI2)#如果返回到updateUI有可能产生信号冲突
        self.moreButton.clicked.connect(self.showMore)
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.sayOk)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.close)

        self.setWindowTitle("付款 - 克莱登大学附属汽车城")
        self.updateUI(False)
        self.updateUI2()
    def updateUI(self,state):
        # QMessageBox.warning(self,"WARNING",str(state))
        self.tabWidget.setHidden(state)
        self.comboBox_4.setEnabled(state)
        self.stackedWidget.setHidden(not state)
    def updateUI2(self):
        self.stackedWidget.setCurrentIndex(self.comboBox_4.currentIndex())
    def sayOk(self):
        QMessageBox.warning(self,"Info","OK!")
        self.close()
    def showMore(self):
        # QMessageBox.warning(self,"WARN",self.moreButton.text())
        if self.moreButton.text()=="&Hide":
            # QMessageBox.warning(self,"WARN","In")
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_7.setChecked(False)
            self.checkBox_8.setChecked(False)
            self.goodsGroup.setVisible(False)
        else:
            self.goodsGroup.setVisible(True)
        if self.moreButton.text()=="&More":
            self.moreButton.setText("&Hide")
        else:
            self.moreButton.setText("&More")
            
        





if __name__=="__main__":
    app=QApplication(sys.argv)
    form=Form()
    form.show()

    app.exec_()