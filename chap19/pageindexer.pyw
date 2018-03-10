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

import collections      #导入_集合模块
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import walker #导入次线程 walker


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        self.lock = QReadWriteLock()    #读写锁用于保护共享数据.主线程读保护,次线程写保护.
        self.path = QDir.homePath()

        pathLabel = QLabel("Indexing path:")
        self.pathLabel = QLabel()
        self.pathLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)   #StyledPanel::可变面板 ,Sunken::凹陷

        self.pathButton = QPushButton("Set &Path...")
        self.pathButton.setAutoDefault(False)   #设置_自动_默认

        findLabel = QLabel("&Find word:")
        self.findEdit = QLineEdit()
        findLabel.setBuddy(self.findEdit)

        commonWordsLabel = QLabel("&Common words:")
        self.commonWordsListWidget = QListWidget()
        commonWordsLabel.setBuddy(self.commonWordsListWidget)

        filesLabel = QLabel("Files containing the &word:")
        self.filesListWidget = QListWidget()
        filesLabel.setBuddy(self.filesListWidget)

        filesIndexedLabel = QLabel("Files indexed")
        self.filesIndexedLCD = QLCDNumber()
        self.filesIndexedLCD.setSegmentStyle(QLCDNumber.Flat)   #setSegmentStyle::设置_ 线段_标式 ,Flat::扁平的

        wordsIndexedLabel = QLabel("Words indexed")
        self.wordsIndexedLCD = QLCDNumber()
        self.wordsIndexedLCD.setSegmentStyle(QLCDNumber.Flat)

        commonWordsLCDLabel = QLabel("Common words")
        self.commonWordsLCD = QLCDNumber()
        self.commonWordsLCD.setSegmentStyle(QLCDNumber.Flat)

        self.statusLabel = QLabel("Click the 'Set Path' "
                                  "button to start indexing")
        self.statusLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)    #setFrameStyle::设置_框架_样式

        topLayout = QHBoxLayout()
        topLayout.addWidget(pathLabel)
        topLayout.addWidget(self.pathLabel, 1)  #1::代表可扩展.
        topLayout.addWidget(self.pathButton)
        topLayout.addWidget(findLabel)
        topLayout.addWidget(self.findEdit, 1)   #1::代表可扩展.

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(filesLabel)
        leftLayout.addWidget(self.filesListWidget)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(commonWordsLabel)
        rightLayout.addWidget(self.commonWordsListWidget)

        middleLayout = QHBoxLayout()
        middleLayout.addLayout(leftLayout, 1)   #1::代表可扩展.
        middleLayout.addLayout(rightLayout)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(filesIndexedLabel)
        bottomLayout.addWidget(self.filesIndexedLCD)
        bottomLayout.addWidget(wordsIndexedLabel)
        bottomLayout.addWidget(self.wordsIndexedLCD)
        bottomLayout.addWidget(commonWordsLCDLabel)
        bottomLayout.addWidget(self.commonWordsLCD)
        bottomLayout.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addLayout(middleLayout)
        layout.addLayout(bottomLayout)
        layout.addWidget(self.statusLabel)
        self.setLayout(layout)

        self.walker = walker.Walker(self.lock, self)    #创建walker次线程对象.
        self.connect(self.walker, SIGNAL("indexed(QString)"), self.indexed) #每历遍完一个文件,触发此信号.
        self.connect(self.walker, SIGNAL("finished(bool)"), self.finished)  #历遍完所有文件触发此信号.(此例是单线程版所以只有一个walker实例)
        self.connect(self.pathButton, SIGNAL("clicked()"), self.setPath)
        self.connect(self.findEdit, SIGNAL("returnPressed()"), self.find)   #returnPressed::回车(输入)_按下
        self.setWindowTitle("Page Indexer")


    def setPath(self):
        self.pathButton.setEnabled(False)
        if self.walker.isRunning():
            self.walker.stop()
            self.walker.wait()  #wait::等候--> 锁定到线程结束运行为止.即:run()方法返回才解锁.
        path = QFileDialog.getExistingDirectory(self,
                    "Choose a Path to Index", self.path)
        if not path:
            self.statusLabel.setText("Click the 'Set Path' "
                                     "button to start indexing")
            self.pathButton.setEnabled(True)
            return
        self.path = QDir.toNativeSeparators(path)       #toNativeSeparators::to_本地化_分隔符-->将默认的'/'分隔符转换成windows的'\'分隔符.
        self.findEdit.setFocus()
        self.pathLabel.setText(self.path)
        self.statusLabel.clear()
        self.filesListWidget.clear()
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        self.walker.initialize(self.path,
                self.filenamesForWords, self.commonWords)
        self.walker.start() #start::启动次线程walker.


    def find(self):
        word = self.findEdit.text()
        if not word:
            self.statusLabel.setText("Enter a word to find in files")
            return
        self.statusLabel.clear()
        self.filesListWidget.clear()
        word = word.lower()
        if " " in word:
            word = word.split()[0]  #如果词组有空白字符分隔,查找空白字符前的单词.
        try:
            self.lock.lockForRead()
            found = word in self.commonWords
        finally:
            self.lock.unlock()
        if found:
            self.statusLabel.setText("Common words like '{}' are "
                    "not indexed".format(word))
            return
        try:
            self.lock.lockForRead()
            files = self.filenamesForWords.get(word, set()).copy()
        finally:
            self.lock.unlock()
        if not files:
            self.statusLabel.setText(
                    "No indexed file contains the word '{}'".format(word))  #没有索引文件包含这单词{}.
            return
        files = [QDir.toNativeSeparators(name) for name in      #toNativeSeparators::to_本地化_分隔符-->将默认的'/'转换成winodows的'\'.
                 sorted(files, key=str.lower)]
        self.filesListWidget.addItems(files)
        self.statusLabel.setText(
                "{} indexed files contain the word '{}'".format(    #{}个索引文件包含这单词{}.
                len(files), word))


    def indexed(self, fname):   #每历遍完一个文件执行此方法.
        self.statusLabel.setText(fname)
        self.fileCount += 1
        if self.fileCount % 25 == 0:
            self.filesIndexedLCD.display(self.fileCount)
            try:
                self.lock.lockForRead()
                indexedWordCount = len(self.filenamesForWords)
                commonWordCount = len(self.commonWords)
            finally:
                self.lock.unlock()
            self.wordsIndexedLCD.display(indexedWordCount)
            self.commonWordsLCD.display(commonWordCount)
        elif self.fileCount % 101 == 0:
            self.commonWordsListWidget.clear()
            try:
                self.lock.lockForRead()
                words = self.commonWords.copy()
            finally:
                self.lock.unlock()
            self.commonWordsListWidget.addItems(sorted(words))


    def finished(self, completed):      #历遍所有文件时执行此方法.
        self.statusLabel.setText("Indexing complete"
                                 if completed else "Stopped")
        self.finishedIndexing()


    def reject(self):
        if self.walker.isRunning():
            self.walker.stop()
            self.finishedIndexing()
        else:
            self.accept()


    def closeEvent(self, event=None):
        self.walker.stop()
        self.walker.wait()


    def finishedIndexing(self):
        self.walker.wait()
        self.filesIndexedLCD.display(self.fileCount)
        self.wordsIndexedLCD.display(len(self.filenamesForWords))
        self.commonWordsLCD.display(len(self.commonWords))
        self.pathButton.setEnabled(True)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

