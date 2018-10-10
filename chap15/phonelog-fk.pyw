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

MAC = "qt_mac_set_native_menubar" in dir()

ID, CALLER, STARTTIME, ENDTIME, TOPIC, OUTCOMEID = range(6)
DATETIME_FORMAT = "yyyy-MM-dd hh:mm"


def createFakeData():   # 创建伪数据.
    import random

    print("Dropping tables...")
    query = QSqlQuery()
    query.exec_("DROP TABLE calls")  # DROP TABLE::丢弃_表
    query.exec_("DROP TABLE outcomes")
    QApplication.processEvents()

    print("Creating tables...")
    query.exec_("""CREATE TABLE outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL)""")

    query.exec_("""CREATE TABLE calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                caller VARCHAR(40) NOT NULL,
                starttime DATETIME NOT NULL,
                endtime DATETIME NOT NULL,
                topic VARCHAR(80) NOT NULL,
                outcomeid INTEGER NOT NULL,
                FOREIGN KEY (outcomeid) REFERENCES outcomes)""")
    QApplication.processEvents()

    print("Populating tables...")
    for name in ("Resolved", "Unresolved", "Calling back", "Escalate",
                 "Wrong number"):
        query.exec_("INSERT INTO outcomes (name) VALUES ('{}')".format(
                    name))
    topics = ("Complaint", "Information request", "Off topic",
              "Information supplied", "Complaint", "Complaint")
    now = QDateTime.currentDateTime()
    query.prepare("INSERT INTO calls (caller, starttime, endtime, "
                  "topic, outcomeid) VALUES (:caller, :starttime, "
                  ":endtime, :topic, :outcomeid)")
    for name in ('Joshan Cockerall', 'Ammanie Ingham',
            'Diarmuid Bettington', 'Juliana Bannister',
            'Oakley-Jay Buxton', 'Reilley Collinge',
            'Ellis-James Mcgehee', 'Jazmin Lawton',
            'Lily-Grace Smythe', 'Coskun Lant', 'Lauran Lanham',
            'Millar Poindexter', 'Naqeeb Neild', 'Maxlee Stoddart',
            'Rebia Luscombe', 'Briana Christine', 'Charli Pease',
            'Deena Mais', 'Havia Huffman', 'Ethan Davie',
            'Thomas-Jack Silver', 'Harpret Bray', 'Leigh-Ann Goodliff',
            'Seoras Bayes', 'Jenna Underhill', 'Veena Helps',
            'Mahad Mcintosh', 'Allie Hazlehurst', 'Aoife Warrington',
            'Cameron Burton', 'Yildirim Ahlberg', 'Alissa Clayton',
            'Josephine Weber', 'Fiore Govan', 'Howard Ragsdale',
            'Tiernan Larkins', 'Seren Sweeny', 'Arisha Keys',
            'Kiki Wearing', 'Kyran Ponsonby', 'Diannon Pepper',
            'Mari Foston', 'Sunil Manson', 'Donald Wykes',
            'Rosie Higham', 'Karmin Raines', 'Tayyibah Leathem',
            'Kara-jay Knoll', 'Shail Dalgleish', 'Jaimie Sells'):
        start = now.addDays(-random.randint(1, 30)).addSecs(-random.randint(60 * 5, 60 * 60 * 2))
        # start = now.addDays(-random.randint(1, 30))
        # start = now.addSecs(-random.randint(60 * 5, 60 * 60 * 2))
        end = start.addSecs(random.randint(20, 60 * 13))
        topic = random.choice(topics)   # choice::选择(随机的.)
        outcomeid = int(random.randint(1, 5))
        query.bindValue(":caller", name)
        query.bindValue(":starttime", start)
        query.bindValue(":endtime", end)
        query.bindValue(":topic", topic)
        query.bindValue(":outcomeid", outcomeid)
        query.exec_()
    QApplication.processEvents()  # processEvents::进程_事件(将控制权交还给程序防止假死现象).

    print("Calls:")
    query.exec_("SELECT id, caller, starttime, endtime, topic, "
                "outcomeid FROM calls ORDER by starttime")
    while query.next():
        id = int(query.value(ID))
        caller = query.value(CALLER)
        starttime = query.value(STARTTIME)
        endtime = query.value(ENDTIME)
        topic = query.value(TOPIC)
        outcomeid = int(query.value(OUTCOMEID))
        subquery = QSqlQuery("SELECT name FROM outcomes "
                             "WHERE id = {}".format(outcomeid))
        outcome = "invalid foreign key"  # 译文：“无效的外键”
        if subquery.next():
            outcome = subquery.value(0)
        print("{0:02d}: {1} {2} - {3} {4} [{5}]".format(id, caller,
              starttime, endtime, topic, outcome))
    QApplication.processEvents()    # processEvents::进程_事件(将控制权交还给程序防止假死现象).


