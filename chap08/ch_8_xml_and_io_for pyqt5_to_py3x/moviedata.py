#!/usr/bin/env python3
"""这是一个用来进行数据处理的模块，其包含了文件的数据结构和几种不同方式的存储
使用单模块进行数据结构放置的优点是我们可以控制出入数据的所有信息。其中包含两个
主要的类，Movie类设置了一些类变量，这是电影的结构，MovieContainer类提供了数据排序、
更新、文件读取和存储相关的方法。
"""
import bisect #Python内置的对分排序法
import codecs #Python编码和解码模块
import pickle #数据储存模块 shelve更进一步
import gzip # 数据pickle后的压缩和解压
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtXml import * # 访问SAS和DOM解析器


CODEC="UTF-8"
# XML解析器无法区分空格和换行符，因此这里重新定义一下
NEWPARA=chr(0x2029)
NEWLINE=chr(0x2028)
DATEFORMAT="yyyy-MM-dd"
# print("Hello")


def encodeNewlines(text):
    return text.replace("\n",NEWLINE).replace("\n\n",NEWPARA)


def decodeNewlines(text):
    return text.replace(NEWLINE,"\n").replace(NEWPARA,"\n\n")

def intFromQStr(qstr):
    '''如果可以转换，则生成INT格式，否则，生成STR格式'''
    i=int(qstr)
    return i


class Movie(object):
    """用来储存电影详细信息的模块
    
    包括电影名称，上映时间，影片长度,是否观看，以及关于影片的备注。如果时间为止，则设置为
    1890年。如果影片长度（分钟数）未知，则设置为0。标题和备注使用QStrings存储，
    备注可能包含多行。标题和备注都是纯文字，非HTML，并且可以包含任何Unicode字符。
    标题不能包含新行或者制表符，但是备注可以。时间使用QDate格式进行储存。
    """
    UNKNOWNYEAR=1996
    UNKNOWNMINUTES=0

    def __init__(self,title=None,year=UNKNOWNYEAR,minutes=UNKNOWNMINUTES,acquired=None,locations=None,notes=None):
        self.title=title
        self.year=year
        self.minutes=minutes
        self.acquired=(acquired if acquired is not None else QDate.currentDate())
        self.notes=notes
        self.locations=locations

