# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\Users\won293_root\Desktop\qt_test\pyqtbook3.tar\pyqtbook31.tar\chap09\vehiclerentaldlg.ui'
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

class Ui_VehicleRentalDlg(object):
    def setupUi(self, VehicleRentalDlg):
        VehicleRentalDlg.setObjectName(_fromUtf8("VehicleRentalDlg"))
        VehicleRentalDlg.resize(206, 246)
        self.gridlayout = QtGui.QGridLayout(VehicleRentalDlg)  #创建网格布局
        self.gridlayout.setMargin(9)  # 设置边缘
        self.gridlayout.setSpacing(6)  # 设置间隔
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(VehicleRentalDlg)  # 创建按键盒
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)  # 设置方向
        # 设置包含的标准按键.
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 1)
        # 创建分隔器(弹簧)
        spacerItem = QtGui.QSpacerItem(188, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label_6 = QtGui.QLabel(VehicleRentalDlg)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.hboxlayout.addWidget(self.label_6)
        self.mileageLabel = QtGui.QLabel(VehicleRentalDlg)
        self.mileageLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mileageLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.mileageLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mileageLabel.setObjectName(_fromUtf8("mileageLabel"))
        self.hboxlayout.addWidget(self.mileageLabel)
        self.gridlayout.addLayout(self.hboxlayout, 2, 0, 1, 1)
        # ***创建堆叠控件***
        self.stackedWidget = QtGui.QStackedWidget(VehicleRentalDlg)  # 创建堆叠控件
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        # 创建堆叠页面2
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.gridlayout1 = QtGui.QGridLayout(self.page_2)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.colorComboBox = QtGui.QComboBox(self.page_2)
        self.colorComboBox.setObjectName(_fromUtf8("colorComboBox"))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.gridlayout1.addWidget(self.colorComboBox, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.page_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout1.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.page_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridlayout1.addWidget(self.label_5, 1, 0, 1, 1)
        self.seatsSpinBox = QtGui.QSpinBox(self.page_2)
        self.seatsSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.seatsSpinBox.setMinimum(2)
        self.seatsSpinBox.setMaximum(12)
        self.seatsSpinBox.setProperty("value", 4)
        self.seatsSpinBox.setObjectName(_fromUtf8("seatsSpinBox"))
        self.gridlayout1.addWidget(self.seatsSpinBox, 1, 1, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        # 堆叠页面1
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.gridlayout2 = QtGui.QGridLayout(self.page)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName(_fromUtf8("gridlayout2"))
        self.weightSpinBox = QtGui.QSpinBox(self.page)
        self.weightSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.weightSpinBox.setMinimum(1)
        self.weightSpinBox.setMaximum(8)
        self.weightSpinBox.setObjectName(_fromUtf8("weightSpinBox"))
        self.gridlayout2.addWidget(self.weightSpinBox, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.page)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout2.addWidget(self.label_2, 0, 0, 1, 1)
        self.volumeSpinBox = QtGui.QSpinBox(self.page)
        self.volumeSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.volumeSpinBox.setMinimum(4)
        self.volumeSpinBox.setMaximum(22)
        self.volumeSpinBox.setProperty("value", 10)
        self.volumeSpinBox.setObjectName(_fromUtf8("volumeSpinBox"))
        self.gridlayout2.addWidget(self.volumeSpinBox, 1, 1, 1, 1)
        self.stackedWidget.addWidget(self.page)
        # ***堆叠设置结束***
        self.gridlayout.addWidget(self.stackedWidget, 1, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.label = QtGui.QLabel(VehicleRentalDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout1.addWidget(self.label)
        self.vehicleComboBox = QtGui.QComboBox(VehicleRentalDlg)
        self.vehicleComboBox.setObjectName(_fromUtf8("vehicleComboBox"))
        self.vehicleComboBox.addItem(_fromUtf8(""))
        self.vehicleComboBox.addItem(_fromUtf8(""))
        self.hboxlayout1.addWidget(self.vehicleComboBox)
        self.gridlayout.addLayout(self.hboxlayout1, 0, 0, 1, 1)
        self.label_4.setBuddy(self.colorComboBox)
        self.label_5.setBuddy(self.seatsSpinBox)
        self.label_3.setBuddy(self.volumeSpinBox)
        self.label_2.setBuddy(self.seatsSpinBox)
        self.label.setBuddy(self.vehicleComboBox)

        self.retranslateUi(VehicleRentalDlg)  #  重译Ui
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.vehicleComboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.stackedWidget.setCurrentIndex)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VehicleRentalDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VehicleRentalDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(VehicleRentalDlg)
    #  重译Ui
    def retranslateUi(self, VehicleRentalDlg):
        VehicleRentalDlg.setWindowTitle(_translate("VehicleRentalDlg", "Vehicle Rental", None))
        self.label_6.setText(_translate("VehicleRentalDlg", "Max. Mileage:", None))
        self.mileageLabel.setText(_translate("VehicleRentalDlg", "1000 miles", None))
        self.colorComboBox.setItemText(0, _translate("VehicleRentalDlg", "Black", None))
        self.colorComboBox.setItemText(1, _translate("VehicleRentalDlg", "Blue", None))
        self.colorComboBox.setItemText(2, _translate("VehicleRentalDlg", "Green", None))
        self.colorComboBox.setItemText(3, _translate("VehicleRentalDlg", "Red", None))
        self.colorComboBox.setItemText(4, _translate("VehicleRentalDlg", "Silver", None))
        self.colorComboBox.setItemText(5, _translate("VehicleRentalDlg", "White", None))
        self.colorComboBox.setItemText(6, _translate("VehicleRentalDlg", "Yellow", None))
        self.label_4.setText(_translate("VehicleRentalDlg", "Co&lor:", None))
        self.label_5.setText(_translate("VehicleRentalDlg", "&Seats:", None))
        self.weightSpinBox.setSuffix(_translate("VehicleRentalDlg", " tons", None))
        self.label_3.setText(_translate("VehicleRentalDlg", "Volu&me:", None))
        self.label_2.setText(_translate("VehicleRentalDlg", "&Weight:", None))
        self.volumeSpinBox.setSuffix(_translate("VehicleRentalDlg", " cu m", None))
        self.label.setText(_translate("VehicleRentalDlg", "&Vehicle Type:", None))
        self.vehicleComboBox.setItemText(0, _translate("VehicleRentalDlg", "Car", None))
        self.vehicleComboBox.setItemText(1, _translate("VehicleRentalDlg", "Van", None))

