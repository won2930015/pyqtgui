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
import gzip
from PyQt4.QtCore import *
from PyQt4.QtXml import *

CODEC = "utf-8"
NEWPARA = chr(0x2029)  # xml分隔符
NEWLINE = chr(0x2028)  # xml换行符
DATEFORMAT = "ddd MMM d, yyyy"


def encodedNewlines(text):
    return text.replace("\n\n", NEWPARA).replace("\n", NEWLINE)


def decodedNewlines(text):
    return text.replace(NEWPARA, "\n\n").replace(NEWLINE, "\n")


# 电影_对象类
class Movie(object):
    """A Movie object holds the details of a movie.
    
    The data held are the title, year, minutes length, date acquired,
    and notes. If the year is unknown it is set to 1890. If the minutes
    is unknown it is set to 0. The title and notes are held as strings,
    and the notes may contain embedded newlines. Both are plain text,
    and can contain any Unicode characters. The title cannot contain
    newlines or tabs, but the notes can contain both. The date acquired
    is held as a QDate.
    """

    UNKNOWNYEAR = 1890  # 未知年份
    UNKNOWNMINUTES = 0  # 未知分钟

    def __init__(self, title=None, year=UNKNOWNYEAR,
            minutes=UNKNOWNMINUTES, acquired=None, location=None,
            notes=None):
        self.title = title
        self.year = year
        self.minutes = minutes
        self.acquired = (acquired if acquired is not None
                                  else QDate.currentDate())
        self.location = location
        self.notes = notes


