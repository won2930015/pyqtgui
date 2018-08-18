#!/usr/bin/env python3


import os,traceback
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        listWidget = QListWidget()
        path = os.path.dirname(__file__)
        for image in os.listdir(os.path.join(path,"images")):
            if image[-4:]==".png":
                item = QListWidgetItem(image.split(".")[0].capitalize())
                item.setIcon(QIcon(os.path.join(path,"images/%s"%image)))
                listWidget.addItem(item)

        listWidget.setDragEnabled(True)
        listWidget.setAcceptDrops(True)

        iconListWidget = QListWidget()
        iconListWidget.setViewMode(QListView.IconMode)
        iconListWidget.setDragEnabled(True)
        iconListWidget.setAcceptDrops(True)

        tableWidget = QTableWidget()
        tableWidget.setColumnCount(3)
        tableWidget.setRowCount(10)
        tableWidget.setHorizontalHeaderLabels(["第一列","第二列","第三列"])
        tableWidget.setDragEnabled(True)
        tableWidget.setAcceptDrops(True)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(listWidget)
        splitter.addWidget(iconListWidget)
        splitter.addWidget(tableWidget)

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setMinimumHeight(400)
        self.setWindowTitle("Drag and Drop by Corkine Ma")


if __name__=="__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()