# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\Users\won293_root\Desktop\qt_test\pyqtbook3.tar\pyqtbook31.tar\chap09\findandreplacedlg.ui'
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

class Ui_FindAndReplaceDlg(object):
    def setupUi(self, FindAndReplaceDlg):
        FindAndReplaceDlg.setObjectName(_fromUtf8("FindAndReplaceDlg"))
        FindAndReplaceDlg.resize(355, 274)
        self.hboxlayout = QtGui.QHBoxLayout(FindAndReplaceDlg)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.replaceLineEdit = QtGui.QLineEdit(FindAndReplaceDlg)
        self.replaceLineEdit.setObjectName(_fromUtf8("replaceLineEdit"))
        self.gridlayout.addWidget(self.replaceLineEdit, 1, 1, 1, 1)
        self.findLineEdit = QtGui.QLineEdit(FindAndReplaceDlg)
        self.findLineEdit.setObjectName(_fromUtf8("findLineEdit"))
        self.gridlayout.addWidget(self.findLineEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(FindAndReplaceDlg)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(FindAndReplaceDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.vboxlayout.addLayout(self.gridlayout)
        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.caseCheckBox = QtGui.QCheckBox(FindAndReplaceDlg)
        self.caseCheckBox.setObjectName(_fromUtf8("caseCheckBox"))
        self.vboxlayout1.addWidget(self.caseCheckBox)
        self.wholeCheckBox = QtGui.QCheckBox(FindAndReplaceDlg)
        self.wholeCheckBox.setChecked(True)
        self.wholeCheckBox.setObjectName(_fromUtf8("wholeCheckBox"))
        self.vboxlayout1.addWidget(self.wholeCheckBox)
        self.vboxlayout.addLayout(self.vboxlayout1)
        spacerItem = QtGui.QSpacerItem(231, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.moreFrame = QtGui.QFrame(FindAndReplaceDlg)
        self.moreFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.moreFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.moreFrame.setObjectName(_fromUtf8("moreFrame"))
        self.vboxlayout2 = QtGui.QVBoxLayout(self.moreFrame)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
        self.backwardsCheckBox = QtGui.QCheckBox(self.moreFrame)
        self.backwardsCheckBox.setObjectName(_fromUtf8("backwardsCheckBox"))
        self.vboxlayout2.addWidget(self.backwardsCheckBox)
        self.regexCheckBox = QtGui.QCheckBox(self.moreFrame)
        self.regexCheckBox.setObjectName(_fromUtf8("regexCheckBox"))
        self.vboxlayout2.addWidget(self.regexCheckBox)
        self.ignoreNotesCheckBox = QtGui.QCheckBox(self.moreFrame)
        self.ignoreNotesCheckBox.setObjectName(_fromUtf8("ignoreNotesCheckBox"))
        self.vboxlayout2.addWidget(self.ignoreNotesCheckBox)
        self.vboxlayout.addWidget(self.moreFrame)
        self.hboxlayout.addLayout(self.vboxlayout)
        self.line = QtGui.QFrame(FindAndReplaceDlg)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.hboxlayout.addWidget(self.line)
        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setMargin(0)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName(_fromUtf8("vboxlayout3"))
        self.findButton = QtGui.QPushButton(FindAndReplaceDlg)
        self.findButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.findButton.setObjectName(_fromUtf8("findButton"))
        self.vboxlayout3.addWidget(self.findButton)
        self.replaceButton = QtGui.QPushButton(FindAndReplaceDlg)
        self.replaceButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.replaceButton.setObjectName(_fromUtf8("replaceButton"))
        self.vboxlayout3.addWidget(self.replaceButton)
        self.closeButton = QtGui.QPushButton(FindAndReplaceDlg)
        self.closeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.vboxlayout3.addWidget(self.closeButton)
        self.moreButton = QtGui.QPushButton(FindAndReplaceDlg)
        self.moreButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.moreButton.setCheckable(True)
        self.moreButton.setObjectName(_fromUtf8("moreButton"))
        self.vboxlayout3.addWidget(self.moreButton)
        spacerItem1 = QtGui.QSpacerItem(21, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout3.addItem(spacerItem1)
        self.hboxlayout.addLayout(self.vboxlayout3)
        self.label_2.setBuddy(self.replaceLineEdit)
        self.label.setBuddy(self.findLineEdit)

        self.retranslateUi(FindAndReplaceDlg)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), FindAndReplaceDlg.reject)
        QtCore.QObject.connect(self.moreButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.moreFrame.setVisible)
        QtCore.QMetaObject.connectSlotsByName(FindAndReplaceDlg)
        FindAndReplaceDlg.setTabOrder(self.findLineEdit, self.replaceLineEdit)
        FindAndReplaceDlg.setTabOrder(self.replaceLineEdit, self.caseCheckBox)
        FindAndReplaceDlg.setTabOrder(self.caseCheckBox, self.wholeCheckBox)
        FindAndReplaceDlg.setTabOrder(self.wholeCheckBox, self.backwardsCheckBox)
        FindAndReplaceDlg.setTabOrder(self.backwardsCheckBox, self.regexCheckBox)
        FindAndReplaceDlg.setTabOrder(self.regexCheckBox, self.ignoreNotesCheckBox)

    def retranslateUi(self, FindAndReplaceDlg):
        FindAndReplaceDlg.setWindowTitle(_translate("FindAndReplaceDlg", "Find and Replace", None))
        self.label_2.setText(_translate("FindAndReplaceDlg", "Replace w&ith:", None))
        self.label.setText(_translate("FindAndReplaceDlg", "Find &what:", None))
        self.caseCheckBox.setText(_translate("FindAndReplaceDlg", "&Case sensitive", None))
        self.wholeCheckBox.setText(_translate("FindAndReplaceDlg", "Wh&ole words", None))
        self.backwardsCheckBox.setText(_translate("FindAndReplaceDlg", "Search &Backwards", None))
        self.regexCheckBox.setText(_translate("FindAndReplaceDlg", "Regular E&xpression", None))
        self.ignoreNotesCheckBox.setText(_translate("FindAndReplaceDlg", "Ignore foot&notes and endnotes", None))
        self.findButton.setText(_translate("FindAndReplaceDlg", "&Find", None))
        self.replaceButton.setText(_translate("FindAndReplaceDlg", "&Replace", None))
        self.closeButton.setText(_translate("FindAndReplaceDlg", "Close", None))
        self.moreButton.setText(_translate("FindAndReplaceDlg", "&More", None))

