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

MAC = "qt_mac_set_native_menubar" in dir()  # 判断是否在MAC系统.


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        listLabel = QLabel("&List")
        self.listWidget = QListWidget()  # 简便项视图控件.P313-1
        listLabel.setBuddy(self.listWidget)

        tableLabel = QLabel("&Table")
        self.tableWidget = QTableWidget()  # 简便项视图控件.P313-1
        tableLabel.setBuddy(self.tableWidget)

        treeLabel = QLabel("Tre&e")
        self.treeWidget = QTreeWidget()  # 简便项视图控件.P313-1
        treeLabel.setBuddy(self.treeWidget)

        addShipButton = QPushButton("&Add Ship")
        removeShipButton = QPushButton("&Remove Ship")
        quitButton = QPushButton("&Quit")
        if not MAC:
            addShipButton.setFocusPolicy(Qt.NoFocus)
            removeShipButton.setFocusPolicy(Qt.NoFocus)
            quitButton.setFocusPolicy(Qt.NoFocus)

        splitter = QSplitter(Qt.Horizontal)  # 创建分隔器
        vbox = QVBoxLayout()
        vbox.addWidget(listLabel)
        vbox.addWidget(self.listWidget)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel)
        vbox.addWidget(self.tableWidget)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        vbox = QVBoxLayout()
        vbox.addWidget(treeLabel)
        vbox.addWidget(self.treeWidget)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(self.tableWidget,
                SIGNAL("itemChanged(QTableWidgetItem*)"),
                self.tableItemChanged)
        self.connect(addShipButton, SIGNAL("clicked()"), self.addShip)
        self.connect(removeShipButton, SIGNAL("clicked()"), self.removeShip)
        self.connect(quitButton, SIGNAL("clicked()"), self.accept)

        self.ships = ships.ShipContainer("ships.dat")
        self.setWindowTitle("Ships (dict)")
        QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        if not QFile.exists(self.ships.filename):
            for ship in ships.generateFakeShips():
                self.ships.addShip(ship)
            self.ships.dirty = False
        else:
            try:
                self.ships.load()
            except IOError as e:
                QMessageBox.warning(self, "Ships - Error",
                        "Failed to load: {}".format(e))
        self.populateList()
        self.populateTable()
        self.tableWidget.sortItems(0)  # 排序_项
        self.populateTree()

    # X 键
    def reject(self):
        self.accept()


    def accept(self):
        if (self.ships.dirty and
            QMessageBox.question(self, "Ships - Save?",
                    "Save unsaved changes?",
                    QMessageBox.Yes|QMessageBox.No) ==
                    QMessageBox.Yes):
            try:
                self.ships.save()
            except IOError as e:
                QMessageBox.warning(self, "Ships - Error",
                        "Failed to save: {}".format(e))
        QDialog.accept(self)


    def populateList(self, selectedShip=None):
        selected = None
        self.listWidget.clear()
        for ship in self.ships.inOrder():
            item = QListWidgetItem("{} of {}/{} ({:,})".format(
                     ship.name, ship.owner, ship.country, ship.teu))
            self.listWidget.addItem(item)
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
        if selected is not None:
            selected.setSelected(True)
            self.listWidget.setCurrentItem(selected)


    def populateTable(self, selectedShip=None):
        selected = None
        self.tableWidget.clear()
        self.tableWidget.setSortingEnabled(False)   # 设置_排序_允许 == False
        self.tableWidget.setRowCount(len(self.ships))  # 设置行数
        headers = ["Name", "Owner", "Country", "Description", "TEU"]
        self.tableWidget.setColumnCount(len(headers))  # 设置列数
        self.tableWidget.setHorizontalHeaderLabels(headers)  # 设置表头标签
        for row, ship in enumerate(self.ships):
            item = QTableWidgetItem(ship.name)
            item.setData(Qt.UserRole, int(id(ship)))
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
            self.tableWidget.setItem(row, ships.NAME, item)
            self.tableWidget.setItem(row, ships.OWNER,
                    QTableWidgetItem(ship.owner))
            self.tableWidget.setItem(row, ships.COUNTRY,
                    QTableWidgetItem(ship.country))
            self.tableWidget.setItem(row, ships.DESCRIPTION,
                    QTableWidgetItem(ship.description))
            item = QTableWidgetItem("{:10}".format(ship.teu))   # "{:10}"::10 == 十进制
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.tableWidget.setItem(row, ships.TEU, item)
        self.tableWidget.setSortingEnabled(True)    # 设置_排序_允许 == True
        self.tableWidget.resizeColumnsToContents()  # 调整列宽适配内容
        if selected is not None:
            selected.setSelected(True)
            self.tableWidget.setCurrentItem(selected)


    def populateTree(self, selectedShip=None):
        selected = None
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(2)  # 设置列数 ==2
        self.treeWidget.setHeaderLabels(["Country/Owner/Name", "TEU"])  # 设置两列的标题.
        self.treeWidget.setItemsExpandable(True)    # 设置_项_可扩展(设置项是否可扩展)
        parentFromCountry = {}
        parentFromCountryOwner = {}
        for ship in self.ships.inCountryOwnerOrder():
            ancestor = parentFromCountry.get(ship.country)
            if ancestor is None:
                ancestor = QTreeWidgetItem(self.treeWidget, [ship.country])
                parentFromCountry[ship.country] = ancestor
            countryowner = ship.country + "/" + ship.owner
            parent = parentFromCountryOwner.get(countryowner)
            if parent is None:
                parent = QTreeWidgetItem(ancestor, [ship.owner])
                parentFromCountryOwner[countryowner] = parent
            item = QTreeWidgetItem(parent, [ship.name, "{:,}".format(ship.teu)])
            item.setTextAlignment(1, Qt.AlignRight|Qt.AlignVCenter)
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
            self.treeWidget.expandItem(parent)      # expandItem::展开_项
            self.treeWidget.expandItem(ancestor)
        self.treeWidget.resizeColumnToContents(0)   # 调整_0列宽适配内容
        self.treeWidget.resizeColumnToContents(1)   # 调整_1列宽适配内容
        if selected is not None:
            selected.setSelected(True)
            self.treeWidget.setCurrentItem(selected)


    def addShip(self):
        ship = ships.Ship(" Unknown", " Unknown", " Unknown")
        self.ships.addShip(ship)
        self.populateList()
        self.populateTree()
        self.populateTable(id(ship))
        self.tableWidget.setFocus()
        self.tableWidget.editItem(self.tableWidget.currentItem())


    def tableItemChanged(self, item):
        ship = self.currentTableShip()
        if ship is None:
            return
        column = self.tableWidget.currentColumn()
        if column == ships.NAME:
            ship.name = item.text().strip()  # strip::去除字符头尾空白字符.
        elif column == ships.OWNER:
            ship.owner = item.text().strip()
        elif column == ships.COUNTRY:
            ship.country = item.text().strip()
        elif column == ships.DESCRIPTION:
            ship.description = item.text().strip()
        elif column == ships.TEU:
            ship.teu = int(item.text())
        self.ships.dirty = True
        self.populateList()
        self.populateTree()


    def currentTableShip(self):  # 返回当前选定行(row)的Ship对象.
        item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if item is None:
            return None
        return self.ships.ship(int(item.data(Qt.UserRole)))


    def removeShip(self):
        ship = self.currentTableShip()
        if ship is None:
            return
        if (QMessageBox.question(self, "Ships - Remove", 
                "Remove {} of {}/{}?".format(ship.name, ship.owner, ship.country),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            return
        self.ships.removeShip(ship)
        self.populateList()
        self.populateTree()
        self.populateTable()


app = QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()

