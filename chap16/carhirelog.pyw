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

import bisect   #bisect::二分模块(二分算法模块.)
import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import genericdelegates #导入 泛型委托模块.


(LICENSE, CUSTOMER, HIRED, MILEAGEOUT, RETURNED, MILEAGEBACK,
 NOTES, MILEAGE, DAYS) = range(9)


class CarHireLog(object):   #汽车_租用_日志.

    def __init__(self, license, customer, hired, mileageout,    #license::执照, customer::客户, hired::租用(租出日期), mileageout::里程数_out(租出时里程时.),
                 returned=QDate(), mileageback=0, notes=""):    #returned::返回(归还时间), mileageback::里程数_back(归还时里程数), notes::注释
        self.license = license          # plain text 执照
        self.customer = customer        # plain text 客户
        self.hired = hired              # QDate 租用(出租日期)
        self.mileageout = mileageout    # int   里程数_out(租出时)
        self.returned = returned        # QDate 返回(归还日期)
        self.mileageback = mileageback  # int   里程数_back(归还时)
        self.notes = notes              # HTML  注释


    def field(self, column):    # 字段|域
        if column == LICENSE:
            return self.license
        elif column == CUSTOMER:
            return self.customer
        elif column == HIRED:
            return self.hired
        elif column == MILEAGEOUT:
            return self.mileageout
        elif column == RETURNED:
            return self.returned
        elif column == MILEAGEBACK:
            return self.mileageback
        elif column == NOTES:
            return self.notes
        elif column == MILEAGE: #里程
            return self.mileage()
        elif column == DAYS:    #天数
            return self.days()
        assert False


    def mileage(self):
        return (0 if self.mileageback == 0
                  else self.mileageback - self.mileageout)


    def days(self):
        return (0 if not self.returned.isValid()
                  else self.hired.daysTo(self.returned))    #daysTo::天数To (返回 hired-- returned的天数.)


    def __hash__(self): # hash::散列|哈希
        return super(CarHireLog, self).__hash__()


    def __eq__(self, other):    #eq::等于
        if self.hired != other.hired:
            return False
        if self.customer != other.customer:
            return False
        if self.license != other.license:
            return False
        return id(self) == id(other)


    def __lt__(self, other):    #lt::小于
        if self.hired < other.hired:
            return True
        if self.customer < other.customer:
            return True
        if self.license < other.license:
            return True
        return id(self) < id(other)



