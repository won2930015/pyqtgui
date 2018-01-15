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

import gzip
import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


#::时间戳,    ::温度,     ::吸入流,   ::混浊度,   ::电导率,      ::凝结,      ::???, ::???
(TIMESTAMP, TEMPERATURE, INLETFLOW, TURBIDITY, CONDUCTIVITY, COAGULATION, RAWPH, FLOCCULATEDPH) = range(8)

TIMESTAMPFORMAT = "yyyy-MM-dd hh:mm"


class WaterQualityModel(QAbstractTableModel):   #WaterQualityModel::水_质_模型, AbstractTableModel::抽象_表_模型.

    def __init__(self, filename):
        super(WaterQualityModel, self).__init__()
        self.filename = filename
        self.results = []


    def load(self):
        exception = None    #exception::错误
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for loading")
            self.results = []
            line_data = gzip.open(self.filename).read()
            for line in line_data.decode("utf-8").splitlines():
                parts = line.rstrip().split(",")
                date = QDateTime.fromString(parts[0] + ":00",
                                            Qt.ISODate)
                result = [date]
                for part in parts[1:]:
                    result.append(float(part))
                self.results.append(result)
        except (IOError, ValueError) as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            self.reset()
            if exception is not None:
                raise exception


    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or
            not (0 <= index.row() < len(self.results))):
            return None
        column = index.column()
        result = self.results[index.row()]
        if role == Qt.DisplayRole:
            item = result[column]
            if column == TIMESTAMP:
                # TODO set time format
                item = item
            else:
                item = "{:.2f}".format(item)
            return item
        elif role == Qt.TextAlignmentRole:
            if column != TIMESTAMP:
                return int(Qt.AlignRight|Qt.AlignVCenter)
            return int(Qt.AlignLeft|Qt.AlignVCenter)
        elif role == Qt.TextColorRole and column == INLETFLOW:
            if result[column] < 0:
                return QColor(Qt.red)
        elif (role == Qt.TextColorRole and
              column in (RAWPH, FLOCCULATEDPH)):
            ph = result[column]
            if ph < 7:
                return QColor(Qt.red)
            elif ph >= 8:
                return QColor(Qt.blue)
            else:
                return QColor(Qt.darkGreen)
        return None


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignCenter)
            return int(Qt.AlignRight|Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == TIMESTAMP:
                return "Timestamp"
            elif section == TEMPERATURE:
                return "\u00B0" + "C"
            elif section == INLETFLOW:
                return "Inflow"
            elif section == TURBIDITY:
                return "NTU"
            elif section == CONDUCTIVITY:
                return "\u03BCS/cm"
            elif section == COAGULATION:
                return "mg/L"
            elif section == RAWPH:
                return "Raw Ph"
            elif section == FLOCCULATEDPH:
                return "Floc Ph"
        return int(section + 1)


    def rowCount(self, index=QModelIndex()):
        return len(self.results)


    def columnCount(self, index=QModelIndex()):
        return 8


class WaterQualityView(QWidget):

    FLOWCHARS = (chr(0x21DC), chr(0x21DD), chr(0x21C9)) #FLOWCHARS::流_字符

    def __init__(self, parent=None):
        super(WaterQualityView, self).__init__(parent)
        self.scrollarea = None  #滚动_区域
        self.model = None
        self.setFocusPolicy(Qt.StrongFocus) #StrongFocus::强制_焦点
        self.selectedRow = -1
        self.flowfont = self.font() #flowfont::流_字体.
        size = self.font().pointSize()
        if platform.system() == "Windows":
            fontDb = QFontDatabase()
            for face in [face.lower() for face in fontDb.families()]:   #families::家族
                #if face.contains("unicode"):
                if face.find("unicode"):
                    self.flowfont = QFont(face, size)
                    break
            else:
                self.flowfont = QFont("symbol", size)
                WaterQualityView.FLOWCHARS = (chr(0xAC), chr(0xAE), chr(0xDE))


    def setModel(self, model):
        self.model = model
        self.connect(self.model,
                SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                self.setNewSize)
        self.connect(self.model, SIGNAL("modelReset()"), self.setNewSize)
        self.setNewSize()


    def setNewSize(self):
        self.resize(self.sizeHint())
        self.update()
        self.updateGeometry()


    def minimumSizeHint(self):
        size = self.sizeHint()
        fm = QFontMetrics(self.font())
        size.setHeight(fm.height() * 3)
        return size


    def sizeHint(self):
        fm = QFontMetrics(self.font())
        size = fm.height()
        return QSize(fm.width("9999-99-99 99:99 ") + (size * 4),
                     (size / 4) + (size * self.model.rowCount()))


    def paintEvent(self, event):
        if self.model is None:
            return
        fm = QFontMetrics(self.font())
        timestampWidth = fm.width("9999-99-99 99:99 ")
        size = fm.height()
        indicatorSize = int(size * 0.8)
        offset = int(1.5 * (size - indicatorSize))
        minY = event.rect().y()
        maxY = minY + event.rect().height() + size
        minY -= size
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)    #setRenderHint::设置_渲染_提示, Antialiasing::反锯齿
        painter.setRenderHint(QPainter.TextAntialiasing)
        y = 0
        for row in range(self.model.rowCount()):
            x = 0
            if minY <= y <= maxY:
                painter.save()
                painter.setPen(self.palette().color(QPalette.Text))
                if row == self.selectedRow:
                    painter.fillRect(x, y + (offset * 0.8), self.width(), size, self.palette().highlight())
                    painter.setPen(self.palette().color(QPalette.HighlightedText))
                timestamp = self.model.data(self.model.index(row, TIMESTAMP))
                painter.drawText(x, y + size, timestamp.toString("yyyy-MM-dd hh:mm"))   #输出 时间戳

                x += timestampWidth
                temperature = float(self.model.data(self.model.index(row, TEMPERATURE)))
                if temperature < 20:
                    color = QColor(0, 0, int(255 * (20 - temperature) / 20))
                elif temperature > 25:
                    color = QColor(int(255 * temperature / 100), 0, 0)
                else:   #20-25C之间
                    color = QColor(0, int(255 * temperature / 100), 0)
                painter.setPen(Qt.NoPen)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize, indicatorSize)    #输出 温度

                x += size
                rawPh = float(self.model.data(self.model.index(row, RAWPH)))
                if rawPh < 7:
                    color = QColor(int(255 * rawPh / 10), 0, 0)
                elif rawPh >= 8:
                    color = QColor(0, 0, int(255 * rawPh / 10))
                else:   #值 ==7~7.9 时.
                    color = QColor(0, int(255 * rawPh / 10), 0)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize, indicatorSize)

                x += size
                flocPh = float(self.model.data(self.model.index(row, FLOCCULATEDPH)))
                if flocPh < 7:
                    color = QColor(int(255 * flocPh / 10), 0, 0)
                elif flocPh >= 8:
                    color = QColor(0, 0, int(255 * flocPh / 10))
                else:   #值 ==7~7.9时.
                    color = QColor(0, int(255 * flocPh / 10), 0)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize, indicatorSize)    #写 flocPh值.
                painter.restore()
                painter.save()


                x += size
                flow = float(self.model.data(self.model.index(row, INLETFLOW)))
                char = None
                if flow <= 0:
                    char = WaterQualityView.FLOWCHARS[0]
                elif flow < 3:  #0.1~2.9时   ::值在3~5.4的被排除不显示←
                    char = WaterQualityView.FLOWCHARS[1]
                elif flow > 5.5:
                    char = WaterQualityView.FLOWCHARS[2]
                if char is not None:
                    painter.setFont(self.flowfont)
                    painter.drawText(x, y + size, char)
                painter.restore()
            y += size
            if y > maxY:
                break


    def mousePressEvent(self, event):
        fm = QFontMetrics(self.font())
        self.selectedRow = event.y() // fm.height() #计数出所在行.
        self.update()
        self.emit(SIGNAL("clicked(QModelIndex)"), self.model.index(self.selectedRow, 0))


    def keyPressEvent(self, event):
        if self.model is None:
            return
        row = -1
        if event.key() == Qt.Key_Up:
            row = max(0, self.selectedRow - 1)
        elif event.key() == Qt.Key_Down:
            row = min(self.selectedRow + 1, self.model.rowCount() - 1)
        if row != -1 and row != self.selectedRow:
            self.selectedRow = row
            if self.scrollarea is not None:
                fm = QFontMetrics(self.font())
                y = fm.height() * self.selectedRow
                self.scrollarea.ensureVisible(0, y) #ensureVisible::确保_可见
            self.update()
            self.emit(SIGNAL("clicked(QModelIndex)"), self.model.index(self.selectedRow, 0))
        else:
            QWidget.keyPressEvent(self, event)


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = WaterQualityModel(os.path.join(os.path.dirname(__file__), "waterdata.csv.gz"))
        self.tableView = QTableView()
        self.tableView.setAlternatingRowColors(True)    #setAlternatingRowColors::设置_交替_行_颜色(True)
        self.tableView.setModel(self.model)
        self.waterView = WaterQualityView()
        self.waterView.setModel(self.model) #即 QWidget 也具有 setModel属性.
        scrollArea = QScrollArea()  #滚动区域::是一个容器
        scrollArea.setBackgroundRole(QPalette.Light)    #setBackgroundRole::设置_背景_角色, QPalette.Light::调色板.光(滚动区域背景色.浅色光的颜色.)
        scrollArea.setWidget(self.waterView)    #将 waterView 加入到 滚动区域
        self.waterView.scrollarea = scrollArea  #将waterView.scrollarea属性 关联到 scrollArea容器对象.

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tableView)
        splitter.addWidget(scrollArea)
        splitter.setSizes([600, 250])
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.setWindowTitle("Water Quality Data")
        QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  #设置_重载_光标

        #开始设置 闪屏画面.
        splash = QLabel(self)
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__),
                "iss013-e-14802.jpg"))
        splash.setPixmap(pixmap)
        splash.setWindowFlags(Qt.SplashScreen)  #setWindowFlags::设置_窗口_标志, SplashScreen::闪_屏(即 窗口是闪屏类型.)
        splash.move(self.x() + ((self.width() - pixmap.width()) / 2),   #置中 闪屏窗口.
                    self.y() + ((self.height() - pixmap.height()) / 2))
        splash.show()
        QApplication.processEvents()    #processEvents::进程_事件.
        try:
            self.model.load()
        except IOError as e:
            QMessageBox.warning(self, "Water Quality - Error", e)
        else:
            self.tableView.resizeColumnsToContents()
        splash.close()
        QApplication.processEvents()
        QApplication.restoreOverrideCursor()    #restoreOverrideCursor::恢复_重载_光标


app = QApplication(sys.argv)
form = MainForm()
form.resize(850, 620)
form.show()
app.exec_()

