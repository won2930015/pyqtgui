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

import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import qrc_resources

MAC = True
try:
    from PyQt4.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

# ASSETID::资产ID, CATEGORYID:种类ID, DATE::日期, DESCRIPTION::描述, ROOM::房间, ACTIONID::动作ID
ID = 0
NAME = ASSETID = 1
CATEGORYID = DATE = DESCRIPTION = 2
ROOM = ACTIONID = 3

ACQUIRED = 1  # 取得


def createFakeData():   # 创建伪数据.
    import random

    print("Dropping tables...")  # 译文：删除表……
    query = QSqlQuery()
    query.exec_("DROP TABLE assets")    # 资产_表
    query.exec_("DROP TABLE logs")      # 日志_表
    query.exec_("DROP TABLE actions")   # 动作_表
    query.exec_("DROP TABLE categories")  # 种类_表
    QApplication.processEvents()    # processEvents::进程_事件

    print("Creating tables...")  # 创建_表
    query.exec_("""CREATE TABLE actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(20) NOT NULL,
                description VARCHAR(40) NOT NULL)""")
    query.exec_("""CREATE TABLE categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(20) NOT NULL,
                description VARCHAR(40) NOT NULL)""")
    query.exec_("""CREATE TABLE assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL,
                categoryid INTEGER NOT NULL,
                room VARCHAR(4) NOT NULL,
                FOREIGN KEY (categoryid) REFERENCES categories)""")
    query.exec_("""CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                assetid INTEGER NOT NULL,
                date DATE NOT NULL,
                actionid INTEGER NOT NULL,
                FOREIGN KEY (assetid) REFERENCES assets,
                FOREIGN KEY (actionid) REFERENCES actions)""")
    QApplication.processEvents()

    print("Populating tables...")   # 译文：填充表……

    # 填充动作表
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Acquired', 'When installed')")   # Acquired::取得
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Broken', 'When failed and unusable')")    # Broken::损坏
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Repaired', 'When back in service')")  # Repaired::修理
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Routine maintenance', "   # Routine maintenance::例行维修
                "'When tested, refilled, etc.')")

    # 填充类别表
    query.exec_("INSERT INTO categories (name, description) VALUES "
                "('Computer Equipment', "
                "'Monitors, System Units, Peripherals, etc.')")  # Computer Equipment::电脑_设备
    query.exec_("INSERT INTO categories (name, description) VALUES "
                "('Furniture', 'Chairs, Tables, Desks, etc.')")  # Furniture::家具
    query.exec_("INSERT INTO categories (name, description) VALUES "
                "('Electrical Equipment', 'Non-computer electricals')")  # Electrical Equipment::电器_设备

    today = QDate.currentDate()

    # 楼层(创建一个列表,排除13层.)
    floors = list(range(1, 12)) + list(range(14, 28))

    # 资产清单::电脑相关==1, 家具==2 ,电器==3
    # 显示器
    monitors = (('17" LCD Monitor', 1),
                ('20" LCD Monitor', 1),
                ('21" LCD Monitor', 1),
                ('21" CRT Monitor', 1),
                ('24" CRT Monitor', 1))
    # 电脑:1
    computers = (("Computer (32-bit/80GB/0.5GB)", 1),
                 ("Computer (32-bit/100GB/1GB)", 1),
                 ("Computer (32-bit/120GB/1GB)", 1),
                 ("Computer (64-bit/240GB/2GB)", 1),
                 ("Computer (64-bit/320GB/4GB)", 1))
    # 打印机:1
    printers = (("Laser Printer (4 ppm)", 1),
                ("Laser Printer (6 ppm)", 1),
                ("Laser Printer (8 ppm)", 1),
                ("Laser Printer (16 ppm)", 1))
    # 椅子:2
    chairs = (("Secretary Chair", 2),
              ("Executive Chair (Basic)", 2),
              ("Executive Chair (Ergonimic)", 2),
              ("Executive Chair (Hi-Tech)", 2))
    # 桌子:2
    desks = (("Desk (Basic, 3 drawer)", 2),
             ("Desk (Standard, 3 drawer)", 2),
             ("Desk (Executive, 3 drawer)", 2),
             ("Desk (Executive, 4 drawer)", 2),
             ("Desk (Large, 4 drawer)", 2))
    # 家具:2
    furniture = (("Filing Cabinet (3 drawer)", 2),
                 ("Filing Cabinet (4 drawer)", 2),
                 ("Filing Cabinet (5 drawer)", 2),
                 ("Bookcase (4 shelves)", 2),
                 ("Bookcase (6 shelves)", 2),
                 ("Table (4 seater)", 2),
                 ("Table (8 seater)", 2),
                 ("Table (12 seater)", 2))
    # 电器:3
    electrical = (("Fan (3 speed)", 3),
                  ("Fan (5 speed)", 3),
                  ("Photocopier (4 ppm)", 3),
                  ("Photocopier (6 ppm)", 3),
                  ("Photocopier (8 ppm)", 3),
                  ("Shredder", 3))
    # 填充资产表和日志表
    query.prepare("INSERT INTO assets (name, categoryid, room) "
                  "VALUES (:name, :categoryid, :room)")
    logQuery = QSqlQuery()
    logQuery.prepare("INSERT INTO logs (assetid, date, actionid) "
                     "VALUES (:assetid, :date, :actionid)")
    assetid = 1
    for i in range(20):
        room = "{0:02d}{1:02d}".format(
                random.choice(floors), random.randint(1, 62))  # 返回随机楼层, 房号.
        for name, category in (random.choice(monitors),
                random.choice(computers), random.choice(chairs),
                random.choice(desks), random.choice(furniture)):
            query.bindValue(":name", name)
            query.bindValue(":categoryid", category)
            query.bindValue(":room", room)
            query.exec_()
            logQuery.bindValue(":assetid", assetid)
            when = today.addDays(-random.randint(7, 1500))
            logQuery.bindValue(":date", when)
            logQuery.bindValue(":actionid", ACQUIRED)
            logQuery.exec_()
            if random.random() > 0.7:
                logQuery.bindValue(":assetid", assetid)
                when = when.addDays(random.randint(1, 1500))
                if when <= today:
                    logQuery.bindValue(":date", when)
                    logQuery.bindValue(":actionid",
                            random.choice((2, 4)))
                    logQuery.exec_()
            assetid += 1
        if random.random() > 0.8:
            name, category = random.choice(printers)
            query.bindValue(":name", name)
            query.bindValue(":categoryid", category)
            query.bindValue(":room", room)
            query.exec_()
            logQuery.bindValue(":assetid", assetid)
            when = today.addDays(-random.randint(7, 1500))
            logQuery.bindValue(":date", when)
            logQuery.bindValue(":actionid", ACQUIRED)
            logQuery.exec_()
            if random.random() > 0.6:
                logQuery.bindValue(":assetid", assetid)
                when = when.addDays(random.randint(1, 1500))
                if when <= today:
                    logQuery.bindValue(":date", when)
                    logQuery.bindValue(":actionid",
                            random.choice((2, 4)))
                    logQuery.exec_()
            assetid += 1
        if random.random() > 0.6:
            name, category = random.choice(electrical)
            query.bindValue(":name", name)
            query.bindValue(":categoryid", category)
            query.bindValue(":room", room)
            query.exec_()
            logQuery.bindValue(":assetid", assetid)
            when = today.addDays(-random.randint(7, 1500))
            logQuery.bindValue(":date", when)
            logQuery.bindValue(":actionid", ACQUIRED)
            logQuery.exec_()
            if random.random() > 0.5:
                logQuery.bindValue(":assetid", assetid)
                when = when.addDays(random.randint(1, 1500))
                if when <= today:
                    logQuery.bindValue(":date", when)
                    logQuery.bindValue(":actionid",
                            random.choice((2, 4)))
                    logQuery.exec_()
            assetid += 1
        QApplication.processEvents()

    print("Assets:")
    query.exec_("SELECT id, name, categoryid, room FROM assets "
                "ORDER by id")
    categoryQuery = QSqlQuery()
    while query.next():
        id = int(query.value(0))
        name = query.value(1)
        categoryid = int(query.value(2))
        room = query.value(3)
        categoryQuery.exec_("SELECT name FROM categories "
                "WHERE id = {}".format(categoryid))
        category = "{}".format(categoryid)
        if categoryQuery.next():
            category = categoryQuery.value(0)
        print("{0}: {1} [{2}] {3}".format(id, name, category, room))
    QApplication.processEvents()


