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

import platform
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import richtextlineedit

NAME, OWNER, COUNTRY, DESCRIPTION, TEU = range(5)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1


# 船
class Ship(object):

    def __init__(self, name, owner, country, teu=0, description=""):
        self.name = name    # 名
        self.owner = owner  # 物主
        self.country = country  # 国家
        self.teu = teu  # 标准箱
        self.description = description  # 描述

    # 哈希表|散列表
    def __hash__(self):
        return super(Ship, self).__hash__()

    # 比较符 <
    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    # 比较符 ==
    def __eq__(self, other):
        return self.name.lower() == other.name.lower()


# 船_容器 (ships-dict示列引用)
class ShipContainer(object):

    def __init__(self, filename=""):
        self.filename = filename  # 文件名
        self.dirty = False  # dirty::脏的(文件修改标记)
        self.ships = {}     # ships::N条船(字典)
        self.owners = set()  # owners::物主们(集)
        self.countries = set()  #countries::国家们(集)

    def ship(self, identity):  # identity::身份
        return self.ships.get(identity)

    def addShip(self, ship):  # 加入_船
        self.ships[id(ship)] = ship
        self.owners.add(ship.owner)
        self.countries.add(ship.country)
        self.dirty = True

    def removeShip(self, ship):
        del self.ships[id(ship)]
        del ship
        self.dirty = True

    def __len__(self):
        return len(self.ships)

    def __iter__(self):  # 迭代器(返回ships集的所有值 values).
        for ship in self.ships.values():
            yield ship

    def inOrder(self):  # 执行排序(按values排序)
        return sorted(self.ships.values())

    def inCountryOwnerOrder(self):  # 执行 国家&物主&名 排序
        return sorted(self.ships.values(), key=lambda x: (x.country, x.owner, x.name))

    def load(self):
        exception = None  # exception::异常
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for loading")
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QDataStream(fh)    #创建 数据流文件(二进制)
            magic = stream.readInt32()
            if magic != MAGIC_NUMBER:
                raise IOError("unrecognized file type")
            fileVersion = stream.readInt16()
            if fileVersion != FILE_VERSION:
                raise IOError("unrecognized file type version")
            self.ships = {}
            while not stream.atEnd():
                name = stream.readQString()
                owner = stream.readQString()
                country = stream.readQString()
                description = stream.readQString()
                teu = stream.readInt32()
                ship = Ship(name, owner, country, teu, description)
                self.ships[id(ship)] = ship
                self.owners.add(owner)
                self.countries.add(country)
            self.dirty = False
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

    def save(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for saving")
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QDataStream(fh)
            stream.writeInt32(MAGIC_NUMBER)
            stream.writeInt16(FILE_VERSION)
            stream.setVersion(QDataStream.Qt_4_1)
            for ship in self.ships.values():
                stream.writeQString(ship.name)
                stream.writeQString(ship.owner)
                stream.writeQString(ship.country)
                stream.writeQString(ship.description)
                stream.writeInt32(ship.teu)
            self.dirty = False
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


# 船_表_模型(AbstractTableModel::抽象_表_模型)
class ShipTableModel(QAbstractTableModel):

    def __init__(self, filename=""):
        super(ShipTableModel, self).__init__()
        self.filename = filename
        self.dirty = False
        self.ships = []
        self.owners = set()  # set()::集(不存在重复元素.)
        self.countries = set()

    def sortByName(self):  # 按名字排序
        self.ships = sorted(self.ships)
        self.reset()  # 重置::数据_重置/更新.

    def sortByCountryOwner(self):  # 按 国家&物主 排序
        self.ships = sorted(self.ships, key=lambda x: (x.country, x.owner, x.name))
        self.reset()

    def flags(self, index):  # 标志??? P325
        if not index.isValid():  # isValid::is_有效的(判断index是否有效(有数据))
            return Qt.ItemIsEnabled
                                # 如果index有效 就将项已有的标志↓与Qt.ItemIsEditable进行结合,返回.
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)| Qt.ItemIsEditable)

    #  P324
    def data(self, index, role=Qt.DisplayRole):  # DisplayRole::显示_角色
        if (not index.isValid() or not (0 <= index.row() < len(self.ships))):
            return None
        ship = self.ships[index.row()]
        column = index.column()  # column::列
        if role == Qt.DisplayRole:
            if column == NAME:
                return ship.name
            elif column == OWNER:
                return ship.owner
            elif column == COUNTRY:
                return ship.country
            elif column == DESCRIPTION:
                return ship.description
            elif column == TEU:
                return "{:,}".format(ship.teu)  # "{:,}"::添加千位分隔符?
        elif role == Qt.TextAlignmentRole:  # TextAlignmentRole::文本_对齐_角色
            if column == TEU:
                return int(Qt.AlignRight|Qt.AlignVCenter)
            return int(Qt.AlignLeft|Qt.AlignVCenter)
        elif role == Qt.TextColorRole and column == TEU:  # 文本_色_角色
            if ship.teu < 80000:
                return QColor(Qt.black)
            elif ship.teu < 100000:
                return QColor(Qt.darkBlue)
            elif ship.teu < 120000:
                return QColor(Qt.blue)
            else:
                return QColor(Qt.red)
        elif role == Qt.BackgroundColorRole:  # BackgroundColorRole::背景_色_角色
            if ship.country in ("Bahamas", "Cyprus", "Denmark",
                    "France", "Germany", "Greece"):
                return QColor(250, 230, 250)
            elif ship.country in ("Hong Kong", "Japan", "Taiwan"):
                return QColor(250, 250, 230)
            elif ship.country in ("Marshall Islands",):
                return QColor(230, 250, 250)
            else:
                return QColor(210, 230, 230)
        return None

    # headerData::(表)头数据,section::区段, orientation::方向 P325
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:  # Horizontal::水平
                return int(Qt.AlignLeft|Qt.AlignVCenter)
            return int(Qt.AlignRight|Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:    # 列表头(栏目)
            if section == NAME:
                return "Name"
            elif section == OWNER:
                return "Owner"
            elif section == COUNTRY:
                return "Country"
            elif section == DESCRIPTION:
                return "Description"
            elif section == TEU:
                return "TEU"
        return int(section + 1)  # 行表头(序号)

    def rowCount(self, index=QModelIndex()):  # rowCount::行数, ModelIndex::模型_索引
        return len(self.ships)

    def columnCount(self, index=QModelIndex()):  # columnCount::例数
        return 5

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.ships):
            ship = self.ships[index.row()]
            column = index.column()
            if column == NAME:
                ship.name = value
            elif column == OWNER:
                ship.owner = value
            elif column == COUNTRY:
                ship.country = value
            elif column == DESCRIPTION:
                ship.description = value
            elif column == TEU:
                ship.teu = int(value)
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)  # 发射dataChanged()信号 ,刷新数据.
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):  # 插入_行. position:插入位置, rows:插入行数
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row, Ship(" Unknown", " Unknown", " Unknown"))
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):  # 移除_行
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.ships = (self.ships[:position] + self.ships[position + rows:])  # 用排除自身的方法更新ships列表.
        self.endRemoveRows()
        self.dirty = True
        return True

    def load(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for loading")
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QDataStream(fh)
            magic = stream.readInt32()
            if magic != MAGIC_NUMBER:
                raise IOError("unrecognized file type")
            fileVersion = stream.readInt16()
            if fileVersion != FILE_VERSION:
                raise IOError("unrecognized file type version")
            stream.setVersion(QDataStream.Qt_4_5)
            self.ships = []
            while not stream.atEnd():
                name = stream.readQString()
                owner = stream.readQString()
                country = stream.readQString()
                description = stream.readQString()
                teu = stream.readInt32()
                self.ships.append(Ship(name, owner, country, teu,
                                       description))
                self.owners.add(owner)
                self.countries.add(country)
            self.dirty = False
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

    def save(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for saving")
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QDataStream(fh)
            stream.writeInt32(MAGIC_NUMBER)
            stream.writeInt16(FILE_VERSION)
            stream.setVersion(QDataStream.Qt_4_5)
            for ship in self.ships:
                stream.writeQString(ship.name)
                stream.writeQString(ship.owner)
                stream.writeQString(ship.country)
                stream.writeQString(ship.description)
                stream.writeInt32(ship.teu)
            self.dirty = False
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


class ShipDelegate(QStyledItemDelegate):  # 船_委托

    def __init__(self, parent=None):
        super(ShipDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if index.column() == DESCRIPTION:  # 处理描述项的字符.
            text = index.model().data(index)
            palette = QApplication.palette()   # palette::调色板
            document = QTextDocument()
            document.setDefaultFont(option.font)
            if option.state & QStyle.State_Selected:  # 当选项的状态 是选中状态时...执行.
                document.setHtml("<font color={}>{}</font>".format(
                        palette.highlightedText().color().name(), text))
            else:
                document.setHtml(text)
            color = (palette.highlight().color()
                     if option.state & QStyle.State_Selected
                     else QColor(index.model().data(index,
                                 Qt.BackgroundColorRole)))
            painter.save()  # 先保存painter原始状态
            painter.fillRect(option.rect, color)
            painter.translate(option.rect.x(), option.rect.y())  # translate::转化(本地化:option逻辑坐标转化为painter的物理坐标,为drawContents作准备?)
            document.drawContents(painter)
            painter.restore()   # restore::恢复(恢复painter状态)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):  #option::项(包含项的所有状态)
        fm = option.fontMetrics  # 选项.字体度量值
        if index.column() == TEU:
            return QSize(fm.width("9,999,999"), fm.height())
        if index.column() == DESCRIPTION:
            text = index.model().data(index)
            document = QTextDocument()
            document.setDefaultFont(option.font)
            document.setHtml(text)
            return QSize(document.idealWidth() + 5, fm.height())    # idealWidth::理想_宽度
        return QStyledItemDelegate.sizeHint(self, option, index)

    # 创建编辑器
    def createEditor(self, parent, option, index):
        if index.column() == TEU:
            spinbox = QSpinBox(parent)
            spinbox.setRange(0, 200000)
            spinbox.setSingleStep(1000)
            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return spinbox
        elif index.column() == OWNER:
            combobox = QComboBox(parent)
            combobox.addItems(sorted(index.model().owners))
            combobox.setEditable(True)  # setEditable::设置_可编辑
            return combobox
        elif index.column() == COUNTRY:
            combobox = QComboBox(parent)
            combobox.addItems(sorted(index.model().countries))
            combobox.setEditable(True)
            return combobox
        elif index.column() == NAME:
            editor = QLineEdit(parent)
            self.connect(editor, SIGNAL("returnPressed()"), self.commitAndCloseEditor)
            return editor
        elif index.column() == DESCRIPTION:
            editor = richtextlineedit.RichTextLineEdit(parent)  # rich,text,line,edit::富_文本_行_编辑框(自定义)
            self.connect(editor, SIGNAL("returnPressed()"), self.commitAndCloseEditor)
            return editor
        else:
            return QStyledItemDelegate.createEditor(self, parent, option, index)

    def commitAndCloseEditor(self):
        editor = self.sender()
        if isinstance(editor, (QTextEdit, QLineEdit)):
            self.emit(SIGNAL("commitData(QWidget*)"), editor)
            self.emit(SIGNAL("closeEditor(QWidget*)"), editor)

    # 定义各栏设置数据的方式.
    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole)
        if index.column() == TEU:   # TEU栏
            if text is None:
                value = 0
            elif isinstance(text, int):
                value = text
            else:
                value = int(re.sub(r"[., ]", "", text))  # 将".,"替换为""空白字符.::https://zhidao.baidu.com/question/369467791671548644.html
            editor.setValue(value)
        elif index.column() in (OWNER, COUNTRY):    # 物主,国家 栏.
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)
        elif index.column() == NAME:    # 名称 栏.
            editor.setText(text)
        elif index.column() == DESCRIPTION:  # 描述 栏.
            editor.setHtml(text)
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):   # 设置_模型_数据
        if index.column() == TEU:
            model.setData(index, editor.value())
        elif index.column() in (OWNER, COUNTRY):
            model.setData(index, editor.currentText())
        elif index.column() == NAME:
            model.setData(index, editor.text())
        elif index.column() == DESCRIPTION:
            model.setData(index, editor.toSimpleHtml())
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)

