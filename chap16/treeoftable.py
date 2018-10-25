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

import bisect
from PyQt4.QtCore import *

KEY, NODE = range(2)


# 分支_节点
class BranchNode(object):

    def __init__(self, name, parent=None):
        super(BranchNode, self).__init__()
        self.name = name
        self.parent = parent
        self.children = []  # children::孩子集

    def __lt__(self, other):    # 小于
        if isinstance(other, BranchNode):
            return self.orderKey() < other.orderKey()
        return False

    def orderKey(self):
        return self.name.lower()

    def toString(self):
        return self.name

    def __len__(self):  # 长度
        return len(self.children)

    def childAtRow(self, row):  # 孩子_在_行(输入ROW号返回对应的NODE)
        assert 0 <= row < len(self.children)
        return self.children[row][NODE]

    def rowOfChild(self, child):    # 行_属于_孩子(输入NODE返回对应的ROW号)
        for i, item in enumerate(self.children):
            if item[NODE] == child:
                return i
        return -1

    def childWithKey(self, key):    # 孩子_和_键 (输入KEY返回对应NODE)
        if not self.children:
            return None
        # Causes a -3 deprecation warning. Solution will be to
        # reimplement bisect_left and provide a key function.
        i = bisect.bisect_left(self.children, (key, None))  # 在有序表children中查找(key, None)元组，存在时返回(key, None)在左侧的位置，(key, None)不存在返回应该插入的位置.
        if i < 0 or i >= len(self.children):   # 超出有效范围时...
            return None
        if self.children[i][KEY] == key:
            return self.children[i][NODE]
        return None

    def insertChild(self, child):  # 插入_孩子
        child.parent = self
        bisect.insort(self.children, (child.orderKey(), child))

    def hasLeaves(self):  # 有_叶节点::检查是否有叶节点.
        if not self.children:
            return False
        return isinstance(self.children[0], LeafNode)


class LeafNode(object):  # 叶_节点

    def __init__(self, fields, parent=None):    # fields::域|字段
        super(LeafNode, self).__init__()
        self.parent = parent
        self.fields = fields

    #  排序_键
    def orderKey(self):
        return "\t".join(self.fields).lower()

    # 返回字符.
    def toString(self, separator="\t"):
        return separator.join(self.fields)

    # 长度
    def __len__(self):
        return len(self.fields)

    def asRecord(self):
        record = []     # 记录
        branch = self.parent    # branch::分支
        while branch is not None:
            record.insert(0, branch.toString())  # 用 头插法 加入所有的祖先对象的KEY.
            branch = branch.parent
        assert record and not record[0]
        record = record[1:]
        return record + self.fields  # 返回从 根 到 该叶节点 的路径(包含叶节点).

    def field(self, column):    # field::域|字段.(返回叶节点的 域|字段)
        assert 0 <= column <= len(self.fields)
        return self.fields[column]


# 树_的_表格_模型, AbstractItemModel::抽象_项_模型
class TreeOfTableModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(TreeOfTableModel, self).__init__(parent)
        self.columns = 0
        self.root = BranchNode("")
        self.headers = []

    def load(self, filename, nesting, separator):  # nesting::嵌套, separator::分隔符
        assert nesting > 0   # 断言 嵌套>0
        self.nesting = nesting
        self.root = BranchNode("")
        exception = None
        fh = None
        try:
            for line in open(filename, "rU", encoding="utf-8"):  # rU 或 Ua 以读方式打开, 同时提供通用换行符支持 (PEP 278)
                if not line:  # 如果是空行 跳过..
                    continue
                self.addRecord(line.split(separator), False)
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            self.reset()    # reset::重置
            for i in range(self.columns):
                self.headers.append("Column #{}".format(i))
            if exception is not None:
                raise exception

    # 从servers.txt文件加载所有记录.
    def addRecord(self, fields, callReset=True):    # 处理...\..\servers.txt文本文件一行记录.
        assert len(fields) > self.nesting
        root = self.root
        branch = None
        for i in range(self.nesting):
            key = fields[i].lower()
            branch = root.childWithKey(key)
            if branch is not None:
                root = branch
            else:
                branch = BranchNode(fields[i])
                root.insertChild(branch)
                root = branch
        assert branch is not None
        items = fields[self.nesting:]
        self.columns = max(self.columns, len(items))
        branch.insertChild(LeafNode(items, branch))
        if callReset:
            self.reset()

    def asRecord(self, index):
        leaf = self.nodeFromIndex(index)    # leaf::叶(返回叶节点)
        if leaf is not None and isinstance(leaf, LeafNode):
            return leaf.asRecord()  # 返回从 根 到 该叶节点 的路径(包含节点).
        return []

    def rowCount(self, parent):  # 返回孩子数.(返回load入分支节点, 孩子的数量.)
        node = self.nodeFromIndex(parent)
        if node is None or isinstance(node, LeafNode):
            return 0
        return len(node)

    def columnCount(self, parent):  #返回总列数
        return self.columns

    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignTop|Qt.AlignLeft)
        if role != Qt.DisplayRole:
            return None
        node = self.nodeFromIndex(index)
        assert node is not None
        if isinstance(node, BranchNode):
            return node.toString() if index.column() == 0 else ""  # 如果是分支节点的,返回节点名.
        return node.field(index.column())  # 是叶节点的,返回当前段的内容.

    def headerData(self, section, orientation, role):   # section::节(表头的区段), orientation::方向
        if (orientation == Qt.Horizontal and
            role == Qt.DisplayRole):
            assert 0 <= section <= len(self.headers)
            return self.headers[section]
        return None


    def index(self, row, column, parent):
        assert self.root
        branch = self.nodeFromIndex(parent)
        assert branch is not None
        return self.createIndex(row, column, branch.childAtRow(row))


    def parent(self, child):
        node = self.nodeFromIndex(child)
        if node is None:
            return QModelIndex()    # 返回一个无效索引
        parent = node.parent
        if parent is None:
            return QModelIndex()
        grandparent = parent.parent  # grandparent::祖父母
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)
        assert row != -1
        return self.createIndex(row, 0, parent)

    def nodeFromIndex(self, index):  # 返回当前 项 的 叶节点
        return (index.internalPointer()  # internalPointer::内部_指针(指向叶结点|分支点)
                if index.isValid() else self.root)  # 当 index,isValid ==false 时返回 root.

