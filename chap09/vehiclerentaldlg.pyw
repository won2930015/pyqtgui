#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class VehicleRentalDlg(QDialog):

    def __init__(self, parent=None):
        super(VehicleRentalDlg, self).__init__(parent)

        vehicleLabel = QLabel("&Vehicle Type:")
        self.vehicleComboBox = QComboBox()
        vehicleLabel.setBuddy(self.vehicleComboBox)
        self.vehicleComboBox.addItems(["Car", "Van"])
        colorLabel = QLabel("Co&lor:")
        self.colorComboBox = QComboBox()
        colorLabel.setBuddy(self.colorComboBox)
        self.colorComboBox.addItems(["Black", "Blue", "Green", "Red",
                                     "Silver", "White", "Yellow"])
        seatsLabel = QLabel("&Seats:")
        self.seatsSpinBox = QSpinBox()
        seatsLabel.setBuddy(self.seatsSpinBox)
        self.seatsSpinBox.setRange(2, 12)
        self.seatsSpinBox.setValue(4)
        self.seatsSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        weightLabel = QLabel("&Weight:")
        self.weightSpinBox = QSpinBox()
        weightLabel.setBuddy(self.weightSpinBox)
        self.weightSpinBox.setRange(1, 8)
        self.weightSpinBox.setValue(1)
        self.weightSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.weightSpinBox.setSuffix(" tons")   #设置后缀为：tons
        volumeLabel = QLabel("Volu&me")
        self.volumeSpinBox = QSpinBox()
        volumeLabel.setBuddy(self.volumeSpinBox)
        self.volumeSpinBox.setRange(4, 22)
        self.volumeSpinBox.setValue(10)
        self.volumeSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.volumeSpinBox.setSuffix(" cu m")   #设置后缀为： cu m
        mileageLabel = QLabel("Max. Mileage")
        self.mileageLabel = QLabel("1000 miles")
        self.mileageLabel.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.mileageLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)   ### setFrameStyle：设置_框架_样式||QFrame.StyledPanel:样式_面板||QFrame.Sunken:凹陷
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        # ***堆叠窗口 开始***
        self.stackedWidget = QStackedWidget()       #创建堆叠窗口。
        carWidget = QWidget()
        carLayout = QGridLayout()
        carLayout.addWidget(colorLabel, 0, 0)
        carLayout.addWidget(self.colorComboBox, 0, 1)
        carLayout.addWidget(seatsLabel, 1, 0)
        carLayout.addWidget(self.seatsSpinBox, 1, 1)
        carWidget.setLayout(carLayout)
        self.stackedWidget.addWidget(carWidget)
        vanWidget = QWidget()
        vanLayout = QGridLayout()
        vanLayout.addWidget(weightLabel, 0, 0)
        vanLayout.addWidget(self.weightSpinBox, 0, 1)
        vanLayout.addWidget(volumeLabel, 1, 0)
        vanLayout.addWidget(self.volumeSpinBox, 1, 1)
        vanWidget.setLayout(vanLayout)
        self.stackedWidget.addWidget(vanWidget)
        # ***堆叠窗口 结束***

        topLayout = QHBoxLayout()   #  顶部布局
        topLayout.addWidget(vehicleLabel)
        topLayout.addWidget(self.vehicleComboBox)
        bottomLayout = QHBoxLayout()    #bottomLayout：底部布局
        bottomLayout.addWidget(mileageLabel)
        bottomLayout.addWidget(self.mileageLabel)
        layout = QVBoxLayout()
        layout.addLayout(topLayout)  # 加入顶部布局
        layout.addWidget(self.stackedWidget)  # 加入堆叠窗口
        layout.addLayout(bottomLayout)  # 加入底部布局
        layout.addWidget(self.buttonBox)  # 加入按键盒
        self.setLayout(layout)  # 设置布局

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        self.connect(self.vehicleComboBox,
                     SIGNAL("currentIndexChanged(QString)"),
                     self.setWidgetStack)   #自定义函数->100 row
        self.connect(self.weightSpinBox, SIGNAL("valueChanged(int)"),
                     self.weightChanged)

        self.setWindowTitle("Vehicle Rental")


    def setWidgetStack(self, text):
        if text == "Car":
            self.stackedWidget.setCurrentIndex(0)
            self.mileageLabel.setText("1000 miles")
        else:
            self.stackedWidget.setCurrentIndex(1)
            self.weightChanged(self.weightSpinBox.value())


    def weightChanged(self, amount):
        self.mileageLabel.setText("{} miles".format(8000 / amount))


app = QApplication(sys.argv)
form = VehicleRentalDlg()
form.show()
app.exec_()

