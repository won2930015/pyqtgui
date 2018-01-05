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
import ships_ans

MAC = "qt_mac_set_native_menubar" in dir()  #判断是否在MAC系统.


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = ships_ans.ShipTableModel("ships.dat")  #创建模型.

        tableLabel1 = QLabel("Table &1")
        self.tableView1 = QTableView()
        tableLabel1.setBuddy(self.tableView1)
        self.tableView1.setModel(self.model)    #LOAD入模型.

        tableLabel2 = QLabel("Table &2")
        self.tableView2 = QTableView()
        tableLabel2.setBuddy(self.tableView2)
        self.tableView2.setModel(self.model)    #LOAD入模型.

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

        self.setWindowTitle("Ships (model)_ans")
        QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        if not QFile.exists(self.model.filename):
            for ship in ships_ans.generateFakeShips():
                self.model.ships_ans.append(ship)
                self.model.owners.add(ship.owner)
                self.model.countries.add(ship.country)
            self.model.reset()  #reset::重置(重置数据)
            self.model.dirty = False
        else:
            try:
                self.model.load()
            except IOError as e:
                QMessageBox.warning(self, "Ships - Error",
                        "Failed to load: {}".format(e))
        self.model.sortByName()
        self.resizeColumns()    #调整列宽适配内容.


    def resizeColumns(self):
        for tableView in (self.tableView1, self.tableView2):
            for column in (ships_ans.NAME, ships_ans.OWNER, ships_ans.COUNTRY,
                           ships_ans.TEU):
                tableView.resizeColumnToContents(column)


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

    
    def sortTable(self, section):   #排序表
        if section in (ships_ans.OWNER, ships_ans.COUNTRY):
            self.model.sortByCountryOwner()
        else:
            self.model.sortByName()
        self.resizeColumns()


    def addShip(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, 0)
        tableView = self.tableView1
        if self.tableView2.hasFocus():  #hasFocus::有_焦点
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
                    self.model.index(row, ships_ans.NAME))
        owner = self.model.data(
                    self.model.index(row, ships_ans.OWNER))
        country = self.model.data(
                    self.model.index(row, ships_ans.COUNTRY))
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