class MovieContainer(object):
    """一个存储电影数据的对象

    按照标题、上映时间排序，如果这两者任何发生改变，应该调用类中的update方法进行
    重新排列。
    """
    MAGIC_NUMBER=0x3051E
    # FILE_VERSION= 100
    FILE_VERSION = 200

    def __init__(self):
        self.__fname='' #QS是属于哪个类？
        self.__movies=[] #此列表用来排序显示
        self.__movieFromId={} #此字典存储相关数据，id为排列的key，movie obj为对象
        self.__dirty=False # 使用前下划线为了避免多重继承的类全局变量重复问题,
        # 在进行某项功能的类方法中就不用这样

    def key(self,title,year):
        text=str(title).lower()
        if text.startswith("a "):# 开头是a 并且是一个单独单词，可以用正则实现
            text=text[2:]
        elif text.startswith("an "):
            text=text[3:]
        elif text.startswith("the "):
            text=text[4:]
        parts=text.split(" ",1) #分一次，用来进行排序
        # 不适用于中文“20世纪危机”之类的，更多的是“2017 I LOVE YOU”这种。
        if parts[0].isdigit():
            text="{0:08d} ".format(int(parts[0]))#前面加0，固定位数
            if len(parts) >1:
                text+=parts[1] #把处理过的头和尾部接回去
        return "{0}\t{1}".format(text.replace(" ",""),year)
        #返回一个用来排序的数据结构，包括由换行符隔开的没有空格的title和year
    
    def isDirty(self):
        return self.__dirty

    def setDirty(self,dirty=True):
        self.__dirty=dirty

    def clear(self,clearFilename=None):
        self.__movies=[]
        self.__movieFromId={}
        if clearFilename:
            self.__fname=''
        self.__dirty=False
    
    def movieFromId(self,id):
        """给一个ID，返回movie对象"""
        return self.__movieFromId[id]

    def movieAtIndex(self,index):
        """给一个Index，返回movie对象"""
        return self.__movies[index][1]

    def add(self,movie):
        """如果电影不存在的话，添加到列表中去，并且返回一个bool值"""
        if id(movie) in self.__movieFromId:
            return False
        # 如何解释 id("hello")和id("hello ")返回的是同一个ID的问题
        key=self.key(movie.title,movie.year)
        bisect.insort_left(self.__movies,[key,movie])
        # 一个排序算法，将[key,movie]插入到__movies的列表中，其中key是
        # key方法中用于排序的一串字符，movie是一个obj，包含名称，时间还有其他的东西
        # 在将二元数组插入到列表中就进行了排序，速度很快。
        # 这个方法不仅会进行list的插入，并且会返回插入值得index，非常有用
        self.__movieFromId[id(movie)]=movie
        # 这个和排序不一样，按照id作为key，movie obj作为value进行字典的存储。
        self.__dirty=True
        # print(movie.notes)
        return True

    def delete(self,movie):
        """接受一个movie obj对象，
        从movie obj所存储在的MovieContainter类中删除相关object"""
        if id(movie) not in self.__movieFromId:
            return False
        key = self.key(movie.title,movie.year)
        i = bisect.bisect_left(self.__movies,[key,movie])
        # 寻找想要删除的movie object的key，然后使用bisect_left查找这个key对应的
        # index 然后删除这个index ，并且删除字典中的值
        del self.__movies[i]
        del self.__movieFromId[id(movie)]
        self.__dirty =True
        return True


    def updateMovie(self,movie,title,year,minutes=None,locations=None,notes=None):
        """更新movie存储"""
        # 如果note,minutes发生改变，直接赋值重写，但是如果title和year出了问题，
        # 那么会涉及到排序的问题，因此需要先判断是否改变，如果改变，
        # 使用movie对象的原始错误的title和year的key，然后使用bisect获取这个key的
        # index，然后重新将这个新的key写入老的位置处，最后，就可以安全的把新的title
        # 和year写入到movie的属性中。
        if minutes is not None:
            movie.minutes=minutes
        if minutes is not None:
            movie.notes=notes
        if locations is not None:
            movie.locations = locations
        if title != movie.title or year !=movie.year:
            key =self.key(movie.title,movie.year)
            i=bisect.bisect_left(self.__movies,[key,movie])
            self.__movies[i][0]=self.key(title,year)
            movie.title=title
            movie.year=year
            self.__movies.sort()
        self.__dirty=True

    def __iter__(self):
        for pair in iter(self.__movies):
            yield pair[1] #movie对象

    def __len__(self):
        return len(self.__movies)

    def setFilename(self,fname):
        self.__fname=fname

    def filename(self):
        return self.__fname


    @staticmethod
    def formats():
        # locations 仅对mpb和mpt和XML两种读写方法进行更新
        return "*.mqb *.mpb *.mqt *.mpt"
    

    def save(self,fname=''):
        if not fname=='':
            self.__fname=fname
        if self.__fname[-4:]=='.mqb':
            return self.saveQDataStream()
        elif self.__fname[-4:]=='.mpb':
            return self.savePickle()
        elif self.__fname[-4:]=='.mqt':
            return self.saveQTextStream()
        elif self.__fname[-4:]=='.mpt':
            return self.saveText()
        return False,"无效数据类型，保存失败。"

    def load(self,fname=''):
        if not fname=='':
            self.__fname=fname
        if self.__fname[-4:]=='.mqb':
            print("MQB数据类型")
            return self.loadQDataStream()
        elif self.__fname[-4:]=='.mpb':
            print("MPB数据类型")
            return self.loadPickle()
        elif self.__fname[-4:]=='.mqt':
            return self.loadQTextStream()
        elif self.__fname[-4:]=='.mpt':
            return self.loadText()
        return False,"无效数据类型，加载失败。"

    def saveQDataStream(self):
        error=None
        fh=None
        try:
            fh=QFile(self.__fname)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream=QDataStream(fh)
            stream.writeInt32(MovieContainer.MAGIC_NUMBER)
            #幻数是一个常量，用来识别自定义文件格式，因为实际文件格式的识别，也就是
            # 通过后缀名靠不住,因此需要写入一个常数和文件版本
            stream.writeInt32(MovieContainer.FILE_VERSION)
            # PyQt不能够识别int型和long型的整数尺寸大小，需要手动写8 16 32 64
            # 对于float 使用readDouble()和writeDouble()来读写
            stream.setVersion(QDataStream.Qt_5_9)
            # 在设置过幻数和文件版本后进行DS版本设置，要设置成其可以读写剩余数据的相应版本
            # ？？？？？？
            writemoviedata=[]
            for key,movie in self.__movies:
                writemoviedata.append(movie)
                print("子项目--->",writemoviedata)
            for movie in writemoviedata:
                print(movie.title,movie.year,movie.minutes,movie.acquired,movie.notes)
                stream << movie.title
                # title是QString数据，作为二进制写入 QDate QImage也可以使用
                # 将右侧数据写入左侧数据流中，C++方式，<<在这里会自动重载
                # 但对于整数，必须使用wINT wUint 
                #因为写入的是整数，因此不需要进行格式化的操作
                stream.writeInt16(movie.year)#Int
                stream.writeInt16(movie.minutes)#Int
                stream << movie.acquired << movie.notes#QDate QString
                #为什么要这么写？
        except EnvironmentError as _err:
            error="保存失败，%s"%_err
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False,error
            self.__dirty=False
            return True,"保存 %s 条电影记录到 %s"%(len(self.__movies),QFileInfo(self.__fname).fileName())

    def loadQDataStream(self):
        error=None
        fh=None
        try: #此处函数输出一个bool表示成功与否的同时自己抛出异常，否则就需要在主程序写try自己捕捉异常
            fh=QFile(self.__fname)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QDataStream(fh)
            magic=stream.readInt32()
            if magic != MovieContainer.MAGIC_NUMBER:
                raise IOError("未知文件类型")
            version = stream.readInt32()
            if version < MovieContainer.FILE_VERSION:
                raise IOError("过于老旧的文件类型")
            elif version > MovieContainer.FILE_VERSION:
                raise IOError("过于新的不支持的文件类型")
            stream.setVersion(QDataStream.Qt_5_9)
            self.clear(False) #尽可能晚的进行这一步，清空数据
            notes = ''
            title = '' #对于非数字型数据都需要先声明，然后再read（year和minu不需要）
            acquired = QDate()
            while not stream.atEnd():
                stream >> title
                year = stream.readInt16()
                minutes = stream.readInt16()
                stream >> acquired >> notes
                print(title,year,minutes,acquired,notes)
                self.add(Movie(title,year,minutes,acquired,notes))
        except EnvironmentError as _err:
            error = "加载失败 %s"%_err
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False,error
            self.__dirty = False
            return True,"加载了 %s 部电影数据，从 %s"%(len(self.__movies), QFileInfo(self.__fname).fileName())



    def savePickle(self):
        # 使用QDataStream的优点是其速度足够快，虽然Pickle也很快，不过Qt可以存储图片之类的
        # 二进制数据，因此性能更好
        error = None
        fh = None
        try:
            fh = gzip.open(str(self.__fname),'wb')
            pickle.dump(self.__movies,fh,2)
            #牺牲磁盘空间换取性能
        except Exception as _err:
            error = "保存失败 %s"%_err
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False,error
            self.__dirty = False
            return True,"保存 %s 条电影记录到 %s"%(len(self.__movies),QFileInfo(self.__fname).fileName())
    
    def loadPickle(self):
        fh=None
        error=None
        try:
            fh=gzip.open(str(self.__fname),'rb')
            self.clear(False)
            self.__movies=pickle.load(fh)
            for key,movie in self.__movies:
                self.__movieFromId[id(movie)]=movie
        except Exception as _err:
            error = "读取失败 %s"%_err
        finally:
            if fh is not None:
                    fh.close()
            if error is not None:
                return False,error
            self.__dirty=False
            return True,"读取 %s 条记录从 %s"%(len(self.__movies),QFileInfo(self.__fname).fileName())

    def saveQTextStream(self):
        fh=None
        error=None
        try:
            fh=QFile(self.__fname)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec(CODEC)
            for key,movie in self.__movies:
                stream << "{{MOVIE}} " << movie.title << "\n" \
                << movie.year << " " << movie.minutes << " " \
                << movie.acquired.toString(Qt.ISODate) \
                << "\n{NOTES}"
                if not movie.notes=='':
                    stream << "\n" << movie.notes
                stream << "\n{{ENDMOVIE}}\n"
        except Exception as _err:
            error = "保存出错 %s"%_err
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False,error
            self.__dirty=False
            return True,"保存 %s 条记录到 %s"%(len(self.__movies),QFileInfo(self.__fname).fileName())

    def saveText(self):
        fh=None
        error=None
        try:
            fh=codecs.open(str(self.__fname),'w',CODEC) #为什么要采用这个模块？
            #写入write()即便是文件重新打开也不空行,
            for key,movie in self.__movies:
                fh.write("{{MOVIE}} %s\n%s %s %s\n{LOCATIONS}\n%s\n{NOTES}"%(str(movie.title),str(movie.year),str(movie.minutes),
                                                        str(movie.acquired.toString(Qt.ISODate)),str(movie.locations)))
                if not movie.notes=='':
                    fh.write("\n%s"%movie.notes)
                try:
                    fh.write("\n{{ENDMOVIE}}\n")
                except:
                    error="无法完全保存数据"
        except Exception as _err:
            error="保存出错，%s"%(_err)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False,error
            self.__dirty=False
            return True,"成功保存%s条电影信息到%s"%(len(self.__movies),QFileInfo(self.__fname).fileName())

    
    def loadText(self):
        # '需要针对老版本进行优化，当locations不存在时候赋给空字符串'
        fh=None
        error=None
        try:
            fh=codecs.open(str(self.__fname),'rU',CODEC) #U表示在全平台适用，\r\n和\n都可以正确读取
            self.clear(False)
            while True:
                title=year=minutes=acquired=None
                locations=notes=''
                line=fh.readline()
                if not line:
                    break
                if not line.startswith("{{MOVIE}}"):
                    raise ValueError("未找到电影记录")
                else:
                    title=str(line[len("{{MOVIE}}"):].strip())
                line=fh.readline()
                try:
                    lineinfo=line.split(" ")
                    if len(lineinfo)==3:
                        year=int(lineinfo[0])
                        minutes=int(lineinfo[1])
                        ymd=lineinfo[2].split("-")
                        acquired=QDate(int(ymd[0]),int(ymd[1]),int(ymd[2]))
                    else:raise ValueError("数据不匹配或数据转换错误")
                except Exception as _err:
                    raise ValueError("时间和日期数据不匹配 %s"%_err)
                line=fh.readline()
                if not '{LOCATIONS}' in line:
                    locations=None
                else:
                    line=fh.readline()
                    locations=str(line) #这里假定Location只有一行
                    line=fh.readline()
                if not line:
                    raise ValueError("数据结构不完整")
                if line != "{NOTES}\n":
                    raise ValueError("附录出现问题")
                while True:
                    line=fh.readline()
                    if not line:
                        raise ValueError("缺少ENDMOVIE标签")
                    if line.startswith("{{ENDMOVIE}}"):
                        if (title is None or year is None or minutes is None or acquired is None or notes is None):
                            raise ValueError("数据不完整")
                        self.add(Movie(title,year,minutes,acquired,locations,notes)) # trimmed是什么？？？？？？
                        break
                    else:
                        notes +=str(line)
                
        except Exception as _err:
            error="加载出错，%s"%(_err)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False,error
            self.__dirty=False
            return True,"成功加载%s条电影信息到%s"%(len(self.__movies),QFileInfo(self.__fname).fileName())

    
    def exportXml(self,fname):

        fh=None
        error=None

        try: #是否存在escape这个函数 是否存在tostring这个方法？？？？？？
        # escape对要保存的数字进行转义，以便可以存储为正常的xml字符串，其接收一个qstring字符串
            fh=QFile(fname)
            if not fh.open(QIODevice.WriteOnly):
                 raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec(CODEC)
            stream << ( "<?xml version='1.0' encoding='%s' ?>\n"
                        "<!DOCTYPE MOVIES>\n"
                        "<MOVIES VERSION='1.0'>\n"%CODEC)
            for key,movie in self.__movies:
                stream << ("<MOVIE YEAR='%s' MINUTES='%s' ACQUIRED='%s'>\n"%(movie.year,movie.minutes,movie.acquired.toString(Qt.ISODate))) \
                << "<TITLE>" << movie.title << ("</TITLE>\n<LOCATIONS>") \
                << movie.locations << "</LOCATIONS>\n<NOTES>"
                if not movie.notes=='':
                    stream << "\n" << encodeNewlines(movie.notes)
                stream << "\n</NOTES>\n</MOVIE>\n"
            stream << "</MOVIES>\n"  

        except Exception as _err:
            error = "保存出错 %s"%_err
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False,error
            self.__dirty=False
            return True,"保存 %s 条记录到 %s"%(len(self.__movies),QFileInfo(self.__fname).fileName())

    def importDOM(self,fname):
        dom=QDomDocument()
        fh=None
        error=None
        try:
            fh=open(fname,mode='r',encoding='utf-8')
            # fh=QFile(fname)
            # 使用qfile出现编码问题
            fh=str(fh.read())
            # print(fh)
            # if not fh.open(QIODevice.WriteOnly):
            #     raise ValueError("文件只读，无法加载")
            if not dom.setContent(fh): #读取文档
                raise ValueError("无法解析XML文档")
        except Exception as _err:
            error="读取出错，%s"%(_err)
        finally:
            if fh is not None:
                # fh.close()
                pass
            if error is not None:
                return False,error
        try:
            self.populateFromDOM(dom)
        except Exception as _err:
            return False,"DOM导入失败 %s"%_err
        self.__fname=''
        self.__dirty=True #有机会另存为别的文件
        return True,"成功读取%s条电影信息从%s"%(len(self.__movies),QFileInfo(fname).fileName())
    

    def populateFromDOM(self,dom):
        '''此函数从一个DOM的root中遍历所有的node(一级)'''
        root=dom.documentElement()
        if root.tagName() != "MOVIES":
            raise ValueError("XML类型不匹配,提取到的XMLTAG为：%s，%s"%(root.tagName(),root.text()))
        self.clear(False)
        node=root.firstChild()
        while not node.isNull():
            if node.toElement().tagName() =="MOVIE":
                self.readMovieNode(node.toElement())
            node=node.nextSibling()


    # element在这里指的是MOVIE
    def readMovieNode(self,element):
        '''此函数遍历root/node(一级)下的所有子node，并将其捕获，转换格式后写回数据库'''


        def getText(node):
            '''此助手函数遍历一个给定层级的node，然后返回其所有的text'''
            child=node.firstChild()
            text=''
            while not child.isNull():
                if child.nodeType() ==  QDomNode.TextNode:
                    text += child.toText().data() #？？？？？？？？？？？？？？？？？这个方法有吗？
                child=child.nextSibling()
            return text

        # 对于属性来说，可以使用attr来取出，转换成为对应格式
        year=intFromQStr(element.attribute("YEAR"))
        minutes=intFromQStr(element.attribute("MINUTES"))
        ymd=element.attribute("ACQUIRED").split("-")
        # print(ymd)
        if len(ymd)!=3:
            raise ValueError("日期数据错误 %s"%element.attribute("ACQUIRED"))
        acquired=QDate(intFromQStr(ymd[0]),intFromQStr(ymd[1]),intFromQStr(ymd[2]))
        title=notes=locations=None
        node=element.firstChild()

        while title is None or notes is None:
            if node.isNull():
                raise ValueError("缺少题目或者附录")
            if node.toElement().tagName() =="TITLE":
                title=getText(node)
            elif node.toElement().tagName() == "LOCATIONS":
                locations = getText(node)
            elif node.toElement().tagName() == "NOTES":
                notes=getText(node)
            node=node.nextSibling() #步进
        if title=='':
            raise ValueError("缺少标题")
        if locations==None:
            locations=''
        self.add(Movie(title,year,minutes,acquired,locations,decodeNewlines(notes)))

    def importSAX(self,fname):
        error=None
        fh=None
        try:

            handler=SaxMovieHandler(self)
            parser=QXmlSimpleReader()
            parser.setContentHandler(handler)
            parser.setErrorHandler(handler)
            fh=QFile(fname)
            input=QXmlInputSource(fh)
            self.clear(False)
            if not parser.parse(input):
                raise ValueError(handler.error)
        except Exception as _err:
            error="导入失败 %s"%_err
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False,error
            self.__fname=''
            self.__dirty=True
            return True,"成功读取%s条电影信息来自%s"%(len(self.__movies),QFileInfo(fname).fileName())   

