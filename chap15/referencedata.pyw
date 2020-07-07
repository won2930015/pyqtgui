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

MAC = True
try:
    from PyQt4.QtGui import qt_mac_set_native_menubar   # qt_mac_设置_本地_菜单条
except ImportError:
    MAC = False

ID, CATEGORY, SHORTDESC, LONGDESC = range(4)    # CATEGORY::种类, SHORTDESC::短描述, LONGDESC::长描述


class ReferenceDataDlg(QDialog):

    def __init__(self, parent=None):
        super(ReferenceDataDlg, self).__init__(parent)

        self.model = QSqlTableModel(self)
        self.model.setTable("reference")  # 创建表reference
        self.model.setSort(ID, Qt.AscendingOrder)  # id列,升序排序
        self.model.setHeaderData(ID, Qt.Horizontal, "ID")  # 设置表标题.
        self.model.setHeaderData(CATEGORY, Qt.Horizontal, "Category")
        self.model.setHeaderData(SHORTDESC, Qt.Horizontal, "Short Desc.")
        self.model.setHeaderData(LONGDESC, Qt.Horizontal, "Long Desc.")
        self.model.select()  # 选择表.

        self.view = QTableView()  # 表视图对象.
        self.view.setModel(self.model)  # 关联模式.
        self.view.setSelectionMode(QTableView.SingleSelection)  # 设置_选择_模式:单选.
        self.view.setSelectionBehavior(QTableView.SelectRows)   # 设置_选择_行为:选择行.
        self.view.setColumnHidden(ID, True)  # 隐藏id列.
        self.view.resizeColumnsToContents()  # 据内容重置列宽.

        buttonBox = QDialogButtonBox()  # 创建DialogButtonBox对象(对话框按键容器.)
        addButton = buttonBox.addButton("&Add", QDialogButtonBox.ActionRole)    # ActionRole::动作角色(作用)
        deleteButton = buttonBox.addButton("&Delete", QDialogButtonBox.ActionRole)
        sortButton = buttonBox.addButton("&Sort", QDialogButtonBox.ActionRole)
        if not MAC:
            addButton.setFocusPolicy(Qt.NoFocus)
            deleteButton.setFocusPolicy(Qt.NoFocus)
            sortButton.setFocusPolicy(Qt.NoFocus)

        menu = QMenu(self)  # 创建菜单.
        sortByCategoryAction = menu.addAction("Sort by &Category")  # 加入菜单项.
        sortByDescriptionAction = menu.addAction("Sort by &Description")
        sortByIDAction = menu.addAction("Sort by &ID")
        sortButton.setMenu(menu)  # 给按键绑定菜单
        closeButton = buttonBox.addButton(QDialogButtonBox.Close)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(addButton, SIGNAL("clicked()"), self.addRecord)
        self.connect(deleteButton, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(sortByCategoryAction, SIGNAL("triggered()"),
                     lambda: self.sort(CATEGORY))
        self.connect(sortByDescriptionAction, SIGNAL("triggered()"),
                     lambda: self.sort(SHORTDESC))
        self.connect(sortByIDAction, SIGNAL("triggered()"),
                     lambda: self.sort(ID))
        self.connect(closeButton, SIGNAL("clicked()"), self.accept)

        self.setWindowTitle("Reference Data")


    def addRecord(self):
        row = self.model.rowCount()  # 返回数据表行数n.
        self.model.insertRow(row)  # 插入行
        index = self.model.index(row, CATEGORY)  # 返回插入行的CATEGORY列为-->QModelIndex对象.
        self.view.setCurrentIndex(index)  # 在视图设置为当前项
        self.view.edit(index)  # 编辑当项.


    def deleteRecord(self):
        index = self.view.currentIndex()  # 获得当前项
        if not index.isValid():  # 是否有效
            return
        record = self.model.record(index.row())  # 获得记录
        category = record.value(CATEGORY)  # 取CATEGORY值.
        desc = record.value(SHORTDESC)  # 取SHORTDESC值.
        if (QMessageBox.question(self, "Reference Data",
                "Delete {} from category {}?".format(
                desc, category),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            return
        self.model.removeRow(index.row())  # 数据表删除行.
        self.model.submitAll()  # 提交全部


    def sort(self, column):
        self.model.setSort(column, Qt.AscendingOrder)  # n列,升序排序
        self.model.select()


def main():
    app = QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "reference.db")
    create = not QFile.exists(filename)

    db = QSqlDatabase.addDatabase("QSQLITE")  # 设置数据库驱动.
    db.setDatabaseName(filename)  # 设置数据库文件
    if not db.open():
        QMessageBox.warning(None, "Reference Data",
            "Database Error: {}".format(db.lastError().text()))
        sys.exit(1)

    if create:
        query = QSqlQuery()
        query.exec_("""CREATE TABLE reference (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                category VARCHAR(30) NOT NULL,
                shortdesc VARCHAR(20) NOT NULL,
                longdesc VARCHAR(80))""")

    form = ReferenceDataDlg()
    form.show()
    sys.exit(app.exec_())


main()

