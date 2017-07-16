# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\Users\won293_root\Desktop\qt_test\pyqtbook3.tar\pyqtbook31.tar\pyqtbook31\pyqtbook31\chap08\addeditmoviedlg_ans.ui'
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

class Ui_AddEditMovieDlg(object):
    def setupUi(self, AddEditMovieDlg):
        AddEditMovieDlg.setObjectName(_fromUtf8("AddEditMovieDlg"))
        AddEditMovieDlg.resize(484, 417)
        self.gridlayout = QtGui.QGridLayout(AddEditMovieDlg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(AddEditMovieDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 5, 4, 1, 2)
        self.locationLineEdit = QtGui.QLineEdit(AddEditMovieDlg)
        self.locationLineEdit.setObjectName(_fromUtf8("locationLineEdit"))
        self.gridlayout.addWidget(self.locationLineEdit, 2, 4, 1, 2)
        self.acquiredDateEdit = QtGui.QDateEdit(AddEditMovieDlg)
        self.acquiredDateEdit.setAlignment(QtCore.Qt.AlignRight)
        self.acquiredDateEdit.setObjectName(_fromUtf8("acquiredDateEdit"))
        self.gridlayout.addWidget(self.acquiredDateEdit, 1, 4, 1, 1)
        self.label = QtGui.QLabel(AddEditMovieDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.titleLineEdit = QtGui.QLineEdit(AddEditMovieDlg)
        self.titleLineEdit.setObjectName(_fromUtf8("titleLineEdit"))
        self.gridlayout.addWidget(self.titleLineEdit, 0, 1, 1, 5)
        self.label_5 = QtGui.QLabel(AddEditMovieDlg)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridlayout.addWidget(self.label_5, 3, 0, 1, 3)
        self.notesTextEdit = QtGui.QTextEdit(AddEditMovieDlg)
        self.notesTextEdit.setTabChangesFocus(True)
        self.notesTextEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.notesTextEdit.setAcceptRichText(False)
        self.notesTextEdit.setObjectName(_fromUtf8("notesTextEdit"))
        self.gridlayout.addWidget(self.notesTextEdit, 4, 0, 1, 6)
        self.label_3 = QtGui.QLabel(AddEditMovieDlg)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout.addWidget(self.label_3, 2, 0, 1, 2)
        self.minutesSpinBox = QtGui.QSpinBox(AddEditMovieDlg)
        self.minutesSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.minutesSpinBox.setMaximum(720)
        self.minutesSpinBox.setObjectName(_fromUtf8("minutesSpinBox"))
        self.gridlayout.addWidget(self.minutesSpinBox, 2, 2, 1, 1)
        self.label_6 = QtGui.QLabel(AddEditMovieDlg)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridlayout.addWidget(self.label_6, 2, 3, 1, 1)
        self.label_4 = QtGui.QLabel(AddEditMovieDlg)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 1, 3, 1, 1)
        self.yearSpinBox = QtGui.QSpinBox(AddEditMovieDlg)
        self.yearSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.yearSpinBox.setMaximum(2100)
        self.yearSpinBox.setMinimum(1890)
        self.yearSpinBox.setProperty("value", 1890)
        self.yearSpinBox.setObjectName(_fromUtf8("yearSpinBox"))
        self.gridlayout.addWidget(self.yearSpinBox, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(AddEditMovieDlg)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 1, 5, 1, 1)
        self.label.setBuddy(self.titleLineEdit)
        self.label_5.setBuddy(self.notesTextEdit)
        self.label_3.setBuddy(self.minutesSpinBox)
        self.label_6.setBuddy(self.locationLineEdit)
        self.label_4.setBuddy(self.acquiredDateEdit)
        self.label_2.setBuddy(self.yearSpinBox)

        self.retranslateUi(AddEditMovieDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddEditMovieDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddEditMovieDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(AddEditMovieDlg)
        AddEditMovieDlg.setTabOrder(self.titleLineEdit, self.yearSpinBox)
        AddEditMovieDlg.setTabOrder(self.yearSpinBox, self.minutesSpinBox)
        AddEditMovieDlg.setTabOrder(self.minutesSpinBox, self.acquiredDateEdit)
        AddEditMovieDlg.setTabOrder(self.acquiredDateEdit, self.locationLineEdit)
        AddEditMovieDlg.setTabOrder(self.locationLineEdit, self.notesTextEdit)

    def retranslateUi(self, AddEditMovieDlg):
        AddEditMovieDlg.setWindowTitle(_translate("AddEditMovieDlg", "My Movies - Add Movie", None))
        self.acquiredDateEdit.setDisplayFormat(_translate("AddEditMovieDlg", "ddd MMM d, yyyy", None))
        self.label.setText(_translate("AddEditMovieDlg", "&Title:", None))
        self.label_5.setText(_translate("AddEditMovieDlg", "&Notes:", None))
        self.label_3.setText(_translate("AddEditMovieDlg", "&Minutes:", None))
        self.minutesSpinBox.setSpecialValueText(_translate("AddEditMovieDlg", "Unknown", None))
        self.label_6.setText(_translate("AddEditMovieDlg", "&Location:", None))
        self.label_4.setText(_translate("AddEditMovieDlg", "A&cquired:", None))
        self.yearSpinBox.setSpecialValueText(_translate("AddEditMovieDlg", "Unknown", None))
        self.label_2.setText(_translate("AddEditMovieDlg", "&Year:", None))

