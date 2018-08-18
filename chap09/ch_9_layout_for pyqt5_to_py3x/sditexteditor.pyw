#!/usr/bin/env python3


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qrc_resources
# 这里不许要导入SIP模块即可使用它

__version__ = "0.0.1"


class MainWindow(QMainWindow):

    NextId = 1
    Instances = set() #设置一个set用来显示当前文件序列

    def __init__(self, filename='', parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose) #按下关闭即删除相关窗口代码
        # 其实，关闭一个窗口在这里只是调用了PyQt的deleteLater方法，因此PyQt对象被删除了，但是Instances类集
        # 中的对象（Python引用）还存在，只是现在，其所引用的PyQt对象不存在了。所以需要SIP.unwrapinstance(qobj)判断
        MainWindow.Instances.add(self) #初始化之后首先添加实例到序列中去
        # 因为对Instances进行了引用，所以此窗口对象不会被当作垃圾回收掉，因此需要将destoryed连接到一个更新文件
        # 列表集合的函数上。

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        fileNewAction = self.createAction("&New", self.fileNew,
                QKeySequence.New, "filenew", "Create a text file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing text file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save the text")
        fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save the text using a new filename")
        fileSaveAllAction = self.createAction("Save A&ll",
                self.fileSaveAll, icon="filesave",
                tip="Save all the files")
        fileCloseAction = self.createAction("&Close", self.close,
                QKeySequence.Close, "fileclose",
                "Close this text editor")
                # 关闭此编辑器，而不是整个应用程序，使用closeEvent实现
        fileQuitAction = self.createAction("&Quit", self.fileQuit,
                "Ctrl+Q", "filequit", "Close the application")
                # 关闭整个应用程序所有窗口
        editCopyAction = self.createAction("&Copy", self.editor.copy,
                QKeySequence.Copy, "editcopy",
                "Copy text to the clipboard")
        editCutAction = self.createAction("Cu&t", self.editor.cut,
                QKeySequence.Cut, "editcut",
                "Cut text to the clipboard")
        editPasteAction = self.createAction("&Paste",
                self.editor.paste, QKeySequence.Paste, "editpaste",
                "Paste in the clipboard's text")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, fileSaveAllAction,
                None, fileCloseAction, fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editCopyAction, editCutAction,
                                   editPasteAction))

        self.windowMenu = self.menuBar().addMenu("&Window")
                # self.connect(self.windowMenu, SIGNAL("aboutToShow()"),
                #              self.updateWindowMenu)
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)
        # 显示即更新WindowsMenu，对于所有的子编辑器中的菜单均生效
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActions(editToolbar, (editCopyAction, editCutAction,
                                      editPasteAction))

                # self.connect(self, SIGNAL("destroyed(QObject*)"),
                #              MainWindow.updateInstances)
        self.destroyed.connect(MainWindow.updateInstances)
        # 因为对Instances进行了引用，所以此窗口对象不会被当作垃圾回收掉，因此需要将destoryed连接到一个更新文件
        # 列表集合的函数上。
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.resize(500, 600)

        self.filename = filename #作为参数传递进来，默认空值
        if self.filename=='':
            #要么是程序刚启动，要么是新建了一个新窗口，否则载入历史文件
            self.filename = str("未命名-{0}.txt".format(
                                    MainWindow.NextId))
            MainWindow.NextId += 1 #为什么使用静态方法？？？？
            self.editor.document().setModified(False)
            self.setWindowTitle("文本编辑器(SDI版) - {0}".format(
                                self.filename))
        else:
            self.loadFile()


    @staticmethod
    def updateInstances(qobj):
        MainWindow.Instances = (set([window for window
                in MainWindow.Instances if isAlive(window)]))


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            getattr(action,signal).connect(slot)
            # action.signal.connect(slot)
            # self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def closeEvent(self, event):
        if (self.editor.document().isModified() and
            QMessageBox.question(self,
                "SDI Text Editor - Unsaved Changes",
                "Save unsaved changes in {0}?".format(self.filename),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
            self.fileSave()


    def fileQuit(self):
        QApplication.closeAllWindows()


    def fileNew(self):
        MainWindow().show()
        #show()非模态
        # 调用此方法会新建一个该类的实例，因为此窗口没有父类，因此超出作用域即被回收，但因为其在__init__处
        # 声明了一个添加，因此其窗口对象依存在那个文件列表中，所以保持了文件引用，暂时不会被销毁。


    def fileOpen(self):
        # 如果是打开一个正在编辑的文档，会调出这个文档，否则打开这个新文件（传递给loadFile进行打开操作）
        filename = QFileDialog.getOpenFileName(self,
                "SDI Text Editor -- Open File")
        if not filename[0]=='':
            if (not self.editor.document().isModified() and
                "未命名" in self.filename[0]):
                self.filename[0] = filename[0]
                self.loadFile()
            else:
                MainWindow(filename[0]).show()


    def loadFile(self):
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            self.editor.setPlainText(stream.readAll())
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self,
                    "加载文件",
                    "Failed to load {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        self.editor.document().setModified(False)
        self.setWindowTitle("SDI Text Editor - {0}".format(
                QFileInfo(self.filename).fileName()))


    def fileSave(self):
        if "未命名" in self.filename:
            return self.fileSaveAs()
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.editor.toPlainText()
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self,
                    "保存文件",
                    "Failed to save {0}: {1}".format(self.filename, e))
            return False
        finally:
            if fh is not None:
                fh.close()
        return True


    def fileSaveAs(self):
        filename = QFileDialog.getSaveFileName(self,
                "文本编辑器 - 另存为", self.filename,
                "cm Text files (*.txt *.cmt *)")
        if not filename[0]=='':
            self.filename = filename[0]
            self.setWindowTitle("文本编辑器(SDI) - {0}".format(
                    QFileInfo(self.filename).fileName()))
            return self.fileSave()
        return False


    def fileSaveAll(self):
        count = 0
        for window in MainWindow.Instances:
            if (isAlive(window) and
                window.editor.document().isModified()):
                if window.fileSave():
                    count += 1
        self.statusBar().showMessage("Saved {0} of {1} files".format(
                count, len(MainWindow.Instances)), 5000)


    def updateWindowMenu(self):
        self.windowMenu.clear()
        for window in MainWindow.Instances:
            if isAlive(window):
                self.windowMenu.addAction(window.windowTitle(),
                        self.raiseWindow)


    def raiseWindow(self):
        # 获取信号，获取信号text内容，遍历存货的Instance集合然后进行比较，使用active和raise进行激活和放到前台。
        action = self.sender()
        if not isinstance(action, QAction):
            return
        for window in MainWindow.Instances:
            if (isAlive(window) and
                window.windowTitle() == action.text()):
                window.activateWindow()
                window.raise_()
                break


def isAlive(qobj):
    import sip
    try:
        sip.unwrapinstance(qobj)
    except RuntimeError:
        return False
    return True


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(":/icon.png"))
MainWindow().show()
app.exec_()