#  电影_容器类
class MovieContainer(object):
    """A MovieContainer holds a set of Movie objects.

    The movies are held in a canonicalized order based on their title
    and year, so if either of these fields is changed the movies must be
    re-sorted. For this reason (and to maintain the dirty flag), all
    updates to movies should be made through this class's updateMovie()
    method.
    """

    MAGIC_NUMBER = 0x3051E  # 文件魔数号
    OLD_FILE_VERSION = 100  # 旧文件号
    FILE_VERSION = 101  # 文件版本号


    def __init__(self):
        self.__fname = ""
        self.__movies = []
        self.__movieFromId = {}
        self.__dirty = False

    def key(self, title, year):
        text = title.lower()
        if text.startswith("a "):
            text = text[2:]
        elif text.startswith("an "):
            text = text[3:]
        elif text.startswith("the "):
            text = text[4:]
        parts = text.split(" ", 1)
        if parts[0].isdigit():  # isdigit::is数字
            text = "{0:08d} ".format(int(parts[0]))  # 例00000018::返回8位整数序号不足位用0填充.
            if len(parts) > 1:
                text += parts[1]
        return "{}\t{}".format(text.replace(" ", ""), year)

    def isDirty(self):
        return self.__dirty

    def setDirty(self, dirty=True):
        self.__dirty = dirty

    def clear(self, clearFilename=True):
        self.__movies = []
        self.__movieFromId = {}
        if clearFilename:
            self.__fname = ""
        self.__dirty = False

    def movieFromId(self, id):
        """Returns the movie with the given Python ID."""
        return self.__movieFromId[id]  # 字典,返回value


    def movieAtIndex(self, index):
        """Returns the index-th movie."""
        return self.__movies[index][1]  # 返回索引的列表项 的第二个元素movie ##.__movies[[key,movie],...]

    def add(self, movie):
        """Adds the given movie to the list if it isn't already
        present. Returns True if added; otherwise returns False."""
        if id(movie) in self.__movieFromId:
            return False
        key = self.key(movie.title, movie.year)
        bisect.insort_left(self.__movies, [key, movie])
        self.__movieFromId[id(movie)] = movie
        self.__dirty = True
        return True

    def delete(self, movie):
        """Deletes the given movie from the list and returns True;
        returns False if the movie isn't in the list."""
        if id(movie) not in self.__movieFromId:
            return False
        key = self.key(movie.title, movie.year)
        i = bisect.bisect_left(self.__movies, [key, movie])
        del self.__movies[i]
        del self.__movieFromId[id(movie)]
        self.__dirty = True
        return True

    def updateMovie(self, movie, title, year, minutes=None, location=None, notes=None):
        if minutes is not None:
            movie.minutes = minutes
        if location is not None:
            movie.location = location
        if notes is not None:
            movie.notes = notes
        if title != movie.title or year != movie.year:
            key = self.key(movie.title, movie.year)
            i = bisect.bisect_left(self.__movies, [key, movie])
            self.__movies[i][0] = self.key(title, year)
            movie.title = title
            movie.year = year
            self.__movies.sort()
        self.__dirty = True

    def __iter__(self):
        for pair in iter(self.__movies):
            yield pair[1]

    def __len__(self):
        return len(self.__movies)

    def setFilename(self, fname):
        self.__fname = fname

    def filename(self):
        return self.__fname

    @staticmethod
    def formats():
        return "*.mqb"

    def save(self, fname=""):
        if fname:
            self.__fname = fname
        if self.__fname.endswith(".mqb"):
            return self.saveQDataStream()
        return False, "Failed to save: invalid file extension"

    def load(self, fname=""):
        if fname:
            self.__fname = fname
        if self.__fname.endswith(".mqb"):
            return self.loadQDataStream()
        return False, "Failed to load: invalid file extension"

    def saveQDataStream(self):
        error = None
        file = None
        try:
            file = QFile(self.__fname)
            if not file.open(QIODevice.WriteOnly):
                raise IOError(file.errorString())
            stream = QDataStream(file)
            stream.writeInt32(MovieContainer.MAGIC_NUMBER)  # 写入文件魔数号
            stream.writeInt32(MovieContainer.FILE_VERSION)  # 写入文件版本号
            stream.setVersion(QDataStream.Qt_4_2)  # 设置数据流版本
            for key, movie in self.__movies:
                stream.writeQString(movie.title)
                stream.writeInt16(movie.year)
                stream.writeInt16(movie.minutes)
                stream.writeQString(
                        movie.acquired.toString(Qt.ISODate))
                stream.writeQString(movie.location)  # 电影.地区
                stream.writeQString(movie.notes)
        except EnvironmentError as e:
            error = "Failed to save: {}".format(e)
        finally:
            if file is not None:
                file.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Saved {} movie records to {}".format(
                    len(self.__movies),
                    QFileInfo(self.__fname).fileName())

    def loadQDataStream(self):
        error = None
        file = None
        try:
            file = QFile(self.__fname)
            if not file.open(QIODevice.ReadOnly):
                raise IOError(file.errorString())
            stream = QDataStream(file)
            magic = stream.readInt32()
            if magic != MovieContainer.MAGIC_NUMBER:
                raise IOError("unrecognized file type")
            version = stream.readInt32()
            if version < MovieContainer.OLD_FILE_VERSION:
                raise IOError("old and unreadable file format")
            elif version > MovieContainer.FILE_VERSION:
                raise IOError("new and unreadable file format")
            new = (False if version == MovieContainer.OLD_FILE_VERSION
                   else True)
            stream.setVersion(QDataStream.Qt_4_2)  # 设置数据流版本.
            self.clear(False)
            while not stream.atEnd():
                title = stream.readQString()
                year = stream.readInt16()
                minutes = stream.readInt16()
                acquired = QDate.fromString(stream.readQString(),
                                            Qt.ISODate)
                location = ""
                if new:  # 如果是新版本的文件时执行.
                    location = stream.readQString()
                notes = stream.readQString()
                self.add(Movie(title, year, minutes, acquired,
                               location, notes))
        except EnvironmentError as e:
            error = "Failed to load: {}".format(e)
        finally:
            if file is not None:
                file.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Loaded {} movie records from {}".format(
                    len(self.__movies),
                    QFileInfo(self.__fname).fileName())

    # 导出来 xml 文件.
    def exportXml(self, fname):
        error = None
        fh = None
        try:
            fh = QFile(fname)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec(CODEC)
            stream << ("<?xml version='1.0' encoding='{}'?>\n"   # 写mxl文件头
                       "<!DOCTYPE MOVIES>\n"
                       "<MOVIES VERSION='1.0'>\n".format(CODEC))
            for key, movie in self.__movies:
                stream << ("<MOVIE YEAR='{}' MINUTES='{}' "
                           "ACQUIRED='{}'>\n".format(movie.year,
                           movie.minutes,
                           movie.acquired.toString(Qt.ISODate))) \
                       << "<TITLE>" << Qt.escape(movie.title) \
                       << "</TITLE>\n" << "<LOCATION>"  # Qt.escape(movie.title)转义为适合的xml字符。
                if movie.location:
                    stream << "\n" << Qt.escape(movie.location)
                stream << "\n</LOCATION>\n" << "<NOTES>"  # Qt.escape(movie.title)转义为适合的xml字符。
                if movie.notes:
                    stream << "\n" << Qt.escape(  # 字符转义.
                            encodedNewlines(movie.notes))  # 将notes字段分隔符,换行符\n\n,\n转换成 mxl格式的分隔符,换行符 row18 -row28
                stream << "\n</NOTES>\n</MOVIE>\n"
            stream << "</MOVIES>\n"
        except EnvironmentError as e:
            error = "Failed to export: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Exported {} movie records to {}".format(
                    len(self.__movies),
                    QFileInfo(fname).fileName())

    # 用dom方式解析mxl文件::(将文件载入内存后解析,较耗内存)
    def importDOM(self, fname):
        dom = QDomDocument()  # 创建Dom对象
        error = None
        fh = None
        try:
            fh = QFile(fname)  # 创建文件对象
            if not fh.open(QIODevice.ReadOnly):  # 设置只读
                raise IOError(fh.errorString())
            if not dom.setContent(fh):  # 设置dom内容为fh
                raise ValueError("could not parse XML")
        except (IOError, OSError, ValueError) as e:
            error = "Failed to import: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
        try:
            self.populateFromDOM(dom)
        except ValueError as e:
            return False, "Failed to import: {}".format(e)
        self.__fname = ""
        self.__dirty = True
        return True, "Imported {} movie records from {}".format(
                    len(self.__movies), QFileInfo(fname).fileName())

    # 填充 从 DOM
    def populateFromDOM(self, dom):
        '''
        xml文件结构
        <MOVIES>
            <MOVIE>  # 1
                YEAR      # 属性
                MINUTES
                ACQUIRED
                <TITLE></TITLE>  # 节点
                <NOTES></NOTES>
            </MOVIE>
            <MOVIE>  # 2
                ... ...
            </MOVIE>
        </MOVIES>
        '''
        root = dom.documentElement()  # 引用内容元素
        if root.tagName() != "MOVIES":  # 根.标签名!='MOVIES'时
            raise ValueError("not a Movies XML file")
        self.clear(False)
        node = root.firstChild()  # 第一孩子
        while not node.isNull():
            if node.toElement().tagName() == "MOVIE":  # toElement：to元素
                self.readMovieNode(node.toElement())
            node = node.nextSibling()  # 下一兄弟

    def readMovieNode(self, element):

        def getText(node):
            child = node.firstChild()
            text = ""
            while not child.isNull():
                if child.nodeType() == QDomNode.TextNode:  # 判断节点类型。
                    text += child.toText().data()
                child = child.nextSibling()
            return text.strip()

        year = int(element.attribute("YEAR"))
        minutes = int(element.attribute("MINUTES"))
        ymd = element.attribute("ACQUIRED").split("-")
        if len(ymd) != 3:
            raise ValueError("invalid acquired date {}".format(
                    element.attribute("ACQUIRED")))
        acquired = QDate(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        title = notes = None
        location = ""
        node = element.firstChild()
        while title is None or notes is None:
            if node.isNull():
                raise ValueError("missing title or notes")
            if node.toElement().tagName() == "TITLE":
                title = getText(node)
            elif node.toElement().tagName() == "LOCATION":
                location = getText(node)
            elif node.toElement().tagName() == "NOTES":
                notes = getText(node)
            node = node.nextSibling()
        self.add(Movie(title, year, minutes, acquired,
                       location, decodedNewlines(notes)))

    # 用SAX方式解析mxl文件
    def importSAX(self, fname):
        error = None
        fh = None
        try:
            handler = SaxMovieHandler(self)  # Sax_电影_处理器
            parser = QXmlSimpleReader()     # parser::解析器，QXmlSimpleReader-xml_简单_读取器
            parser.setContentHandler(handler)  # 设置内容处理器
            parser.setErrorHandler(handler)  # 设置错误处理器
            fh = QFile(fname)
            input = QXmlInputSource(fh)  # xml输入源
            self.clear(False)
            if not parser.parse(input):
                raise ValueError(handler.error)
        except (IOError, OSError, ValueError) as e:
            error = "Failed to import: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__fname = ""
            self.__dirty = True
            return True, "Imported {} movie records from {}".format(
                    len(self.__movies), QFileInfo(fname).fileName())


class SaxMovieHandler(QXmlDefaultHandler):

    def __init__(self, movies):
        super(SaxMovieHandler, self).__init__()
        self.movies = movies
        self.text = ""
        self.error = None

    def clear(self):
        self.year = None
        self.minutes = None
        self.acquired = None
        self.title = None
        self.location = ""
        self.notes = None

    # 遇到开始元素时执行.如:<MOVIE>,<TITLE>,<NOTES>等
    def startElement(self, namespaceURI, localName, qName, attributes):
        if qName == "MOVIE":
            self.clear()
            self.year = int(attributes.value("YEAR"))
            self.minutes = int(attributes.value("MINUTES"))
            ymd = attributes.value("ACQUIRED").split("-")
            if len(ymd) != 3:
                raise ValueError("invalid acquired date {}".format(
                        attributes.value("ACQUIRED")))
            self.acquired = QDate(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        elif qName in ("TITLE", "NOTES"):
            self.text = ""
        return True

    # 在两相标签之间一有文本,就执行此方法.(用于读取 <TITLE></TITLE> ; <NOTES></NOTES>  # 节点的文件.
    def characters(self, text):
        self.text += text
        return True

    # 遇到关闭元素时执行.如：</MOVIE>,</TITLE>,</NOTES>等
    def endElement(self, namespaceURI, localName, qName):
        if qName == "MOVIE":
            if (self.year is None or self.minutes is None or
                self.acquired is None or self.title is None or
                self.notes is None):
                raise ValueError("incomplete movie record")
            self.movies.add(Movie(self.title, self.year, self.minutes,
                    self.acquired, self.location,
                    decodedNewlines(self.notes)))
            self.clear()
        elif qName == "TITLE":
            self.title = self.text.strip()
        elif qName == "NOTES":
            self.notes = self.text.strip()
        elif qName == "LOCATION":
            self.location = self.text.strip()
        return True


    def fatalError(self, exception):
        self.error = "parse error at line {} column {}: {}".format(
                exception.lineNumber(), exception.columnNumber(),
                exception.message())
        return False