class SaxMovieHandler(QXmlDefaultHandler):
    '''使用SAX的方式，内存需求不大，速度更快，但是需要创建至少一个单独的处理程序子类'''

    def __init__(self,movies):
        super(SaxMovieHandler,self).__init__()
        self.movies=movies
        self.text=''
        self.error=None

    def clear(self):
        '''用来判断数据的完整性'''
        self.year=None
        self.minutes=None
        self.acquired=None
        self.title=None
        self.locations=None
        self.notes=None

    def startElement(self,namespaceURI,localName,qName,attributes):
        '''在开始一个标签的时候进行的处理'''
        if qName =='MOVIE':
            self.clear()
            self.year=intFromQStr(attributes.value("YEAR"))
            self.minutes=intFromQStr(attributes.value("MINUTES"))
            ymd=attributes.value("ACQUIRED").split("-")
            if len(ymd) != 3:
                raise ValueError("数据格式不匹配 %s"%attributes.value("ACQUIRED"))
            self.acquired=QDate(intFromQStr(ymd[0]),intFromQStr(ymd[1]),intFromQStr(ymd[2]))
        elif qName in ('TITLE','NOTES','LOCATIONS'):
            self.text=''
        return True #每个重新实现的类方法都要返回一个bool值
    
    def characters(self,text):
        self.text +=text
        return True

    def endElement(self,namespaceURI,localName,qName):
        '''在遇到标签结束的时候进行的处理'''
        if qName == "MOVIE":
            if  self.year is None or self.minutes is None or self.acquired is None or self.title is None or \
                self.notes is None or self.title=='':
                raise ValueError("数据不完整")
            self.movies.add(Movie(self.title,self.year,self.minutes,self.acquired,self.locations,decodeNewlines(self.notes)))
            self.clear()
        elif qName == 'TITLE':
            self.title=self.text
        elif qName == "NOTES":
            self.notes = self.text
        elif qName == "LOCATIONS":
            self.locations=self.text
        return True

    def fatalError(self,exception):
        self.error="解析错误，行 %d 列 %d ：%s"%(exception.lineNumber(),exception.columnNumber(),exception.message())
        return False





        

        







