#!/usr/bin/env python3

import sys

from PyQt4.QtGui import QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import textedit
import qrc_resources
import traceback


__version__ = "0.0.1"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.mdi = QMdiArea() #声明一个工作区,Qt5使用maiarea代替workspace，可以通过设置scrollbarsenabled来使其拥有比窗口更大的工作空间
        # 通过背景刷可以设置背景颜色
        self.setCentralWidget(self.mdi)

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
                self.fileSaveAll, "filesave",
                tip="Save all the files")
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
        editCopyAction = self.createAction("&Copy", self.editCopy,
                QKeySequence.Copy, "editcopy",
                "Copy text to the clipboard")
        editCutAction = self.createAction("Cu&t", self.editCut,
                QKeySequence.Cut, "editcut",
                "Cut text to the clipboard")
        editPasteAction = self.createAction("&Paste", self.editPaste,
                QKeySequence.Paste, "editpaste",
                "Paste in the clipboard's text")
        editShowAction = self.createAction("&ShowBug", self.showbug,
                 "Showbug",
                "Show the fucking bugs")


        self.windowNextAction = self.createAction("&Next",
                self.mdi.activateNextSubWindow, QKeySequence.NextChild) #activeNextWindows函数已废弃
        self.windowPrevAction = self.createAction("&Previous",
                self.mdi.activatePreviousSubWindow,
                QKeySequence.PreviousChild)
        self.windowCascadeAction = self.createAction("Casca&de",
                self.mdi.cascadeSubWindows)
        self.windowTileAction = self.createAction("&Tile",
                self.mdi.tileSubWindows)
        self.windowRestoreAction = self.createAction("&Restore All",
                self.windowRestoreAll)
        self.windowMinimizeAction = self.createAction("&Iconize All",
                self.windowMinimizeAll)
        # self.windowArrangeIconsAction = self.createAction(
        #         "&Arrange Icons", self.mdi.arrangeIcons)
        self.windowCloseAction = self.createAction("&Close",
                self.mdi.closeActiveSubWindow, QKeySequence.Close)

        self.windowMapper = QSignalMapper(self)  # todo::https://blog.csdn.net/noricky/article/details/81240147
                                                 # https://www.cnblogs.com/findumars/p/8035496.html
        # self.connect(self.windowMapper, SIGNAL("mapped(QWidget*)"),
        #              self.mdi, SLOT("setActiveWindow(QWidget*)"))
        self.windowMapper.mapped.connect(self.mdi.setActiveSubWindow)

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, fileSaveAllAction,
                None, fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editCopyAction, editCutAction,
                                   editPasteAction,editShowAction))
        self.windowMenu = self.menuBar().addMenu("&Window")
        # self.connect(self.windowMenu, SIGNAL("aboutToShow()"),
        #              self.updateWindowMenu)
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActions(editToolbar, (editCopyAction, editCutAction,
                                      editPasteAction,editShowAction))

        settings = QSettings()
        re_geo=settings.value("MainWindow/Geometry")
        if re_geo != None:
            self.restoreGeometry(QByteArray(re_geo))

        re_state=settings.value("MainWindow/State")
        if re_state != None:
            self.restoreState(QByteArray(re_state))

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.updateWindowMenu()
        self.setWindowTitle("Text Editor")
        QTimer.singleShot(0, self.loadFiles)
        # 开始的时候加载了一些文件，如果有的话。那么，用户希望这时候使用快捷键导航，但是这时候他没有出发abouttoshow
        # 所以，菜单不会更新，updatewindowsmenu没有起作用，所以就不能导航，因此在打开程序的时候使用计时器来搞定这些



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
        failures = []
        #遍历所有的文件并且进行保存
        for textEdit in self.mdi.subWindowList():
            if textEdit.widget().isModified():
                try:
                    textEdit.widget().save()
                except IOError as e:
                    failures.append(str(e))
        if (failures and
            QMessageBox.warning(self, "Text Editor -- Save Error",
                    "Failed to save{0}\nQuit anyway?".format(
                    "\n\t".join(failures)),
                    QMessageBox.Yes|QMessageBox.No) ==
                    QMessageBox.No):
            event.ignore()
            return
        settings = QSettings()
        settings.setValue("MainWindow/Geometry",
                          QVariant(self.saveGeometry()))
        settings.setValue("MainWindow/State",
                          QVariant(self.saveState()))
        files = []
        for textEdit in self.mdi.subWindowList():
            if not "Unnamed" in textEdit.widget().filename:
                files.append(textEdit.widget().filename)
        settings.setValue("CurrentFiles", QVariant(files))
        self.mdi.closeAllSubWindows()


    def loadFiles(self):
        try:
            if len(sys.argv) > 1:
                for filename in sys.argv[1:31]:  # Load at most 30 files
                    filename = str(filename)
                    if QFileInfo(filename).isFile():
                        self.loadFile(filename)
                        QApplication.processEvents()
                        # 暂时将控制权返还给事件循环，以便其可以得到处理，然后从下一个语句开始恢复处理进程。
                        # 让应用程序保持相应，这时候鼠标和键盘事件会获取一些处理器时间，即便同时有大良进程
                        # 程序依旧可以相应用户操作
            else:
                settings = QSettings()
                cfiles=settings.value("CurrentFiles")
                if cfiles != None:
                    files = list(settings.value("CurrentFiles"))
                else:
                    files=[]
                for filename in files:
                    filename = str(filename)
                    if QFile.exists(filename):
                        self.loadFile(filename)
                        QApplication.processEvents()
        except:
            err=traceback.format_exc()
            QMessageBox.warning(self,"WARN",err)


    def fileNew(self):
        # 新建一个实例，传递给mdi，然后show调用即可
        textEdit = textedit.TextEdit()
        self.mdi.addSubWindow(textEdit)
        textEdit.show()


    def fileOpen(self):
        # 获取文件名和地址，如果存在，则激活窗口，并且退出循环，否则传递给loadfile打开
        try:
            filename = QFileDialog.getOpenFileName(self,
                    "Text Editor -- Open File")
            # print(filename)
            if not filename[0]=='':
                for textEdit in self.mdi.subWindowList():
                    # print(textEdit.widget())
                    # if textEdit.filename == filename[0]:
                    if textEdit.widget().filename == filename[0]:
                        self.mdi.setActiveSubWindow(textEdit)
                        break
                else:
                    self.loadFile(filename[0])
        except:
            QMessageBox.warning(self,"WARN",traceback.format_exc())


    def loadFile(self, filename):
        try:
            textEdit = textedit.TextEdit(filename)
            try:
                textEdit.load()
            except EnvironmentError as e:
                QMessageBox.warning(self, "Text Editor -- Load Error",
                        "Failed to load {0}: {1}".format(filename, e))
                textEdit.close()
                del textEdit
            else:
                self.mdi.addSubWindow(textEdit)
                textEdit.show()
        except:
            QMessageBox.warning(self,"WARN",traceback.format_exc())


    def fileSave(self):
        try:
            # textEdit = self.mdi.activeSubWindow()
            # if textEdit.widget() is None:
            #     return True
            # try:
            #     textEdit.save()
            #     return True
            # except EnvironmentError as e:
            #     QMessageBox.warning(self, "Text Editor -- Save Error",
            #             "Failed to save {0}: {1}".format(textEdit.widget().filename, e))
            #     return False
            textEdit = self.mdi.currentSubWindow()
            # i.e., if a widget outside the MDI area is the active window, no subwindow will be active.
            # 不使用activeSubWindow()的原因
            QMessageBox.warning(self,"WARN(SAVE)","当前窗口：%s\n当前窗口部件：%s\n激活窗口：%s"%(str(textEdit),str(textEdit.widget()),str(self.mdi.activeSubWindow())))
            textEdit=textEdit.widget()

            if textEdit is None or not isinstance(textEdit, QTextEdit):
                return True
            try:
                textEdit.save()
                return True
            except EnvironmentError as e:
                QMessageBox.warning(self, "Text Editor -- Save Error",
                        "Failed to save {0}: {1}".format(textEdit.filename, e))
                return False
        except:
            QMessageBox.warning(self,"WARN",traceback.format_exc())


    def fileSaveAs(self):
        try:
            # textEdit = self.mdi.activeSubWindow()
            # if textEdit.widget() is None:
            #     return
            # filename = QFileDialog.getSaveFileName(self,
            #                 "Text Editor -- Save File As",
            #                 textEdit.widget().filename, "Text files (*.txt *.*)")
            # if not filename[0]=='':
            #     textEdit.widget().filename = filename[0]
            #     return self.fileSave()
            # return True
            textEdit = self.mdi.currentSubWindow()
            QMessageBox.warning(self,"WARN(SAVE)","当前窗口：%s\n当前窗口部件：%s\n激活窗口：%s"%(str(textEdit),str(textEdit.widget()),str(self.mdi.activeSubWindow())))
            textEdit=textEdit.widget()

            if textEdit is None or not isinstance(textEdit, QTextEdit):
                return
            filename,filetype = QFileDialog.getSaveFileName(self,
                            "Text Editor -- Save File As",
                            textEdit.filename, "Text files (*.txt *.*)")
            if filename:
                textEdit.filename = filename
                return self.fileSave()
            return True
        except:
            QMessageBox.warning(self,"WARN",traceback.format_exc())


    def fileSaveAll(self):
        errors = []
        for textEdit in self.mdi.subWindowList():
            textEdit=textEdit.widget()
            if textEdit.isModified():
                try:
                    textEdit.save()
                except EnvironmentError as e:
                    errors.append("{0}: {1}".format(textEdit.filename, e))
        if errors:
            QMessageBox.warning(self,
                    "Text Editor -- Save All Error",
                    "Failed to save\n{0}".format("\n".join(errors)))


    def editCopy(self):
        textEdit = self.mdi.activeSubWindow()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if not text.isEmpty():
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    def showbug(self):
        try:
            a=self.mdi.currentSubWindow()
            QMessageBox.warning(self,"WARN",str(a))
        except:
            QMessageBox.warning(self,"WARN",traceback.format_exc())

    def editCut(self):
        textEdit = self.mdi.activeSubWindow()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if not text.isEmpty():
            cursor.removeSelectedText()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)


    def editPaste(self):
        textEdit = self.mdi.activeSubWindow()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        clipboard = QApplication.clipboard()
        textEdit.insertPlainText(clipboard.text())


    def windowRestoreAll(self):
        for textEdit in self.mdi.subWindowList():
            textEdit.showNormal()


    def windowMinimizeAll(self):
        for textEdit in self.mdi.subWindowList():
            textEdit.showMinimized()


    def updateWindowMenu(self):
        self.windowMenu.clear()
        # self.addActions(self.windowMenu, (self.windowNextAction,
        #         self.windowPrevAction, self.windowCascadeAction,
        #         self.windowTileAction, self.windowRestoreAction,
        #         self.windowMinimizeAction,
        #         self.windowArrangeIconsAction, None,
        #         self.windowCloseAction))
        self.addActions(self.windowMenu, (self.windowNextAction,
        self.windowPrevAction, self.windowCascadeAction,
        self.windowTileAction, self.windowRestoreAction,
        self.windowMinimizeAction, None,
        self.windowCloseAction))
        textEdits = self.mdi.subWindowList()
        if not textEdits:
            return
        self.windowMenu.addSeparator()
        i = 1
        menu = self.windowMenu
        for textEdit in textEdits:
            title = textEdit.windowTitle()
            if i == 10:
                self.windowMenu.addSeparator()
                menu = menu.addMenu("&More")
            accel = ""
            if i < 10:
                accel = "&{0} ".format(i)
            elif i < 36:
                accel = "&{0} ".format(chr(i + ord("@") - 9))
            action = menu.addAction("{0}{1}".format(accel, title))
            # self.connect(action, SIGNAL("triggered()"),
            #              self.windowMapper, SLOT("map()"))
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, textEdit)
            i += 1


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(":/icon.png"))
app.setOrganizationName("Marvin Studio")
app.setOrganizationDomain("http://www.marvinstudio.cn")
app.setApplicationName("文本编辑器")
form = MainWindow()
form.show()
app.exec_()

