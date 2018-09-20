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
import ships

MAC = "qt_mac_set_native_menubar" in dir()


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = ships.ShipTableModel("ships.dat")  # 创建 船_表_模型 对象

        tableLabel1 = QLabel("Table &1")
        self.tableView1 = QTableView()
        tableLabel1.setBuddy(self.tableView1)
        self.tableView1.setModel(self.model)    # 关联 船_表_模型
        self.tableView1.setItemDelegate(ships.ShipDelegate(self))   # 关联 船_委托(自定义):控制项的外观与使用的编辑器.

        tableLabel2 = QLabel("Table &2")
        self.tableView2 = QTableView()
        tableLabel2.setBuddy(self.tableView2)
        self.tableView2.setModel(self.model)
        self.tableView2.setItemDelegate(ships.ShipDelegate(self))

        addShipButton = QPushButton("&Add Ship")
        removeShipButton = QPushButton("&Remove Ship")
        quitButton = QPushButton("&Quit")
        if not MAC:
            addShipButton.setFocusPolicy(Qt.NoFocus)
            removeShipButton.setFocusPolicy(Qt.NoFocus)
            quitButton.setFocusPolicy(Qt.NoFocus)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)

        splitter = QSplitter(Qt.Horizontal)

        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel1)
        vbox.addWidget(self.tableView1)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)

        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel2)
        vbox.addWidget(self.tableView2)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        for tableView in (self.tableView1, self.tableView2):
            header = tableView.horizontalHeader()
            self.connect(header, SIGNAL("sectionClicked(int)"), self.sortTable)
        self.connect(addShipButton, SIGNAL("clicked()"), self.addShip)
        self.connect(removeShipButton, SIGNAL("clicked()"), self.removeShip)
        self.connect(quitButton, SIGNAL("clicked()"), self.accept)

        self.setWindowTitle("Ships (delegate)")
        QTimer.singleShot(0, self.initialLoad)

    def initialLoad(self):
        if not QFile.exists(self.model.filename):
            for ship in ships.generateFakeShips():
                self.model.ships.append(ship)
                self.model.owners.add(ship.owner)
                self.model.countries.add(ship.country)
            self.model.reset()  # 重置数据.(继承自父类的方法)
            self.model.dirty = False
        else:
            try:
                self.model.load()
            except IOError as e:
                QMessageBox.warning(self, "Ships - Error",
                        "Failed to load: {}".format(e))
        self.model.sortByName()
        self.resizeColumns()

    def resizeColumns(self):    # 调整列宽
        self.tableView1.resizeColumnsToContents()
        self.tableView2.resizeColumnsToContents()

    def reject(self):
        self.accept()

    def accept(self):
        if (self.model.dirty and
            QMessageBox.question(self, "Ships - Save?",
                    "Save unsaved changes?",
                    QMessageBox.Yes|QMessageBox.No) ==
                    QMessageBox.Yes):
            try:
                self.model.save()
            except IOError as e:
                QMessageBox.warning(self, "Ships - Error",
                        "Failed to save: {}".format(e))
        QDialog.accept(self)

    def sortTable(self, section):   # section::区段==int
        if section in (ships.OWNER, ships.COUNTRY):
            self.model.sortByCountryOwner()
        else:
            self.model.sortByName()
        self.resizeColumns()


    def addShip(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, 0)
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        tableView.setFocus()
        tableView.setCurrentIndex(index)
        tableView.edit(index)


    def removeShip(self):
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        index = tableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        name = self.model.data(
                    self.model.index(row, ships.NAME))
        owner = self.model.data(
                    self.model.index(row, ships.OWNER))
        country = self.model.data(
                    self.model.index(row, ships.COUNTRY))
        if (QMessageBox.question(self, "Ships - Remove", 
                "Remove {} of {}/{}?".format(name, owner, country),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            return
        self.model.removeRow(row)
        self.resizeColumns()


app = QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()

