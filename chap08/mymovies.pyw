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
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import addeditmoviedlg
import moviedata
import qrc_resources


__version__ = "1.0.0"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.movies = moviedata.MovieContainer()
        self.table = QTableWidget()
        self.setCentralWidget(self.table)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        fileNewAction = self.createAction("&New...", self.fileNew,
                QKeySequence.New, "filenew",
                "Create a movie data file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing  movie data file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save the movie data")
        fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save the movie data using a new name")
        fileImportDOMAction = self.createAction(
                "&Import from XML (DOM)...", self.fileImportDOM,
                tip="Import the movie data from an XML file")
        fileImportSAXAction = self.createAction(
                "I&mport from XML (SAX)...", self.fileImportSAX,
                tip="Import the movie data from an XML file")
        fileExportXmlAction = self.createAction(
                "E&xport as XML...", self.fileExportXml,
                tip="Export the movie data to an XML file")
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
        editAddAction = self.createAction("&Add...", self.editAdd,
                "Ctrl+A", "editadd", "Add data about a movie")
        editEditAction = self.createAction("&Edit...", self.editEdit,
                "Ctrl+E", "editedit", "Edit the current movie's data")
        editRemoveAction = self.createAction("&Remove...",
                self.editRemove, "Del", "editdelete",
                "Remove a movie's data")
        helpAboutAction = self.createAction("&About", self.helpAbout,
                tip="About the application")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, None,
                fileImportDOMAction, fileImportSAXAction,
                fileExportXmlAction, None, fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editAddAction, editEditAction,
                editRemoveAction))
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction,))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAsAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editAddAction, editEditAction,
                                      editRemoveAction))

        self.connect(self.table,
                SIGNAL("itemDoubleClicked(QTableWidgetItem*)"),
                self.editEdit)
        # 设置快捷键 todo::http://chenye.science/coding-dairy-20170726.html
        QShortcut(QKeySequence("Return"), self.table, self.editEdit)  # (快捷键, 应用的控件, 执行的函数)
        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry",
                QByteArray()))
        self.restoreState(settings.value("MainWindow/State",
                QByteArray()))
        
        self.setWindowTitle("My Movies")
        QTimer.singleShot(0, self.loadInitialFile)  # 零时单触发


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
        if self.okToContinue():
            settings = QSettings()
            settings.setValue("LastFile", self.movies.filename())
            settings.setValue("MainWindow/Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
        else:
            event.ignore()


    def okToContinue(self):
        if self.movies.isDirty():
            reply = QMessageBox.question(self,
                    "My Movies - Unsaved Changes",
                    "Save unsaved changes?",
                    QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True


    def loadInitialFile(self):
        settings = QSettings()
        fname = settings.value("LastFile")
        if fname and QFile.exists(fname):
            ok, msg = self.movies.load(fname)
            self.statusBar().showMessage(msg, 5000)
        self.updateTable()


    def updateTable(self, current=None):
        self.table.clear()  # 清空
        self.table.setRowCount(len(self.movies))  # 设置行数
        self.table.setColumnCount(5)    # 设置列数
        self.table.setHorizontalHeaderLabels(["Title", "Year", "Mins",  # 设置水平表头标签
                "Acquired", "Notes"])
        self.table.setAlternatingRowColors(True)    # 设置交替行颜色
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # 设置Table 编辑触发条件:不触发
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # 设置选择行为：选择行
        self.table.setSelectionMode(QTableWidget.SingleSelection)  # 设置选择方式：单选
        selected = None
        for row, movie in enumerate(self.movies):
            item = QTableWidgetItem(movie.title)
            if current is not None and current == id(movie):  # 获取电影对象ID号（内存句柄号）
                selected = item
            item.setData(Qt.UserRole, int(id(movie)))  # todo::设置用户角色数据== int(id(movie))
            self.table.setItem(row, 0, item)  # 设置项(行, 列, item对象)
            year = movie.year
            if year != movie.UNKNOWNYEAR:
                item = QTableWidgetItem("{}".format(year))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 1, item)
            minutes = movie.minutes
            if minutes != movie.UNKNOWNMINUTES:
                item = QTableWidgetItem("{}".format(minutes))
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                self.table.setItem(row, 2, item)
            item = QTableWidgetItem(movie.acquired.toString(
                                    moviedata.DATEFORMAT))
            item.setTextAlignment(Qt.AlignRight|
                                  Qt.AlignVCenter)
            self.table.setItem(row, 3, item)
            notes = movie.notes
            if len(notes) > 40:
                notes = notes[:39] + "..."
            self.table.setItem(row, 4, QTableWidgetItem(notes))
        self.table.resizeColumnsToContents()  # 调整列宽适配内容
        if selected is not None:
            selected.setSelected(True)  # 设置为可选中
            self.table.setCurrentItem(selected)  # 设置_当前项为
            self.table.scrollToItem(selected)  # 滚动_到_项(selected)
        

    def fileNew(self):
        if not self.okToContinue():
            return
        self.movies.clear()
        self.statusBar().clearMessage()
        self.updateTable()


    def fileOpen(self):
        if not self.okToContinue():
            return
        path = (QFileInfo(self.movies.filename()).path()
                if self.movies.filename() else ".")
        fname = QFileDialog.getOpenFileName(self,
                "My Movies - Load Movie Data", path,
                "My Movies data files ({})".format(self.movies.formats()))
        if fname:
            ok, msg = self.movies.load(fname)
            self.statusBar().showMessage(msg, 5000)
            self.updateTable()


    def fileSave(self):
        if not self.movies.filename():
            return self.fileSaveAs()
        else:
            ok, msg = self.movies.save()
            self.statusBar().showMessage(msg, 5000)
            return ok


    def fileSaveAs(self):
        fname = self.movies.filename() if self.movies.filename() else "."
        fname = QFileDialog.getSaveFileName(self,
                "My Movies - Save Movie Data", fname,
                "My Movies data files ({})".format(self.movies.formats()))
        if fname:
            if "." not in fname:
                fname += ".mqb"
            ok, msg = self.movies.save(fname)
            self.statusBar().showMessage(msg, 5000)
            return ok
        return False


    def fileImportDOM(self):
        self.fileImport("dom")


    def fileImportSAX(self):
        self.fileImport("sax")


    def fileImport(self, format):
        if not self.okToContinue():
            return
        path = (QFileInfo(self.movies.filename()).path()
                if self.movies.filename() else ".")
        fname = QFileDialog.getOpenFileName(self,
                "My Movies - Import Movie Data", path,
                "My Movies XML files (*.xml)")
        if fname:
            if format == "dom":
                ok, msg = self.movies.importDOM(fname)
            else:
                ok, msg = self.movies.importSAX(fname)
            self.statusBar().showMessage(msg, 5000)
            self.updateTable()


    def fileExportXml(self):
        fname = self.movies.filename()
        if not fname:
            fname = "."
        else:
            i = fname.rfind(".")
            if i > 0:
                fname = fname[:i]

            fname += ".xml"
        fname = QFileDialog.getSaveFileName(self,
                "My Movies - Export Movie Data", fname,
                "My Movies XML files (*.xml)")
        if fname:
            if "." not in fname:
                fname += ".xml"
            ok, msg = self.movies.exportXml(fname)
            self.statusBar().showMessage(msg, 5000)


    def editAdd(self):
        form = addeditmoviedlg.AddEditMovieDlg(self.movies, None,
                                               self)
        if form.exec_():
            self.updateTable(id(form.movie))


    def editEdit(self):
        movie = self.currentMovie()
        if movie is not None:
            form = addeditmoviedlg.AddEditMovieDlg(self.movies,
                                                   movie, self)
            if form.exec_():
                self.updateTable(id(movie))


    def editRemove(self):
        movie = self.currentMovie()
        if movie is not None:
            year = (" {}".format(movie.year)
                    if movie.year != movie.UNKNOWNYEAR else "")
            if (QMessageBox.question(self,
                    "My Movies - Delete Movie",
                    "Delete Movie `{}' {}?".format(
                    movie.title, year),
                    QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
                self.movies.delete(movie)
                self.updateTable()


    def currentMovie(self):
        row = self.table.currentRow()
        if row > -1:
            item = self.table.item(row, 0)
            id = int(item.data(Qt.UserRole))  # 读取用户角色数据 todo:: row175
            return self.movies.movieFromId(id)
        return None


    def helpAbout(self):
        QMessageBox.about(self, "My Movies - About",
                """<b>My Movies</b> v {0}
                <p>Copyright &copy; 2008-10 Qtrac Ltd. 
                All rights reserved.
                <p>This application can be used to view some basic
                information about movies and to load and save the 
                movie data in a variety of custom file formats.
                <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system()))


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")  # 设置环境变量,为使用QSettings()作准备.
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("My Movies")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()

