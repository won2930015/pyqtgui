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
##########################
#         次线程         #
#########################


import html.entities        # entities::实体 ,将html实体转换成unicdoe字符.
import os
import re
import sys
from PyQt4.QtCore import *


class Walker(QThread):

    COMMON_WORDS_THRESHOLD = 250    # 共同_单词_阈值
    MIN_WORD_LEN = 3
    MAX_WORD_LEN = 25
    INVALID_FIRST_OR_LAST = frozenset("0123456789_")  # INVALID_FIRST_OR_LAST::无效_头_或_尾 ,创建不可变集合-->frozenset({'4', '2', '_', '1', '9', '7', '5', '3', '6', '8', '0'})
    STRIPHTML_RE = re.compile(r"<[^>]*?>", re.IGNORECASE|re.MULTILINE)      # re.IGNORECASE::忽略大小写 ,re.MULTILINE::跨多行
    ENTITY_RE = re.compile(r"&(\w+?);|&#(\d+?);")   # (exp)::匹配exp,并捕获文本到自动命名的组里 ,\w::匹配字母，数字，下划线 ,\d::匹配数字.
    SPLIT_RE = re.compile(r"\W+", re.IGNORECASE | re.MULTILINE)       # \W+::匹配1至任意多个不是字母，数字，下划线 的字符

    def __init__(self, index, lock, files, filenamesForWords,
                 commonWords, parent=None):
        super(Walker, self).__init__(parent)
        self.index = index
        self.lock = lock
        self.files = files
        self.filenamesForWords = filenamesForWords
        self.commonWords = commonWords
        self.stopped = False
        self.mutex = QMutex()   #QMutex::互斥体-->一般用于保护 私有变量 不被别的次线程读写.
        self.completed = False  #completed::完整的


    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()


    def isStopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()


    def run(self):
        self.processFiles()
        self.stop()
        self.emit(SIGNAL("finished(bool,int)"), self.completed,      #finished::完成的.
                  self.index)


    def processFiles(self):
        def unichrFromEntity(match):    #unichrFromEntity::统一字符从实体(从实体转变为统一字符) ,match::匹配
            text = match.group(match.lastindex)     #lastindex::最后_索引
            if text.isdigit():  #isdigit::is_数字-->是实体码点 时.
                return chr(int(text))
            u = html.entities.name2codepoint.get(text)  #entities::实体 ,name2codepoint::实体名称 转 实体码点 ,实体=='€ № ‰ ' ,将实体字符名 转换成对应的unicode16进制数值
                                                        #http://blog.csdn.net/ownfire/article/details/53941723
            return chr(u) if u is not None else ""

        for fname in self.files:
            if self.isStopped():
                return
            words = set()
            fh = None
            try:
                fh = open(fname, "r", encoding="utf-8",
                          errors="ignore")
                text = fh.read()
            except EnvironmentError as e:       #EnvironmentError::环境_错误
                sys.stderr.write("Error: {}\n".format(e))
                continue
            finally:
                if fh is not None:
                    fh.close()
            if self.isStopped():
                return
            text = self.STRIPHTML_RE.sub("", text)
            text = self.ENTITY_RE.sub(unichrFromEntity, text)
            text = text.lower()
            for word in self.SPLIT_RE.split(text):
                if (self.MIN_WORD_LEN <= len(word) <=
                    self.MAX_WORD_LEN and
                    word[0] not in self.INVALID_FIRST_OR_LAST and
                    word[-1] not in self.INVALID_FIRST_OR_LAST):
                    try:
                        self.lock.lockForRead()
                        new = word not in self.commonWords
                    finally:
                        self.lock.unlock()
                    if new:
                        words.add(word)
            if self.isStopped():
                return
            for word in words:
                try:
                    self.lock.lockForWrite()
                    files = self.filenamesForWords[word]
                    if len(files) > self.COMMON_WORDS_THRESHOLD:
                        del self.filenamesForWords[word]
                        self.commonWords.add(word)
                    else:
                        files.add(fname)
                finally:
                    self.lock.unlock()
            self.emit(SIGNAL("indexed(QString,int)"), fname, self.index)
        self.completed = True

