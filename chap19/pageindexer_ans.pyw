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

import collections      # 导入_集合模块
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import walker_ans as walker  # 导入次线程 walker


def isAlive(qobj):  # is_活着的
    import sip
    try:
        sip.unwrapinstance(qobj)    # unwrapinstance::解_包_实例.::解包对象得到指针(实例的引用).
    except RuntimeError:        # RuntimeError::运行时错误.
        return False
    return True


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.mutex = QMutex()
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        self.lock = QReadWriteLock()    # 读写锁用于保护共享数据.主线程读保护,次线程写保护.
        self.path = QDir.homePath()

        pathLabel = QLabel("Indexing path:")
        self.pathLabel = QLabel()
        self.pathLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)   # StyledPanel::可变面板 ,Sunken::凹陷

        self.pathButton = QPushButton("Set &Path...")
        self.pathButton.setAutoDefault(False)   # 设置_自动_默认

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
        self.filesIndexedLCD.setSegmentStyle(QLCDNumber.Flat)   # setSegmentStyle::设置_ 线段_标式 ,Flat::扁平的

        wordsIndexedLabel = QLabel("Words indexed")
        self.wordsIndexedLCD = QLCDNumber()
        self.wordsIndexedLCD.setSegmentStyle(QLCDNumber.Flat)

        commonWordsLCDLabel = QLabel("Common words")
        self.commonWordsLCD = QLCDNumber()
        self.commonWordsLCD.setSegmentStyle(QLCDNumber.Flat)

        self.statusLabel = QLabel("Click the 'Set Path' "
                                  "button to start indexing")
        self.statusLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)    # setFrameStyle::设置_框架_样式

        topLayout = QHBoxLayout()
        topLayout.addWidget(pathLabel)
        topLayout.addWidget(self.pathLabel, 1)  # 1::代表可扩展.
        topLayout.addWidget(self.pathButton)
        topLayout.addWidget(findLabel)
        topLayout.addWidget(self.findEdit, 1)   # 1::代表可扩展.

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(filesLabel)
        leftLayout.addWidget(self.filesListWidget)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(commonWordsLabel)
        rightLayout.addWidget(self.commonWordsListWidget)

        middleLayout = QHBoxLayout()
        middleLayout.addLayout(leftLayout, 1)   # 1::代表可扩展.
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

        self.walkers = []
        self.completed = []
        self.connect(self.pathButton, SIGNAL("clicked()"), self.setPath)
        self.connect(self.findEdit, SIGNAL("returnPressed()"), self.find)
        self.setWindowTitle("Page Indexer")

    def stopWalkers(self):  # 停止所有次线程.
        for walker in self.walkers:
            if isAlive(walker) and walker.isRunning():
                walker.stop()
        for walker in self.walkers:
            if isAlive(walker) and walker.isRunning():
                walker.wait()
        self.walkers = []
        self.completed = []

    def setPath(self):
        self.stopWalkers()
        self.pathButton.setEnabled(False)
        path = QFileDialog.getExistingDirectory(self,       # getExistingDirectory::获得_存在_目录
                    "Choose a Path to Index", self.path)
        if not path:
            self.statusLabel.setText("Click the 'Set Path' "
                                     "button to start indexing")
            self.pathButton.setEnabled(True)
            return
        self.statusLabel.setText("Scanning directories...")
        QApplication.processEvents()  # Needed for Windows   ,processEvents::进程_事件 ,空闲时交还进程的控制权(这样软件界面不会假死.可响应其他事件.)
        self.path = QDir.toNativeSeparators(path)       # toNativeSeparators::to_本地化_分隔符-->将默认的'/'分隔符转换成windows的'\'分隔符.
        self.findEdit.setFocus()
        self.pathLabel.setText(self.path)
        self.statusLabel.clear()
        self.filesListWidget.clear()
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)   # 创建默认字典value为set(集).
        self.commonWords = set()
        nofilesfound = True     # nofilesfound::没_文件_找到
        files = []
        index = 0
        for root, dirs, fnames in os.walk(self.path):   # os.walk(self.path)::历遍path下所有文件夹|文件.
            for name in [name for name in fnames
                         if name.endswith((".htm", ".html"))]:
                files.append(os.path.join(root, name))
                if len(files) == 1000:      # 文件每达1000个建立一个线程.
                    self.processFiles(index, files[:])
                    files = []
                    index += 1
                    nofilesfound = False
        if files:   # 不足1000个文件也用一个线程处理.
            self.processFiles(index, files[:])
            nofilesfound = False
        if nofilesfound:
            self.finishedIndexing()
            self.statusLabel.setText(
                    "No HTML files found in the given path")    # 给出的路径没有找到HTML文件.

    def processFiles(self, index, files):
        thread = walker.Walker(index, self.lock, files,
                self.filenamesForWords, self.commonWords, self)
        self.connect(thread, SIGNAL("indexed(QString,int)"), self.indexed)  # walker每历遍一个文件触发一次些信号.
        self.connect(thread, SIGNAL("finished(bool,int)"), self.finished)   # walker完成所有文件历遍时角发此信号.(这里一个walker代表了一个线程)
        self.connect(thread, SIGNAL("finished()"),
                     thread, SLOT("deleteLater()"))  # 触发deleteLater槽::册除完成的线程节省内存.
        self.walkers.append(thread)
        self.completed.append(False)
        thread.start()
        thread.wait(300)  # Needed for Windows ,wait(300)::等待(300豪秒)


    def find(self):
        word = self.findEdit.text()
        if not word:
            try:
                self.mutex.lock()
                self.statusLabel.setText("Enter a word to find in files")
            finally:
                self.mutex.unlock()
            return
        try:
            self.mutex.lock()
            self.statusLabel.clear()
            self.filesListWidget.clear()
        finally:
            self.mutex.unlock()
        word = word.lower()
        if " " in word:
            word = word.split()[0]   # 如果词组有空白字符分隔,查找空白字符前的单词.
        try:
            self.lock.lockForRead()
            found = word in self.commonWords
        finally:
            self.lock.unlock()
        if found:
            try:
                self.mutex.lock()
                self.statusLabel.setText("Common words like '{}' "
                        "are not indexed".format(word))
            finally:
                self.mutex.unlock()
            return
        try:
            self.lock.lockForRead()
            files = self.filenamesForWords.get(word, set()).copy()
        finally:
            self.lock.unlock()
        if not files:
            try:
                self.mutex.lock()
                self.statusLabel.setText("No indexed file contains "
                        "the word '{}'".format(word))           # 没有索引文件包含这单词{}.
            finally:
                self.mutex.unlock()
            return
        files = [QDir.toNativeSeparators(name) for name in      # toNativeSeparators::to_本地化_分隔符-->将默认的'/'转换成winodows的'\'.
                 sorted(files, key=str.lower)]
        try:
            self.mutex.lock()
            self.filesListWidget.addItems(files)
            self.statusLabel.setText(
                    "{} indexed files contain the word '{}'".format(        # {}个索引文件包含单词{}.
                    len(files), word))
        finally:
            self.mutex.unlock()

    def indexed(self, fname, index):    # walker每历遍完一个文件时执行此函数.
        try:
            self.mutex.lock()
            self.statusLabel.setText(fname)
            self.fileCount += 1
            count = self.fileCount
        finally:
            self.mutex.unlock()
        if count % 25 == 0:
            try:
                self.lock.lockForRead()
                indexedWordCount = len(self.filenamesForWords)
                commonWordCount = len(self.commonWords)
            finally:
                self.lock.unlock()
            try:
                self.mutex.lock()
                self.filesIndexedLCD.display(count)
                self.wordsIndexedLCD.display(indexedWordCount)
                self.commonWordsLCD.display(commonWordCount)
            finally:
                self.mutex.unlock()
        elif count % 101 == 0:
            try:
                self.lock.lockForRead()
                words = self.commonWords.copy()
            finally:
                self.lock.unlock()
            try:
                self.mutex.lock()
                self.commonWordsListWidget.clear()
                self.commonWordsListWidget.addItems(sorted(words))
            finally:
                self.mutex.unlock()

    def finished(self, completed, index):       # walker历遍完所文件时执行此函数.
        done = False        # done::已完成
        if self.walkers:
            self.completed[index] = True
            if all(self.completed):     # all(x)参数x对象的所有元素不为0、''、False或者x为空对象，则返回True，否则返回False
                try:
                    self.mutex.lock()
                    self.statusLabel.setText("Finished")
                    done = True
                finally:
                    self.mutex.unlock()
        else:
            try:
                self.mutex.lock()
                self.statusLabel.setText("Finished")
                done = True
            finally:
                self.mutex.unlock()
        if done:
            self.finishedIndexing()

    def reject(self):
        if not all(self.completed):
            self.stopWalkers()
            self.finishedIndexing()
        else:
            self.accept()

    def closeEvent(self, event=None):
        self.stopWalkers()


    def finishedIndexing(self):
        self.filesIndexedLCD.display(self.fileCount)
        self.wordsIndexedLCD.display(len(self.filenamesForWords))
        self.commonWordsLCD.display(len(self.commonWords))
        self.pathButton.setEnabled(True)
        QApplication.processEvents()  # Needed for Windows   ,processEvents::进程_事件 ,空闲时交还进程的控制权(这样软件界面不会假死.可响应其他事件.)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