class ReferenceDataDlg(QDialog):    # 引用_数据_窗口::继承Dialog(对话框)窗口

    def __init__(self, table, title, parent=None):
        super(ReferenceDataDlg, self).__init__(parent)

        self.model = QSqlTableModel(self)
        self.model.setTable(table)  # setTable::设置_表(载入数据库表)
        self.model.setSort(NAME, Qt.AscendingOrder)  # setSort::设置_排序,(栏目,升序排序)
        self.model.setHeaderData(ID, Qt.Horizontal, "ID")   # setHeaderData::设置_表头_数据
        self.model.setHeaderData(NAME, Qt.Horizontal, "Name")
        self.model.setHeaderData(DESCRIPTION, Qt.Horizontal, "Description")
        self.model.select()  # 填充表.

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QTableView.SingleSelection)  # SingleSelection::单选
        self.view.setSelectionBehavior(QTableView.SelectRows)   # setSelectionBehavior::设置_选择_行为, SelectRows::行_选择
        self.view.setColumnHidden(ID, True)  # setColumnHidden::设置_列_隐藏(隐藏列.)
        self.view.resizeColumnsToContents()  # 重置_列_适配到内容

        addButton = QPushButton("&Add")
        deleteButton = QPushButton("&Delete")
        okButton = QPushButton("&OK")
        if not MAC:
            addButton.setFocusPolicy(Qt.NoFocus)
            deleteButton.setFocusPolicy(Qt.NoFocus)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(addButton, SIGNAL("clicked()"), self.addRecord)
        self.connect(deleteButton, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(okButton, SIGNAL("clicked()"), self.accept)  # accept::自带内置方法.

        self.setWindowTitle("Asset Manager - Edit {} Reference Data".format(title))


    def addRecord(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, NAME)
        self.view.setCurrentIndex(index)
        self.view.edit(index)


    def deleteRecord(self):  # 删除_记录
        index = self.view.currentIndex()
        if not index.isValid():
            return
        # QSqlDatabase.database().transaction()  # 事务(开始事务???)
        record = self.model.record(index.row())
        id = int(record.value(ID))
        table = self.model.tableName()
        query = QSqlQuery()
        if table == "actions":
            query.exec_("SELECT COUNT(*) FROM logs "
                        "WHERE actionid = {}".format(id))
        elif table == "categories":
            query.exec_("SELECT COUNT(*) FROM assets "
                        "WHERE categoryid = {}".format(id))
        count = 0
        if query.next():
            count = int(query.value(0))
        if count:   # 如果 日志表(logs)或资产表(assets)有该 动作/种类 记录的,弹出信息不删除该记录.
            QMessageBox.information(self,
                    "Delete {}".format(table),
                    "Cannot delete {}<br>"
                    "from the {} table because it is used by "
                    "{} records".format(
                    record.value(NAME), table, count))
            # QSqlDatabase.database().rollback()  # 回滚事务
            return
        self.model.removeRow(index.row())
        self.model.submitAll()  # 提交_全部::更新数据库.
        # QSqlDatabase.database().commit()  # 提交


class AssetDelegate(QSqlRelationalDelegate):  # AssetDelegate::资产_委托

    def __init__(self, parent=None):
        super(AssetDelegate, self).__init__(parent)

    # 显示ROOM(房间)列时设置为 右中对齐.
    def paint(self, painter, option, index):
        myoption = QStyleOptionViewItem(option)  # 样式选项_视图_项:: 创建视图项 的样式选项对象.
        if index.column() == ROOM:
            myoption.displayAlignment |= (Qt.AlignRight|Qt.AlignVCenter)
        QSqlRelationalDelegate.paint(self, painter, myoption, index)


    def createEditor(self, parent, option, index):
        if index.column() == ROOM:
            editor = QLineEdit(parent)
            regex = QRegExp(r"(?:0[1-9]|1[0124-9]|2[0-7])"           # 层数
                                   r"(?:0[1-9]|[1-5][0-9]|6[012])")  # 房号
            validator = QRegExpValidator(regex, parent)  # 创建验证器
            editor.setValidator(validator)  # 设置验证器
            editor.setInputMask("9999")  # 设置_输入_掩码.
            editor.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return editor
        else:
            return QSqlRelationalDelegate.createEditor(self, parent,
                                                       option, index)

    def setEditorData(self, editor, index):  # 从 资产模型表 读room(房间)域 数据填充到editor控件中.
        if index.column() == ROOM:
            text = index.model().data(index, Qt.DisplayRole)
            editor.setText(text)
        else:
            QSqlRelationalDelegate.setEditorData(self, editor, index)


    def setModelData(self, editor, model, index):   # 将editor数据填充到 资产模型表 中.
        if index.column() == ROOM:
            model.setData(index, editor.text())
        else:
            QSqlRelationalDelegate.setModelData(self, editor, model, index)


class LogDelegate(QSqlRelationalDelegate):  #LogDelegate::日志_委托

    def __init__(self, parent=None):
        super(LogDelegate, self).__init__(parent)


    def paint(self, painter, option, index):
        myoption = QStyleOptionViewItem(option)  # 样式选项_视图_项:: 创建视图项 的样式选项对象.
        if index.column() == DATE:  # DATE(日期)列 显示时右中对齐.
            myoption.displayAlignment |= (Qt.AlignRight|Qt.AlignVCenter)
        QSqlRelationalDelegate.paint(self, painter, myoption, index)


    def createEditor(self, parent, option, index):
        if index.column() == ACTIONID:  # 是actionid(动作id)列时...
            text = index.model().data(index, Qt.DisplayRole)
            # if text.isdigit() and int(text) == ACQUIRED:    # isdigit::is数字
            if not isinstance(text, QPyNullVariant) and text.isdigit() and int(text) == ACQUIRED:    # isdigit::is数字
                print(int(text))
                return  # Acquired is read-only::译:取得 是 只读的.
        if index.column() == DATE:
            editor = QDateEdit(parent)
            editor.setMaximumDate(QDate.currentDate())
            editor.setDisplayFormat("yyyy-MM-dd")
            if PYQT_VERSION_STR >= "4.1.0":
                editor.setCalendarPopup(True)   # 设置_日期_popup窗口 ==True
            editor.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
            return editor
        else:
            return QSqlRelationalDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        if index.column() == DATE:
            str_date = index.model().data(index, Qt.DisplayRole)  # <<<日期转换失败.没法修改日期...
            date = QDate.fromString(str(str_date),"yyyy-MM-dd" )
            editor.setDate(date)
        else:
            QSqlRelationalDelegate.setEditorData(self, editor, index)


    def setModelData(self, editor, model, index):
        if index.column() == DATE:
            model.setData(index, editor.date())
        else:
            QSqlRelationalDelegate.setModelData(self, editor, model,
                                                index)


class MainForm(QDialog):

    def __init__(self):
        super(MainForm, self).__init__()

        self.assetModel = QSqlRelationalTableModel(self)    # SqlRelationalTableModel::sql_关系_表_模型.
        self.assetModel.setTable("assets")  # setTable::设置_表
        self.assetModel.setRelation(CATEGORYID,
                QSqlRelation("categories", "id", "name"))
        self.assetModel.setSort(ROOM, Qt.AscendingOrder)    # AscendingOrder::升序排序
        self.assetModel.setHeaderData(ID, Qt.Horizontal, "ID")
        self.assetModel.setHeaderData(NAME, Qt.Horizontal, "Name")
        self.assetModel.setHeaderData(CATEGORYID, Qt.Horizontal, "Category")
        self.assetModel.setHeaderData(ROOM, Qt.Horizontal, "Room")
        self.assetModel.select()    # 填充表

        self.assetView = QTableView()
        self.assetView.setModel(self.assetModel)
        self.assetView.setItemDelegate(AssetDelegate(self))
        self.assetView.setSelectionMode(QTableView.SingleSelection)  # setSelectionMode::设置_选择_模式, SingleSelection::单选
        self.assetView.setSelectionBehavior(QTableView.SelectRows)  # setSelectionBehavior::设置_选择_行为
        self.assetView.setColumnHidden(ID, True)    # setColumnHidden::设置_列_隐藏(将ID列设为隐藏).
        self.assetView.resizeColumnsToContents()
        assetLabel = QLabel("A&ssets")
        assetLabel.setBuddy(self.assetView)

        self.logModel = QSqlRelationalTableModel(self)  # SqlRelationalTableModel::sql_关系_表_模型.
        self.logModel.setTable("logs")  # setTable::设置_表
        self.logModel.setRelation(ACTIONID,
                QSqlRelation("actions", "id", "name"))
        self.logModel.setSort(DATE, Qt.AscendingOrder)
        self.logModel.setHeaderData(DATE, Qt.Horizontal, "Date")
        self.logModel.setHeaderData(ACTIONID, Qt.Horizontal, "Action")
        self.logModel.select()

        self.logView = QTableView()
        self.logView.setModel(self.logModel)
        self.logView.setItemDelegate(LogDelegate(self))
        self.logView.setSelectionMode(QTableView.SingleSelection)   # setSelectionMode::设置_选择_模式, SingleSelection::单选
        self.logView.setSelectionBehavior(QTableView.SelectRows)    # setSelectionBehavior::设置_选择_行为
        self.logView.setColumnHidden(ID, True)      # setColumnHidden::设置_列_隐藏(将ID列设为隐藏).
        self.logView.setColumnHidden(ASSETID, True)
        self.logView.resizeColumnsToContents()
        self.logView.horizontalHeader().setStretchLastSection(True)  # setStretchLastSection::设置_伸展_末尾_栏
        logLabel = QLabel("&Logs")
        logLabel.setBuddy(self.logView)

        addAssetButton = QPushButton("&Add Asset")
        deleteAssetButton = QPushButton("&Delete Asset")
        addActionButton = QPushButton("Add A&ction")
        deleteActionButton = QPushButton("Delete Ac&tion")
        editActionsButton = QPushButton("&Edit Actions...")
        editCategoriesButton = QPushButton("Ed&it Categories...")
        quitButton = QPushButton("&Quit")
        for button in (addAssetButton, deleteAssetButton,
                addActionButton, deleteActionButton,
                editActionsButton, editCategoriesButton, quitButton):
            if MAC:
                button.setDefault(False)
                button.setAutoDefault(False)
            else:
                button.setFocusPolicy(Qt.NoFocus)

        dataLayout = QVBoxLayout()
        dataLayout.addWidget(assetLabel)
        dataLayout.addWidget(self.assetView, 1)
        dataLayout.addWidget(logLabel)
        dataLayout.addWidget(self.logView)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(addAssetButton)
        buttonLayout.addWidget(deleteAssetButton)
        buttonLayout.addWidget(addActionButton)
        buttonLayout.addWidget(deleteActionButton)
        buttonLayout.addWidget(editActionsButton)
        buttonLayout.addWidget(editCategoriesButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QHBoxLayout()
        layout.addLayout(dataLayout,0)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(self.assetView.selectionModel(),
                SIGNAL(("currentRowChanged(QModelIndex,QModelIndex)")),
                self.assetChanged)
        self.connect(addAssetButton, SIGNAL("clicked()"), self.addAsset)
        self.connect(deleteAssetButton, SIGNAL("clicked()"),
                     self.deleteAsset)
        self.connect(addActionButton, SIGNAL("clicked()"), self.addAction)
        self.connect(deleteActionButton, SIGNAL("clicked()"),
                     self.deleteAction)
        self.connect(editActionsButton, SIGNAL("clicked()"),
                     self.editActions)
        self.connect(editCategoriesButton, SIGNAL("clicked()"),
                     self.editCategories)
        self.connect(quitButton, SIGNAL("clicked()"), self.done)

        self.assetChanged(self.assetView.currentIndex())
        self.setMinimumWidth(650)   # setMinimumWidth::设置_最小_宽度
        self.setWindowTitle("Asset Manager")


    def done(self, result=1):  # done::完成.(按窗口×键或ESC键时执行)
        query = QSqlQuery()
        query.exec_("DELETE FROM logs WHERE logs.assetid NOT IN"    # 如果logs.assetid在assets.id中不存在,即删除!
                    "(SELECT id FROM assets)")
        QDialog.done(self, 1)


    def assetChanged(self, index):
        if index.isValid():
            record = self.assetModel.record(index.row())    #record::记录(取得 行 记录对象.)
            # id = int(record.value("id"))
            id = int(record.value("id"))
            self.logModel.setFilter("assetid = {}".format(id))  #setFilter::设置过滤器.
        else:
            self.logModel.setFilter("assetid = -1")
        self.logModel.reset()   # reset::重置(重置数据), workaround for Qt <= 4.3.3/SQLite bug
        self.logModel.select()  # 填充数据.
        self.logView.horizontalHeader().setVisible(self.logModel.rowCount() > 0)    #行数>0 设置Visible(可见)==.
        if PYQT_VERSION_STR < "4.1.0":
            self.logView.setColumnHidden(ID, True)
            self.logView.setColumnHidden(ASSETID, True)


    def addAsset(self):
        row = (self.assetView.currentIndex().row()
               if self.assetView.currentIndex().isValid() else 0)

        QSqlDatabase.database().transaction()       #database::数据库, transaction::事务.
        self.assetModel.insertRow(row)
        index = self.assetModel.index(row, NAME)    #返回列索引对象index
        self.assetView.setCurrentIndex(index)

        assetid = 1
        query = QSqlQuery()
        query.exec_("SELECT MAX(id) FROM assets")
        if query.next():
            assetid = int(query.value(0))
        query.prepare("INSERT INTO logs (assetid, date, actionid) "
                      "VALUES (:assetid, :date, :actionid)")
        query.bindValue(":assetid", assetid + 1)
        query.bindValue(":date", QDate.currentDate())
        query.bindValue(":actionid", ACQUIRED)
        query.exec_()
        QSqlDatabase.database().commit()
        self.assetView.edit(index)


    def deleteAsset(self):
        index = self.assetView.currentIndex()
        if not index.isValid():
            return
        QSqlDatabase.database().transaction()   #database::数据库, transaction::事务.(开始数据库事务.)
        record = self.assetModel.record(index.row())
        assetid = int(record.value(ID))
        logrecords = 1
        query = QSqlQuery(
                "SELECT COUNT(*) FROM logs WHERE assetid = {}".format(
                assetid))
        if query.next():
            logrecords = int(query.value(0))
        msg = ("<font color=red>Delete</font><br><b>{}</b>"
               "<br>from room {}".format(
               record.value(NAME), record.value(ROOM)))
        if logrecords > 1:
            msg += ", along with {} log records".format(logrecords)
        msg += "?"
        if (QMessageBox.question(self, "Delete Asset", msg,
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            QSqlDatabase.database().rollback()
            return
        query.exec_("DELETE FROM logs WHERE assetid = {}".format(
                    assetid))
        self.assetModel.removeRow(index.row())
        self.assetModel.submitAll()
        QSqlDatabase.database().commit()
        self.assetChanged(self.assetView.currentIndex())


    def addAction(self):
        index = self.assetView.currentIndex()   # 得到 资产视图 的index对象.
        if not index.isValid():
            return
        QSqlDatabase.database().transaction()  # 开始 数据库.事务
        record = self.assetModel.record(index.row())    # 获取 资产模型表 的记录(record)
        assetid = int(record.value(ID))  # 取 ID号.

        row = self.logModel.rowCount()  # 取得日志模型表总行数.
        self.logModel.insertRow(row)    # 日志模型表 插入新行.
        self.logModel.setData(self.logModel.index(row, ASSETID), assetid)   # 插入新行 写入数据.
        self.logModel.setData(self.logModel.index(row, DATE), QDate.currentDate())
        QSqlDatabase.database().commit()  # 提交数据库修改.
        index = self.logModel.index(row, ACTIONID)  # 取得 日志模型表ACTIONID项 的index对象.
        self.logView.setCurrentIndex(index)  # 设置 index对象为 志日视图 的当前对象.
        self.logView.edit(index)  # 编辑当前对象.


    def deleteAction(self):
        index = self.logView.currentIndex()
        if not index.isValid():
            return
        record = self.logModel.record(index.row())
        action = record.value(ACTIONID)
        if action == "Acquired":
            QMessageBox.information(self, "Delete Log",
                    "The 'Acquired' log record cannot be deleted.<br>"
                    "You could delete the entire asset instead.")
            return
        when = record.value(DATE)
        if (QMessageBox.question(self, "Delete Log",
                "Delete log<br>{} {}?".format(when, action),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            return
        self.logModel.removeRow(index.row())
        self.logModel.submitAll()


    def editActions(self):
        form = ReferenceDataDlg("actions", "Action", self)
        form.exec_()


    def editCategories(self):
        form = ReferenceDataDlg("categories", "Category", self)
        form.exec_()


def main():
    app = QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "assets.db")
    create = not QFile.exists(filename)
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QMessageBox.warning(None, "Asset Manager",
            "Database Error: {}".format(db.lastError().text()))
        sys.exit(1)

    splash = None
    if create:
        app.setOverrideCursor(QCursor(Qt.WaitCursor))
        splash = QLabel()
        pixmap = QPixmap(":/assetmanagersplash.png")
        splash.setPixmap(pixmap)
        splash.setMask(pixmap.createHeuristicMask())    # setMask::设置_掩码, createHeuristicMask::创建_启发式_掩码(将图片设置为启发式掩码)
        splash.setWindowFlags(Qt.SplashScreen)      # SplashScreen::泼开_屏幕(在屏幕上泼开),setWindowFlags::设置_窗口_标记(设置在屏幕上采用的动作)
        rect = app.desktop().availableGeometry()    # availableGeometry::可用_几何(获得桌面可用的几何范围.)
        splash.move((rect.width() - pixmap.width()) / 2,
                    (rect.height() - pixmap.height()) / 2)
        splash.show()
        app.processEvents()
        createFakeData()

    form = MainForm()
    form.show()
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()
    app.exec_()  # 开始事件循环.
    del form
    del db


main()

