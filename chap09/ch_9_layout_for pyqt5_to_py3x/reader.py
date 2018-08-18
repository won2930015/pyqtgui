import PyQt5,sys,traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
'''


'''
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.groupList=QListWidget()
        self.messageList=QListWidget()
        self.messageView=QTextBrowser()
        self.messageSplitter=QSplitter(Qt.Vertical)
        self.messageSplitter.addWidget(self.messageList)
        self.messageSplitter.addWidget(self.messageView)
        self.mainSpitter=QSplitter(Qt.Horizontal)
        self.mainSpitter.addWidget(self.groupList)
        self.mainSpitter.addWidget(self.messageSplitter)
        self.setCentralWidget(self.mainSpitter)

        self.mainSpitter.setStretchFactor(0,1)
        self.mainSpitter.setStretchFactor(1,3)
        self.messageSplitter.setStretchFactor(0,1)
        self.messageSplitter.setStretchFactor(1,2)

        settings=QSettings()
        size=settings.value("MainWindow/Size",QVariant(QSize(600,500)))
        self.resize(size)
        position=settings.value("MainWindow/Position",QVariant(QPoint(0,0)))
        self.move(position)
        
        re_geo=settings.value("MainWindow/Geometry")
        re_state=settings.value("MainWindow/State")
        if re_geo != None:
            self.restoreGeometry(QByteArray(re_geo))
        if re_state != None:
            self.restoreState(QByteArray(re_state))

        re_messsp=settings.value("Spliter/MessageSplitter")
        re_mainsp=settings.value("Spliter/MainSplitter")
        # re_state=settings.value("MainWindow/State")
        # if re_state != None:
        #     self.restoreState(re_state)
        if re_messsp != None:
            self.messageSplitter.restoreState(QByteArray(re_messsp))
        if re_mainsp != None:
            self.mainSpitter.restoreState(QByteArray(re_mainsp))

        # self.restoreGeometry(
        #         settings.value("MainWindow/Geometry").toByteArray())
        # self.restoreState(
        #         settings.value("MainWindow/State").toByteArray())



    def closeEvent(self,event):
        QMessageBox.warning(self,"WARN","TEST")
        settings=QSettings()
        # settings.setValue("MainWindow/Size",QVariant(self.size()))
        # settings.setValue("MainWindow/Position",QVariant(self.pos()))
        settings.setValue("MainWindow/Geometry",
                              QVariant(self.saveGeometry()))
        settings.setValue("MainWindow/State",
                              QVariant(self.saveState()))
        settings.setValue("Spliter/MessageSplitter",QVariant(self.messageSplitter.saveState()))
        settings.setValue("Spliter/MainSplitter",QVariant(self.mainSpitter.saveState()))






if __name__=="__main__":
    app=QApplication(sys.argv)
    app.setOrganizationName("Marvin Studio")
    app.setOrganizationDomain("http://www.marvinstudio.cn")
    app.setApplicationName("cmReader Simple")
    form=MainWindow()
    form.show()
    app.exec_()