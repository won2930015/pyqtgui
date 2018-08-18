# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cmaddeditmoviedlg.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(590, 395)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setMinimumSize(QtCore.QSize(100, 0))
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.spinBox_2 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_2.setMinimumSize(QtCore.QSize(100, 0))
        self.spinBox_2.setObjectName("spinBox_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.spinBox_2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setMinimumSize(QtCore.QSize(100, 0))
        self.dateEdit.setObjectName("dateEdit")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.dateEdit)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.plainTextEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.label.setBuddy(self.lineEdit)
        self.label_2.setBuddy(self.spinBox)
        self.label_3.setBuddy(self.spinBox_2)
        self.label_4.setBuddy(self.dateEdit)
        self.label_5.setBuddy(self.plainTextEdit)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "标题"))
        self.label_2.setText(_translate("Dialog", "上映年份"))
        self.label_3.setText(_translate("Dialog", "时长"))
        self.label_4.setText(_translate("Dialog", "观看时间"))
        self.label_5.setText(_translate("Dialog", "备注"))