def generateFakeShips():    # 生成_伪造_船舶
    for name, owner, country, teu, description in (
("Emma M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 151687,
 "<b>W\u00E4rtsil\u00E4-Sulzer RTA96-C</b> main engine,"
 "<font color=green>109,000 hp</font>"),
("MSC Pamela", "MSC", "Liberia", 90449,
 "Draft <font color=green>15m</font>"),
("Colombo Express", "Hapag-Lloyd", "Germany", 93750,
 "Main engine, <font color=green>93,500 hp</font>"),
("Houston Express", "Norddeutsche Reederei", "Germany", 95000,
 "Features a <u>twisted leading edge full spade rudder</u>. "
 "Sister of <i>Savannah Express</i>"),
("Savannah Express", "Norddeutsche Reederei", "Germany", 95000,
 "Sister of <i>Houston Express</i>"),
("MSC Susanna", "MSC", "Liberia", 90449, ""),
("Eleonora M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 151687,
 "Captain <i>Hallam</i>"),
("Estelle M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 151687,
 "Captain <i>Wells</i>"),
("Evelyn M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 151687,
  "Captain <i>Byrne</i>"),
("Georg M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
("Gerd M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
("Gjertrud M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
("Grete M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
("Gudrun M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
("Gunvor M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 97933, ""),
("CSCL Le Havre", "Danaos Shipping", "Cyprus", 107200, ""),
("CSCL Pusan", "Danaos Shipping", "Cyprus", 107200,
 "Captain <i>Watts</i>"),
("Xin Los Angeles", "China Shipping Container Lines (CSCL)",
 "Hong Kong", 107200, ""),
("Xin Shanghai", "China Shipping Container Lines (CSCL)", "Hong Kong",
 107200, ""),
("Cosco Beijing", "Costamare Shipping", "Greece", 99833, ""),
("Cosco Hellas", "Costamare Shipping", "Greece", 99833, ""),
("Cosco Guangzho", "Costamare Shipping", "Greece", 99833, ""),
("Cosco Ningbo", "Costamare Shipping", "Greece", 99833, ""),
("Cosco Yantian", "Costamare Shipping", "Greece", 99833, ""),
("CMA CGM Fidelio", "CMA CGM", "France", 99500, ""),
("CMA CGM Medea", "CMA CGM", "France", 95000, ""),
("CMA CGM Norma", "CMA CGM", "Bahamas", 95000, ""),
("CMA CGM Rigoletto", "CMA CGM", "France", 99500, ""),
("Arnold M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 93496,
 "Captain <i>Morrell</i>"),
("Anna M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 93496,
 "Captain <i>Lockhart</i>"),
("Albert M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 93496,
 "Captain <i>Tallow</i>"),
("Adrian M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 93496,
 "Captain <i>G. E. Ericson</i>"),
("Arthur M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 93496, ""),
("Axel M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 93496, ""),
("NYK Vega", "Nippon Yusen Kaisha", "Panama", 97825, ""),
("MSC Esthi", "MSC", "Liberia", 99500, ""),
("MSC Chicago", "Offen Claus-Peter", "Liberia", 90449, ""),
("MSC Bruxelles", "Offen Claus-Peter", "Liberia", 90449, ""),
("MSC Roma", "Offen Claus-Peter", "Liberia", 99500, ""),
("MSC Madeleine", "MSC", "Liberia", 107551, ""),
("MSC Ines", "MSC", "Liberia", 107551, ""),
("Hannover Bridge", "Kawasaki Kisen Kaisha", "Japan", 99500, ""),
("Charlotte M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Clementine M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Columbine M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Cornelia M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Chicago Express", "Hapag-Lloyd", "Germany", 93750, ""),
("Kyoto Express", "Hapag-Lloyd", "Germany", 93750, ""),
("Clifford M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Sally M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Sine M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Skagen M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Sofie M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Sor\u00F8 M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Sovereing M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Susan M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Svend M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Svendborg M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("A.P. M\u00F8ller", "M\u00E6rsk Line", "Denmark", 91690,
 "Captain <i>Ferraby</i>"),
("Caroline M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Carsten M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Chastine M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("Cornelius M\u00E6rsk", "M\u00E6rsk Line", "Denmark", 91690, ""),
("CMA CGM Otello", "CMA CGM", "France", 91400, ""),
("CMA CGM Tosca", "CMA CGM", "France", 91400, ""),
("CMA CGM Nabucco", "CMA CGM", "France", 91400, ""),
("CMA CGM La Traviata", "CMA CGM", "France", 91400, ""),
("CSCL Europe", "Danaos Shipping", "Cyprus", 90645, ""),
("CSCL Africa", "Seaspan Container Line", "Cyprus", 90645, ""),
("CSCL America", "Danaos Shipping ", "Cyprus", 90645, ""),
("CSCL Asia", "Seaspan Container Line", "Hong Kong", 90645, ""),
("CSCL Oceania", "Seaspan Container Line", "Hong Kong", 90645,
 "Captain <i>Baker</i>"),
("M\u00E6rsk Seville", "Blue Star GmbH", "Liberia", 94724, ""),
("M\u00E6rsk Santana", "Blue Star GmbH", "Liberia", 94724, ""),
("M\u00E6rsk Sheerness", "Blue Star GmbH", "Liberia", 94724, ""),
("M\u00E6rsk Sarnia", "Blue Star GmbH", "Liberia", 94724, ""),
("M\u00E6rsk Sydney", "Blue Star GmbH", "Liberia", 94724, ""),
("MSC Heidi", "MSC", "Panama", 95000, ""),
("MSC Rania", "MSC", "Panama", 95000, ""),
("MSC Silvana", "MSC", "Panama", 95000, ""),
("M\u00E6rsk Stralsund", "Blue Star GmbH", "Liberia", 95000, ""),
("M\u00E6rsk Saigon", "Blue Star GmbH", "Liberia", 95000, ""),
("M\u00E6rsk Seoul", "Blue Star Ship Managment GmbH", "Germany",
 95000, ""),
("M\u00E6rsk Surabaya", "Offen Claus-Peter", "Germany", 98400, ""),
("CMA CGM Hugo", "NSB Niederelbe", "Germany", 90745, ""),
("CMA CGM Vivaldi", "CMA CGM", "Bahamas", 90745, ""),
("MSC Rachele", "NSB Niederelbe", "Germany", 90745, ""),
("Pacific Link", "NSB Niederelbe", "Germany", 90745, ""),
("CMA CGM Carmen", "E R Schiffahrt", "Liberia", 89800, ""),
("CMA CGM Don Carlos", "E R Schiffahrt", "Liberia", 89800, ""),
("CMA CGM Don Giovanni", "E R Schiffahrt", "Liberia", 89800, ""),
("CMA CGM Parsifal", "E R Schiffahrt", "Liberia", 89800, ""),
("Cosco China", "E R Schiffahrt", "Liberia", 91649, ""),
("Cosco Germany", "E R Schiffahrt", "Liberia", 89800, ""),
("Cosco Napoli", "E R Schiffahrt", "Liberia", 89800, ""),
("YM Unison", "Yang Ming Line", "Taiwan", 88600, ""),
("YM Utmost", "Yang Ming Line", "Taiwan", 88600, ""),
("MSC Lucy", "MSC", "Panama", 89954, ""),
("MSC Maeva", "MSC", "Panama", 89954, ""),
("MSC Rita", "MSC", "Panama", 89954, ""),
("MSC Busan", "Offen Claus-Peter", "Panama", 89954, ""),
("MSC Beijing", "Offen Claus-Peter", "Panama", 89954, ""),
("MSC Toronto", "Offen Claus-Peter", "Panama", 89954, ""),
("MSC Charleston", "Offen Claus-Peter", "Panama", 89954, ""),
("MSC Vittoria", "MSC", "Panama", 89954, ""),
("Ever Champion", "NSB Niederelbe", "Marshall Islands", 90449,
 "Captain <i>Phillips</i>"),
("Ever Charming", "NSB Niederelbe", "Marshall Islands", 90449,
 "Captain <i>Tonbridge</i>"),
("Ever Chivalry", "NSB Niederelbe", "Marshall Islands", 90449, ""),
("Ever Conquest", "NSB Niederelbe", "Marshall Islands", 90449, ""),
("Ital Contessa", "NSB Niederelbe", "Marshall Islands", 90449, ""),
("Lt Cortesia", "NSB Niederelbe", "Marshall Islands", 90449, ""),
("OOCL Asia", "OOCL", "Hong Kong", 89097, ""),
("OOCL Atlanta", "OOCL", "Hong Kong", 89000, ""),
("OOCL Europe", "OOCL", "Hong Kong", 89097, ""),
("OOCL Hamburg", "OOCL", "Marshall Islands", 89097, ""),
("OOCL Long Beach", "OOCL", "Marshall Islands", 89097, ""),
("OOCL Ningbo", "OOCL", "Marshall Islands", 89097, ""),
("OOCL Shenzhen", "OOCL", "Hong Kong", 89097, ""),
("OOCL Tianjin", "OOCL", "Marshall Islands", 89097, ""),
("OOCL Tokyo", "OOCL", "Hong Kong", 89097, "")):
        yield Ship(name, owner, country, teu, description)

