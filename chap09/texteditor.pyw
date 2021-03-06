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

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import textedit
import qrc_resources


__version__ = "1.0.0"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.mdi = QWorkspace()  # QWorkspace[已被QMdiArea代替]::工作空间. todo::http://www.kuqin.com/qtdocument/qworkspace.html#details
        self.setCentralWidget(self.mdi)

        fileNewAction = self.createAction("&New", self.fileNew,
                QKeySequence.New, "filenew", "Create a text file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing text file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save the text")
        fileSaveAsAction = self.createAction("Save &As...",   # 无快捷键
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
        # 下一窗口 动作
        self.windowNextAction = self.createAction("&Next",
                self.mdi.activateNextWindow, QKeySequence.NextChild)
        # 上一窗口 动作
        self.windowPrevAction = self.createAction("&Previous",
                self.mdi.activatePreviousWindow,
                QKeySequence.PreviousChild)
        # 层叠窗口(all)
        self.windowCascadeAction = self.createAction("Casca&de",
                self.mdi.cascade)
        # 平铺窗口(all)
        self.windowTileAction = self.createAction("&Tile",
                self.mdi.tile)
        # 还原窗口(all)
        self.windowRestoreAction = self.createAction("&Restore All",
                self.windowRestoreAll)
        # 最小化窗口(all)
        self.windowMinimizeAction = self.createAction("&Iconize All",
                self.windowMinimizeAll)
        # 排列图标 动作
        self.windowArrangeIconsAction = self.createAction(
                "&Arrange Icons", self.mdi.arrangeIcons)
        # 关闭窗口 动作
        self.windowCloseAction = self.createAction("&Close",
                self.mdi.closeActiveWindow, QKeySequence.Close)

        self.windowMapper = QSignalMapper(self)  # todo::https://blog.csdn.net/noricky/article/details/81240147
                                                 # https://www.cnblogs.com/findumars/p/8035496.html
        self.connect(self.windowMapper, SIGNAL("mapped(QWidget*)"),
                     self.mdi, SLOT("setActiveWindow(QWidget*)"))
        # 文件菜单
        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, fileSaveAllAction,
                None, fileQuitAction))
        # 编辑菜单
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editCopyAction, editCutAction,
                                   editPasteAction))
        # 窗口菜单
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.connect(self.windowMenu, SIGNAL("aboutToShow()"),
                     self.updateWindowMenu)
        # 文件工具条
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAction))
        # 编缉工具条
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActions(editToolbar, (editCopyAction, editCutAction,
                                      editPasteAction))
        # 创建配置文件
        settings = QSettings()
        # 恢复几何图形
        self.restoreGeometry(settings.value("MainWindow/Geometry",
                QByteArray()))
        # 恢复状态
        self.restoreState(settings.value("MainWindow/State",
                QByteArray()))

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.updateWindowMenu()
        self.setWindowTitle("Text Editor")
        QTimer.singleShot(0, self.loadFiles)  # 单singleShot，表示它只会触发一次，发出一次信号，然后来执行槽函数。
                                              # todo::https://blog.csdn.net/fanyun_01/article/details/73162626


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
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
        for textEdit in self.mdi.windowList():
            if textEdit.isModified():
                try:
                    textEdit.save()
                except IOError as e:
                    failures.append(e)
        if (failures and
            QMessageBox.warning(self, "Text Editor -- Save Error",
                    "Failed to save{}\nQuit anyway?".format(
                    "\n\t".join(failures)),
                    QMessageBox.Yes|QMessageBox.No) ==
                    QMessageBox.No):
            event.ignore()
            return
        # 创建配置文件,记录配置.
        settings = QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())  # 保存几何
        settings.setValue("MainWindow/State", self.saveState())  # 保存状态
        files = []
        for textEdit in self.mdi.windowList():
            if not textEdit.filename.startswith("Unnamed"):
                files.append(textEdit.filename)
        settings.setValue("CurrentFiles", files)  # 保存最近打开文件.
        self.mdi.closeAllWindows()


    def loadFiles(self):
        if len(sys.argv) > 1:
            for filename in sys.argv[1:31]: # Load at most 30 files(最大预载入30个文件.)
                if QFileInfo(filename).isFile():
                    self.loadFile(filename)
                    QApplication.processEvents()  # todo::https://www.cnblogs.com/findumars/p/5607683.html
        else:
            settings = QSettings()
            files = settings.value("CurrentFiles") or []
            for filename in files:
                if QFile.exists(filename):
                    self.loadFile(filename)
                    QApplication.processEvents()  # processEvents()函数的作用是当程序处理耗时事件时(如文件保存/载入),把使用权返回给调用者.避免出现假死的情况.


    def fileNew(self):
        textEdit = textedit.TextEdit()
        self.mdi.addWindow(textEdit)
        textEdit.show()


    def fileOpen(self):
        filename = QFileDialog.getOpenFileName(self,
                "Text Editor -- Open File")
        if filename:
            for textEdit in self.mdi.windowList():
                if textEdit.filename == filename:
                    self.mdi.setActiveWindow(textEdit)
                    break
            else:
                self.loadFile(filename)


    def loadFile(self, filename):
        textEdit = textedit.TextEdit(filename)
        try:
            textEdit.load()
        except EnvironmentError as e:
            QMessageBox.warning(self, "Text Editor -- Load Error",
                    "Failed to load {}: {}".format(filename, e))
            textEdit.close()
            del textEdit
        else:
            self.mdi.addWindow(textEdit)
            textEdit.show()


    def fileSave(self):
        textEdit = self.mdi.activeWindow()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return True
        try:
            textEdit.save()
            return True
        except EnvironmentError as e:
            QMessageBox.warning(self, "Text Editor -- Save Error",
                    "Failed to save {}: {}".format(textEdit.filename, e))
            return False


    def fileSaveAs(self):
        textEdit = self.mdi.activeWindow()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        filename = QFileDialog.getSaveFileName(self,
                        "Text Editor -- Save File As",
                        textEdit.filename, "Text files (*.txt *.*)")
        if filename:
            textEdit.filename = filename
            return self.fileSave()
        return True


    def fileSaveAll(self):
        errors = []
        for textEdit in self.mdi.windowList():
            if textEdit.isModified():
                try:
                    textEdit.save()
                except EnvironmentError as e:
                    errors.append("{}: {}".format(textEdit.filename, e))
        if errors:
            QMessageBox.warning(self,
                    "Text Editor -- Save All Error",
                    "Failed to save\n{}".format("\n".join(errors)))

    # 复制
    def editCopy(self):
        textEdit = self.mdi.activeWindow()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    # 剪切
    def editCut(self):
        textEdit = self.mdi.activeWindow()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            cursor.removeSelectedText()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    # 粘贴
    def editPaste(self):
        textEdit = self.mdi.activeWindow()
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        clipboard = QApplication.clipboard()
        textEdit.insertPlainText(clipboard.text())

    # 还原窗口(all)
    def windowRestoreAll(self):
        for textEdit in self.mdi.windowList():
            textEdit.showNormal()

    # 最小化窗口(all)
    def windowMinimizeAll(self):
        for textEdit in self.mdi.windowList():
            textEdit.showMinimized()

    # 更新窗口菜单
    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.addActions(self.windowMenu, (self.windowNextAction,
                self.windowPrevAction, self.windowCascadeAction,
                self.windowTileAction, self.windowRestoreAction,
                self.windowMinimizeAction,
                self.windowArrangeIconsAction, None,
                self.windowCloseAction))
        textEdits = self.mdi.windowList()
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
                accel = "&{} ".format(i)
            elif i < 36:
                accel = "&{} ".format(chr(i + ord("@") - 9))
            action = menu.addAction("{}{}".format(accel, title))
            self.connect(action, SIGNAL("triggered()"),
                         self.windowMapper, SLOT("map()"))  # 81ROW
            self.windowMapper.setMapping(action, textEdit)  # TODO::http://blog.sina.com.cn/s/blog_a3eacdb20101ddcf.html
            i += 1


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(":/icon.png"))
app.setOrganizationName("Qtrac Ltd.")
app.setOrganizationDomain("qtrac.eu")
app.setApplicationName("Text Editor")
form = MainWindow()
form.show()
app.exec_()