class CarHireModel(QAbstractTableModel):    #汽车_出租_模型.

    def __init__(self, parent=None):
        super(CarHireModel, self).__init__(parent)
        self.logs = []

        # Generate fake data
        import gzip
        import random
        import string
        surname_data = gzip.open(os.path.join(  #surname_data::性氏_数据
                os.path.dirname(__file__), "surnames.txt.gz")).read()
        surnames = surname_data.decode("utf-8").splitlines()
        years = ("06 ", "56 ", "07 ", "57 ", "08 ", "58 ")
        titles = ("Ms ", "Mr ", "Ms ", "Mr ", "Ms ", "Mr ", "Dr ")    #Mr::女士, Ms::先生, Dr::未知????
        notetexts = ("Returned <font color=red><b>damaged</b></font>",  #notetexts::注释_文本, Returned damaged::返回受损(车)
                "Returned with <i>empty fuel tank</i>",                 #返回 空油箱(车)
                "Customer <b>complained</b> about the <u>engine</u>",   #Customer complained about the engine::客户 抱怨 发动机
                "Customer <b>complained</b> about the <u>gears</u>",    #Customer complained about the gears ::客户 抱怨 齿轮箱
                "Customer <b>complained</b> about the <u>clutch</u>",   #Customer complained about the clutch ::客户 抱怨 离合器
                "Returned <font color=darkred><b>dirty</b></font>",)    #Returned dirty ::返回 脏的(车)
        today = QDate.currentDate()     #today::今天
        for i in range(250):
            license = []    #license::执照
            for c in range(5):
                license.append(random.choice(string.ascii_uppercase))   #uppercase::大写字母
            license = ("".join(license[:2]) + random.choice(years) +    #生成执照
                       "".join(license[2:]))
            customer = random.choice(titles) + random.choice(surnames)  #生成客户(名+性)
            hired = today.addDays(-random.randint(0, 365))  #生成出租日期
            mileageout = random.randint(10000, 30000)   #生成里程(出租时)
            notes = ""
            if random.random() >= 0.2:
                days = random.randint(1, 21)    #生成 天数
                returned = hired.addDays(days)  #生成 返回(归还日期)
                mileageback = (mileageout +     #生成 里程(归还时.)
                               (days * random.randint(30, 300)))
                if random.random() > 0.75:
                    notes = random.choice(notetexts)    #生成 注释
            else:
                returned = QDate()
                mileageback = 0
            log = CarHireLog(license, customer, hired, mileageout,
                             returned, mileageback, notes)
            bisect.insort(self.logs, log)   #insort::进入_排序(加入到 logs 并二分排序)


    def rowCount(self, index=QModelIndex()):
        return len(self.logs)


    def columnCount(self, index=QModelIndex()):
        return 9


    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            log = self.logs[index.row()]
            value = log.field(index.column())
            if (index.column() in (MILEAGEBACK, MILEAGE, DAYS) and
                value == 0):
                return None
            return value
        if (role == Qt.TextAlignmentRole and
            index.column() not in (LICENSE, CUSTOMER, NOTES)):
            return int(Qt.AlignRight|Qt.AlignVCenter)
        if role == Qt.BackgroundColorRole:
            palette = QApplication.palette()
            if index.column() in (LICENSE, MILEAGE, DAYS):
                return palette.alternateBase()  # alternateBase::交替_底色(返回交替色底色?)
            else:
                return palette.base()   #base::底色
        return None


    def setData(self, index, value, role=Qt.EditRole):
        if (index.isValid() and role == Qt.EditRole and
            index.column() not in (LICENSE, MILEAGE, DAYS)):
            log = self.logs[index.row()]
            column = index.column()
            if column == CUSTOMER:
                log.customer = value
            elif column == HIRED:
                log.hired = value
            elif column == MILEAGEOUT:
                log.mileageout = int(value)
            elif column == RETURNED:
                log.returned = value
            elif column == MILEAGEBACK:
                log.mileageback = int(value)
            elif column == NOTES:
                log.notes = value
            self.emit(SIGNAL(
                    "dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        return False


    def headerData(self, section, orientation, role):   #section::段|部分, orientation::方向, role::角色.
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignCenter)
            return int(Qt.AlignRight|Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == LICENSE:
                return "License"
            elif section == CUSTOMER:
                return "Customer"
            elif section == HIRED:
                return "Hired"
            elif section == MILEAGEOUT:
                return "Mileage #1"
            elif section == RETURNED:
                return "Returned"
            elif section == MILEAGEBACK:
                return "Mileage #2"
            elif section == DAYS:
                return "Days"
            elif section == MILEAGE:
                return "Miles"
            elif section == NOTES:
                return "Notes"
        return section + 1


    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() not in (LICENSE, MILEAGE, DAYS):
            flag |= Qt.ItemIsEditable   #ItemIsEditable::项_是_可编辑的(设置项为可编辑的.)
        return flag
            

class HireDateColumnDelegate(genericdelegates.DateColumnDelegate):  #出租_日期_列_委托

    def createEditor(self, parent, option, index):
        i = index.sibling(index.row(), RETURNED)    #sibling::兄弟
        self.maximum = i.model().data(i, Qt.DisplayRole).addDays(-1)    #addDays(-1)::不设置最大的日期.
        return genericdelegates.DateColumnDelegate.createEditor(
                self, parent, option, index)


class ReturnDateColumnDelegate(genericdelegates.DateColumnDelegate):    #归还日期_列_委托

    def createEditor(self, parent, option, index):
        i = index.sibling(index.row(), HIRED)   #sibling::兄弟
        self.minimum = i.model().data(i, Qt.DisplayRole).addDays(1) #addDays(-1)::不设置最大的日期.
        return genericdelegates.DateColumnDelegate.createEditor(
                self, parent, option, index)


class MileageOutColumnDelegate(genericdelegates.IntegerColumnDelegate): #里程(租出时)_列_委托

    def createEditor(self, parent, option, index):
        i = index.sibling(index.row(), MILEAGEBACK)
        maximum = int(i.model().data(i, Qt.DisplayRole))
        self.maximum = 1000000 if maximum == 0 else maximum - 1
        return genericdelegates.IntegerColumnDelegate.createEditor(
                self, parent, option, index)


class MileageBackColumnDelegate(genericdelegates.IntegerColumnDelegate):    #里程(归还时)_列_委托

    def createEditor(self, parent, option, index):
        i = index.sibling(index.row(), MILEAGEOUT)
        self.minimum = int(i.model().data(i, Qt.DisplayRole)) + 1
        return genericdelegates.IntegerColumnDelegate.createEditor(
                self, parent, option, index)


class MainForm(QMainWindow):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        model = CarHireModel(self)

        self.view = QTableView()
        self.view.setModel(model)
        self.view.resizeColumnsToContents()

        delegate = genericdelegates.GenericDelegate(self)
        delegate.insertColumnDelegate(CUSTOMER,
                genericdelegates.PlainTextColumnDelegate())
        earliest = QDate.currentDate().addYears(-3)      #earliest::初期的.
        delegate.insertColumnDelegate(HIRED,
                HireDateColumnDelegate(earliest))
        delegate.insertColumnDelegate(MILEAGEOUT,
                MileageOutColumnDelegate(0, 1000000))
        delegate.insertColumnDelegate(RETURNED,
                ReturnDateColumnDelegate(earliest))
        delegate.insertColumnDelegate(MILEAGEBACK,
                MileageBackColumnDelegate(0, 1000000))
        delegate.insertColumnDelegate(NOTES,
                genericdelegates.RichTextColumnDelegate())

        self.view.setItemDelegate(delegate)
        self.setCentralWidget(self.view)

        QShortcut(QKeySequence("Escape"), self, self.close)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)

        self.setWindowTitle("Car Hire Logs")


app = QApplication(sys.argv)
form = MainForm()
rect = QApplication.desktop().availableGeometry()   #availableGeometry::可用_几何
form.resize(int(rect.width() * 0.7), int(rect.height() * 0.8))
form.move(0, 0)
form.show()
app.exec_()

