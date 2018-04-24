# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ticketorderdlg1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TicketOrderDlg(object):
    def setupUi(self, TicketOrderDlg):
        TicketOrderDlg.setObjectName(_fromUtf8("TicketOrderDlg"))
        TicketOrderDlg.resize(379, 140)
        self.gridlayout = QtGui.QGridLayout(TicketOrderDlg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(TicketOrderDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 6)
        spacerItem = QtGui.QSpacerItem(361, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 6)
        self.amountLabel = QtGui.QLabel(TicketOrderDlg)
        self.amountLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.amountLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.amountLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.amountLabel.setObjectName(_fromUtf8("amountLabel"))
        self.gridlayout.addWidget(self.amountLabel, 2, 5, 1, 1)
        self.label_4 = QtGui.QLabel(TicketOrderDlg)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.label_3 = QtGui.QLabel(TicketOrderDlg)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(TicketOrderDlg)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridlayout.addWidget(self.label_5, 2, 4, 1, 1)
        self.priceSpinBox = QtGui.QDoubleSpinBox(TicketOrderDlg)
        self.priceSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.priceSpinBox.setMaximum(5000.0)
        self.priceSpinBox.setObjectName(_fromUtf8("priceSpinBox"))
        self.gridlayout.addWidget(self.priceSpinBox, 2, 1, 1, 1)
        self.quantitySpinBox = QtGui.QSpinBox(TicketOrderDlg)
        self.quantitySpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.quantitySpinBox.setMaximum(50)
        self.quantitySpinBox.setMinimum(1)
        self.quantitySpinBox.setProperty("value", 1)
        self.quantitySpinBox.setObjectName(_fromUtf8("quantitySpinBox"))
        self.gridlayout.addWidget(self.quantitySpinBox, 2, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(81, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 1, 4, 1, 2)
        self.label_2 = QtGui.QLabel(TicketOrderDlg)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.whenDateTimeEdit = QtGui.QDateTimeEdit(TicketOrderDlg)
        self.whenDateTimeEdit.setObjectName(_fromUtf8("whenDateTimeEdit"))
        self.gridlayout.addWidget(self.whenDateTimeEdit, 1, 1, 1, 2)
        self.customerLineEdit = QtGui.QLineEdit(TicketOrderDlg)
        self.customerLineEdit.setObjectName(_fromUtf8("customerLineEdit"))
        self.gridlayout.addWidget(self.customerLineEdit, 0, 1, 1, 5)
        self.label = QtGui.QLabel(TicketOrderDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_4.setBuddy(self.quantitySpinBox)
        self.label_3.setBuddy(self.priceSpinBox)
        self.label_2.setBuddy(self.whenDateTimeEdit)
        self.label.setBuddy(self.customerLineEdit)

        self.retranslateUi(TicketOrderDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TicketOrderDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TicketOrderDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(TicketOrderDlg)
        TicketOrderDlg.setTabOrder(self.customerLineEdit, self.whenDateTimeEdit)
        TicketOrderDlg.setTabOrder(self.whenDateTimeEdit, self.priceSpinBox)
        TicketOrderDlg.setTabOrder(self.priceSpinBox, self.quantitySpinBox)
        TicketOrderDlg.setTabOrder(self.quantitySpinBox, self.buttonBox)

    def retranslateUi(self, TicketOrderDlg):
        TicketOrderDlg.setWindowTitle(_translate("TicketOrderDlg", "Ticket Order #1", None))
        self.amountLabel.setText(_translate("TicketOrderDlg", "$", None))
        self.label_4.setText(_translate("TicketOrderDlg", "&Quantity:", None))
        self.label_3.setText(_translate("TicketOrderDlg", "&Price:", None))
        self.label_5.setText(_translate("TicketOrderDlg", "Amount", None))
        self.priceSpinBox.setPrefix(_translate("TicketOrderDlg", "$ ", None))
        self.label_2.setText(_translate("TicketOrderDlg", "&When:", None))
        self.label.setText(_translate("TicketOrderDlg", "&Customer:", None))

