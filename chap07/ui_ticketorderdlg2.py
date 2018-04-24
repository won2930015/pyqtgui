# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ticketorderdlg2.ui'
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
        TicketOrderDlg.resize(305, 233)
        self.gridlayout = QtGui.QGridLayout(TicketOrderDlg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        spacerItem = QtGui.QSpacerItem(20, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TicketOrderDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.customerLineEdit = QtGui.QLineEdit(TicketOrderDlg)
        self.customerLineEdit.setObjectName(_fromUtf8("customerLineEdit"))
        self.gridlayout1.addWidget(self.customerLineEdit, 0, 1, 1, 2)
        self.whenDateTimeEdit = QtGui.QDateTimeEdit(TicketOrderDlg)
        self.whenDateTimeEdit.setObjectName(_fromUtf8("whenDateTimeEdit"))
        self.gridlayout1.addWidget(self.whenDateTimeEdit, 1, 1, 1, 1)
        self.label = QtGui.QLabel(TicketOrderDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout1.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(TicketOrderDlg)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout1.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(74, 33, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem2, 1, 2, 1, 1)
        self.gridlayout.addLayout(self.gridlayout1, 0, 0, 1, 3)
        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setMargin(0)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName(_fromUtf8("gridlayout2"))
        self.priceSpinBox = QtGui.QDoubleSpinBox(TicketOrderDlg)
        self.priceSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.priceSpinBox.setMaximum(5000.0)
        self.priceSpinBox.setObjectName(_fromUtf8("priceSpinBox"))
        self.gridlayout2.addWidget(self.priceSpinBox, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(TicketOrderDlg)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(TicketOrderDlg)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridlayout2.addWidget(self.label_5, 2, 0, 1, 1)
        self.quantitySpinBox = QtGui.QSpinBox(TicketOrderDlg)
        self.quantitySpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.quantitySpinBox.setMaximum(50)
        self.quantitySpinBox.setMinimum(1)
        self.quantitySpinBox.setProperty("value", 1)
        self.quantitySpinBox.setObjectName(_fromUtf8("quantitySpinBox"))
        self.gridlayout2.addWidget(self.quantitySpinBox, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(TicketOrderDlg)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout2.addWidget(self.label_4, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem3, 3, 1, 1, 1)
        self.amountLabel = QtGui.QLabel(TicketOrderDlg)
        self.amountLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.amountLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.amountLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.amountLabel.setObjectName(_fromUtf8("amountLabel"))
        self.gridlayout2.addWidget(self.amountLabel, 2, 1, 1, 1)
        self.gridlayout.addLayout(self.gridlayout2, 1, 0, 2, 1)
        self.label.setBuddy(self.customerLineEdit)
        self.label_2.setBuddy(self.whenDateTimeEdit)
        self.label_3.setBuddy(self.priceSpinBox)
        self.label_4.setBuddy(self.quantitySpinBox)

        self.retranslateUi(TicketOrderDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TicketOrderDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TicketOrderDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(TicketOrderDlg)
        TicketOrderDlg.setTabOrder(self.customerLineEdit, self.whenDateTimeEdit)
        TicketOrderDlg.setTabOrder(self.whenDateTimeEdit, self.priceSpinBox)
        TicketOrderDlg.setTabOrder(self.priceSpinBox, self.quantitySpinBox)
        TicketOrderDlg.setTabOrder(self.quantitySpinBox, self.buttonBox)

    def retranslateUi(self, TicketOrderDlg):
        TicketOrderDlg.setWindowTitle(_translate("TicketOrderDlg", "Ticket Order #2", None))
        self.label.setText(_translate("TicketOrderDlg", "&Customer:", None))
        self.label_2.setText(_translate("TicketOrderDlg", "&When:", None))
        self.priceSpinBox.setPrefix(_translate("TicketOrderDlg", "$ ", None))
        self.label_3.setText(_translate("TicketOrderDlg", "&Price:", None))
        self.label_5.setText(_translate("TicketOrderDlg", "Amount", None))
        self.label_4.setText(_translate("TicketOrderDlg", "&Quantity:", None))
        self.amountLabel.setText(_translate("TicketOrderDlg", "$", None))