class PhoneLogDlg(QDialog):

    FIRST, PREV, NEXT, LAST = range(4)

    def __init__(self, parent=None):
        super(PhoneLogDlg, self).__init__(parent)

        callerLabel = QLabel("&Caller:")
        self.callerEdit = QLineEdit()
        callerLabel.setBuddy(self.callerEdit)

        today = QDate.currentDate()

        startLabel = QLabel("&Start:")
        self.startDateTime = QDateTimeEdit()
        startLabel.setBuddy(self.startDateTime)
        # self.startDateTime.setDateRange(today, today)
        self.startDateTime.setDateRange(today.addYears(-1), today)
        self.startDateTime.setDisplayFormat(DATETIME_FORMAT)

        endLabel = QLabel("&End:")
        self.endDateTime = QDateTimeEdit()
        endLabel.setBuddy(self.endDateTime)
        # self.endDateTime.setDateRange(today, today)
        self.endDateTime.setDateRange(today.addYears(-1), today)
        self.endDateTime.setDisplayFormat(DATETIME_FORMAT)

        topicLabel = QLabel("&Topic:")
        topicEdit = QLineEdit()
        topicLabel.setBuddy(topicEdit)

        outcomeLabel = QLabel("&Outcome:")
        self.outcomeComboBox = QComboBox()
        outcomeLabel.setBuddy(self.outcomeComboBox)

        firstButton = QPushButton()
        firstButton.setIcon(QIcon(":/first.png"))
        prevButton = QPushButton()
        prevButton.setIcon(QIcon(":/prev.png"))
        nextButton = QPushButton()
        nextButton.setIcon(QIcon(":/next.png"))
        lastButton = QPushButton()
        lastButton.setIcon(QIcon(":/last.png"))

        addButton = QPushButton("&Add")
        addButton.setIcon(QIcon(":/add.png"))
        deleteButton = QPushButton("&Delete")
        deleteButton.setIcon(QIcon(":/delete.png"))
        quitButton = QPushButton("&Quit")
        quitButton.setIcon(QIcon(":/quit.png"))

        if not MAC:
            addButton.setFocusPolicy(Qt.NoFocus)
            deleteButton.setFocusPolicy(Qt.NoFocus)

        fieldLayout = QGridLayout()  # 创建网格布局.
        fieldLayout.addWidget(callerLabel, 0, 0)
        fieldLayout.addWidget(self.callerEdit, 0, 1, 1, 3)
        fieldLayout.addWidget(startLabel, 1, 0)
        fieldLayout.addWidget(self.startDateTime, 1, 1)
        fieldLayout.addWidget(endLabel, 1, 2)
        fieldLayout.addWidget(self.endDateTime, 1, 3)
        fieldLayout.addWidget(topicLabel, 2, 0)
        fieldLayout.addWidget(topicEdit, 2, 1, 1, 3)
        fieldLayout.addWidget(outcomeLabel, 3, 0)
        fieldLayout.addWidget(self.outcomeComboBox, 3, 1, 1, 3)

        navigationLayout = QHBoxLayout()
        navigationLayout.addWidget(firstButton)
        navigationLayout.addWidget(prevButton)
        navigationLayout.addWidget(nextButton)
        navigationLayout.addWidget(lastButton)
        fieldLayout.addLayout(navigationLayout, 4, 0, 1, 2)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)

        layout = QHBoxLayout()
        layout.addLayout(fieldLayout)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.model = QSqlRelationalTableModel(self)  # 创建 SQL_关系_表_模型 P344-1
        self.model.setTable("calls")
        self.model.setRelation(OUTCOMEID, QSqlRelation("outcomes", "id", "name"))  # <<---TODO::注意!!!P344-2
        self.model.setSort(STARTTIME, Qt.AscendingOrder)    # AscendingOrder::升序排序
        self.model.select()

        # P342
        self.mapper = QDataWidgetMapper(self)  # 数据_控件_映射
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)  # 设置_提交_政策,ManualSubmit::手动_提交
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))  # <<--注意!!!
        self.mapper.addMapping(self.callerEdit, CALLER)
        self.mapper.addMapping(self.startDateTime, STARTTIME)
        self.mapper.addMapping(self.endDateTime, ENDTIME)
        self.mapper.addMapping(topicEdit, TOPIC)

        relationModel = self.model.relationModel(OUTCOMEID)  # <<---注意!!! relationModel::关系模型(创建关系模型)

        self.outcomeComboBox.setModel(relationModel)  # <<---注意!!!
        self.outcomeComboBox.setModelColumn(relationModel.fieldIndex("name"))  # <<---注意!!! P345-5.显示的列设为'name'
        self.mapper.addMapping(self.outcomeComboBox, OUTCOMEID)  # <<---注意!!!
        self.mapper.toFirst()

        self.connect(firstButton, SIGNAL("clicked()"), lambda: self.saveRecord(PhoneLogDlg.FIRST))
        self.connect(prevButton, SIGNAL("clicked()"), lambda: self.saveRecord(PhoneLogDlg.PREV))
        self.connect(nextButton, SIGNAL("clicked()"), lambda: self.saveRecord(PhoneLogDlg.NEXT))
        self.connect(lastButton, SIGNAL("clicked()"), lambda: self.saveRecord(PhoneLogDlg.LAST))
        self.connect(addButton, SIGNAL("clicked()"), self.addRecord)
        self.connect(deleteButton, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(quitButton, SIGNAL("clicked()"), self.done)

        self.setWindowTitle("Phone Log")


    def done(self, result=None):  # P345
        self.mapper.submit()
        QDialog.done(self, True)

        
    def addRecord(self):
        row = self.model.rowCount()
        self.mapper.submit()
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        now = QDateTime.currentDateTime()
        self.startDateTime.setDateTime(now)
        self.endDateTime.setDateTime(now)
        self.outcomeComboBox.setCurrentIndex(
                self.outcomeComboBox.findText("Unresolved"))
        self.callerEdit.setFocus()


    def deleteRecord(self):
        caller = self.callerEdit.text()
        starttime = self.startDateTime.dateTime().toString()
        if (QMessageBox.question(self,
                "Delete",
                "Delete call made by<br>{} on {}?".format(
                caller, starttime),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():  # 如果删除的是最后一条记录.
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)


    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == PhoneLogDlg.FIRST:
            row = 0
        elif where == PhoneLogDlg.PREV:
            row = 0 if row <= 1 else row - 1
        elif where == PhoneLogDlg.NEXT:
            row += 1
            if row >= self.model.rowCount():
                row = self.model.rowCount() - 1
        elif where == PhoneLogDlg.LAST:
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)


def main():
    app = QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "phonelog-fk.db")
    create = not QFile.exists(filename)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QMessageBox.warning(None, "Phone Log",
            "Database Error: {}".format(db.lastError().text()))
        sys.exit(1)

    splash = None
    if create:
        app.setOverrideCursor(QCursor(Qt.WaitCursor))
        splash = QLabel()
        pixmap = QPixmap(":/phonelogsplash.png")
        splash.setPixmap(pixmap)
        splash.setMask(pixmap.createHeuristicMask())  # createHeuristicMask:: 创建_启发式_掩码
        splash.setWindowFlags(Qt.SplashScreen)  # SplashScreen::泼开_屏幕(在屏幕上泼开),setWindowFlags::设置_窗口_标记(设置在屏幕上采用的动作)
        rect = app.desktop().availableGeometry()  # availableGeometry::可用_几何.
        splash.move((rect.width() - pixmap.width()) / 2,
                    (rect.height() - pixmap.height()) / 2)
        splash.show()
        app.processEvents()
        createFakeData()

    form = PhoneLogDlg()
    form.show()
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()
    sys.exit(app.exec_())

main()

