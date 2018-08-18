#!/usr/bin/env python3
import sys,os,platform
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import moviedata
import qrc_resources
import traceback
import cmaddeditmoviedlg

__version__="0.0.2"

class MainWindow(QMainWindow):
    
    def __init__(self,parent=None):
        
        super(MainWindow,self).__init__(parent)
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

        self.table.itemDoubleClicked.connect(self.editEdit)
        QShortcut(QKeySequence("Return"),self.table,self.editEdit)

        settings = QSettings()

        setting_geo=settings.value("MainWindow/Geometry")
        setting_state=settings.value("MainWindow/State")
        if setting_geo is not None:
            self.restoreGeometry(setting_geo)
        if setting_state is not None:
            self.restoreState(setting_state)

        self.setWindowTitle("My Movies")
        QTimer.singleShot(0,self.loadInitialFile)

        self.setMinimumSize(1000,600)

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
            # self.connect(action, SIGNAL(signal), slot)
            getattr(action,signal).connect(slot)
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
            settings.setValue("LastFile",
                              QVariant(self.movies.filename()))
            settings.setValue("MainWindow/Geometry",
                              QVariant(self.saveGeometry()))
            settings.setValue("MainWindow/State",
                              QVariant(self.saveState()))
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

    def updateTable(self,current=None):
        self.table.clear()
        self.table.setRowCount(len(self.movies))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Title","Year","Mins","Acquired","Locations","Notes"])
        self.table.setColumnWidth(0,300)
        self.table.setColumnWidth(4,190)
        self.table.setAlternatingRowColors(True)
        #设置不允许用户随意编辑 选择后选择Row 选择的模式为传递信号
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        selected=None
        for row,movie in enumerate(self.movies):
            item=QTableWidgetItem(movie.title)
            if current is not None and current == id(movie):
                selected = item
            item.setData(Qt.UserRole,QVariant(int(id(movie))))
            self.table.setItem(row,0,item)
            year=movie.year
            if year != movie.UNKNOWNYEAR:
                item = QTableWidgetItem("%s"%year)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row,1,item)
            minutes = movie.minutes
            if minutes != movie.UNKNOWNMINUTES:
                item = QTableWidgetItem("%s"%minutes)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row,2,item)
            item = QTableWidgetItem(movie.acquired.toString(moviedata.DATEFORMAT))
            #?????????????????????????????????????????????????????????????????????
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.table.setItem(row,3,item)

            locations=movie.locations
            if locations == None or locations == " " or locations == "":
                locations = "未知(显示驱动)"
            elif len(locations) > 17:
                locations = locations[:17] +"..."
            item=QTableWidgetItem(str(locations))
            self.table.setItem(row,4,item)

            notes = movie.notes
            if notes ==None:
                notes="未知(显示驱动)"
            elif len(notes) >40:
                notes = notes[:40]+"..."
            # self.table.resizeColumnsToContents()
            item = QTableWidgetItem(notes)
            self.table.setItem(row,5,item)

            if selected is not None:
                selected.setSelected(True)
                self.table.setCurrentItem(selected)
                self.table.scrollToItem(selected)

        self.table.setColumnWidth(0,300)
        self.table.setColumnWidth(1,50)
        self.table.setColumnWidth(2,50)
        self.table.setColumnWidth(3,190)
        self.table.setColumnWidth(4,190)
        self.table.setColumnWidth(5,190)

    def fileNew(self):
        try:
            if not self.okToContinue():
                return
            self.movies.clear()
            self.statusBar().clearMessage()
            self.updateTable()
        except:
            self.showbug()

    def fileOpen(self):
        if not self.okToContinue():
            return
        path = (QFileInfo(self.movies.filename()).path() if not self.movies.filename()=='' else ".")
        fname = QFileDialog.getOpenFileName(self,"My Movies - Load Movie Data",path,"cmMOVIE-Support data type %s"%self.movies.formats())
        if not fname==('',''):
            ok,msg = self.movies.load(fname[0])
            self.statusBar().showMessage(msg,30000)
            self.updateTable()


    def fileSave(self):
        if self.movies.filename()=='':
            return self.fileSaveAs()
        else:
            ok,msg=self.movies.save()
            self.statusBar().showMessage(msg,30000)
            return ok

    def fileSaveAs(self):
        fname = (self.movies.filename() if not self.movies.filename()=='' else ".")
        fname = QFileDialog.getSaveFileName (self,"My Movies - Save Movie Data",fname[0],
                                            "cmMOVIE-Support file type %s"%self.movies.formats())
        # print("_____>",fname)
        if not fname==('',''):
            if not "." in fname[0]:
                fname[0] += ".mqb"
            ok ,msg =self.movies.save(fname[0])
            self.statusBar().showMessage(msg,30000)
            return ok
        return False

    def fileImportDOM(self):
        self.fileImport("dom")

    def fileImportSAX(self):
        self.fileImport("sax")

    def fileImport(self,format):
        try:
            if not self.okToContinue():
                return
            path = (QFileInfo(self.movies.filename()).path() if not self.movies.filename()=='' else ".")
            fname = QFileDialog.getOpenFileName(self,"My Movie - Import Movie Data",path,
                                                "My Movies XML files(*.xml)")
            if not fname[0]=='':
                if format =='dom':
                    # print(fname[0])
                    ok,msg=self.movies.importDOM(fname[0])
                else:
                    ok,msg=self.movies.importSAX(fname[0])
                self.statusBar().showMessage(msg,30000)
                self.updateTable()
        except:
            self.showbug()


    def fileExportXml(self):
        try:
            fname = self.movies.filename()
            xmls=('.mqb','.mqt','.mpb','.mpt')
            if fname =='':
                fname="."
            elif fname[-4:] in xmls:
                fname = fname[:-4] + ".xml"
            fname = QFileDialog.getSaveFileName(self,
                                                "My Movies - Export Movie Data",fname,
                                                "My Movies XML files(*.xml)"
                                                )
            if not fname[0] == "":
                if not "." in fname[0]:
                    fname[0] += ".xml"
                ok ,msg =self.movies.exportXml(fname[0])
                self.statusBar().showMessage('导出成功',30000)
        except:
            self.showbug()
            
            

    def editAdd(self):
        form = cmaddeditmoviedlg.AddEditMovieDlg(self.movies,None,self)
        if form.exec_():
            self.updateTable(id(form.movie))
    
    def editEdit(self):
        try:
            movie = self.currentMovie()
            # print(movie)
            if movie is not None: 
                form = cmaddeditmoviedlg.AddEditMovieDlg(self.movies,movie,self)
                if form.exec_():
                    self.updateTable(id(movie))
        except:
            self.showbug()

    def editRemove(self):
        movie = self.currentMovie()
        if movie is not None:
            year = (movie.year if movie.year != movie.UNKNOWNYEAR else "")
            if QMessageBox.question(self,"My Movies -Delete Movie","删除电影条目：%s, %s"%(movie.title,year),
                                    QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
                self.movies.delete(movie)
                self.updateTable()
                                        

    def currentMovie(self):
        try:
            row = self.table.currentRow()
            if row > -1:
                item = self.table.item(row,0)
                id = item.data(Qt.UserRole)
                return self.movies.movieFromId(id)
            return None
        except:
            self.showbug()

    def helpAbout(self):
        QMessageBox.about(self,"My Movies - About",
                        """<b>My Movies</b> v%s
                        <p>Copyright &copy; 2017 Marvin Studio
                        All Right Reserved.
                        <p>此程序是我在学习Qt和Python数据导入和导出（其中包括字节和XML，以及二进制数据）以及
                        完整的一个module来实现数据的组成、结构化、排序和相关导入导出、写入、更新、删除函数的设计
                        的过程中写的一个Demo。
                        <p>Python %s - Qt %s - PyQt %s"""%(__version__,platform.python_version(),QT_VERSION_STR,PYQT_VERSION_STR)
                        )

    def showbug(self):
        _err=traceback.format_exc()
        QMessageBox.warning(self,"WARNING","出现错误\n%s"%_err)

def main():
    app=QApplication(sys.argv)
    app.setOrganizationName("Marvin Studio")
    app.setOrganizationDomain("http://www.marvinstudio.cn")
    app.setApplicationName("My Movies")
    app.setWindowIcon(QIcon(":/icon.png"))
    form=MainWindow()
    form.show()
    app.exec_()

main()            

