#!/usr/bin/env python3
'''
这是Image Changer的主程序窗口
根据原始的Py2和PyQt4代码改写而成，适用于Py3和PyQt5，除了PyQt不需要安装别的第三方包
'''
try:
    import os,platform,sys,traceback
    import PyQt5
    from tkinter import Tk
    from tkinter.messagebox import showwarning
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtPrintSupport import *
    import qrc_resources
    import newimagedlg
    import helpform
    import resizedlg
except Exception as _err:
    Tk().withdraw()
    warn=showwarning("WARNING","WARNING Info:\n%s"%_err)

__version__="0.0.1"

class MainWindow(QMainWindow):

    def __init__(self,parent=None):
            super(MainWindow,self).__init__(parent)
            self.image=QImage() #不是QMainWindow子对象，因此不用声明父类，使用Py垃圾收集进行处理
            self.dirty=False #未修改文件的标志
            self.filename=None
            self.mirroredvertically=False #几个变量初始化为False
            self.mirroredhorizontally=False
            self.imagelabel=QLabel()
            self.imagelabel.setMinimumSize(200,200) #设置一个最小大小以防其不占用空间
            self.imagelabel.setAlignment(Qt.AlignCenter) #对Lable中的各图片保持水平和垂直居中
            self.imagelabel.setContextMenuPolicy(Qt.ActionsContextMenu) 
            # 添加上下文菜单的一个最简单的方法是对需要添加上下文的部件声明一个上下文菜单策略，然后向
            # 该窗口部件中添加一些动作。
            self.setCentralWidget(self.imagelabel) #imageLabel添加到MWindow中充当中心部件窗口
            # QLabel可以显示各种类型的文本、图片。中心部件窗口是复合窗口部件。
            # setCentralWidght可以设置什么部件为主窗口，同时也可以重新定义一个部件的父对象，让父窗口掌控它。
            logDockWidget=QDockWidget("Log Info",self)
            # 声明一个Dock组件，然后设置其父对象和标题名称，这样的话，当mainwindow被删除后，它也会被删除
            logDockWidget.setObjectName("LogDockWidget")
            # 设置此组件的ObjName ？？？什么用
            # 让PyQt能够保存和回复停靠窗口部件的尺寸大小和位置。因为一个地方可能有多个停靠窗口部件，通过变量名区分。
            logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
            # 设置dock在mianwindow的停靠区域。
            # 使用setFeatures()方法来控制Dock的移动、浮动和关闭属性。
            self.listWidget=QListWidget()
            logDockWidget.setWidget(self.listWidget)
            # 设置一个ListWidght，然后把它赋给logdockwidget
            self.addDockWidget(Qt.RightDockWidgetArea,logDockWidget)
            # 将dockwidght设置为默认呈现在mainwindow的右边。
            self.printer=None
            # 只有在需要打印机的时候，才会创建打印机对象。同时因为保留了打印机对象的印象，所以其会一直存在
            # 并且保留前一个状态，比如打印机的纸张大小和打印份数等
            self.sizeLabel=QLabel()
            self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            # 框架类型的设置
            status=self.statusBar()
            status.setSizeGripEnabled(False)
            status.addPermanentWidget(self.sizeLabel)
            status.showMessage("Ready Go!",5000)
            # 可以使用clearMessage或者showMessage方法清除或者挤掉上一条消息

            # fileNewAction=QAction(QIcon(":/filenew.png"),"&New...",self) #资源连接到qrc文件
            # # 对于窗口部件，通常对其进行布局来声明父对象，而对于QAction这种纯粹的数据对象，必须为其明确提供父对象
            # fileNewAction.setShortcut(QKeySequence.New)
            # helptext="新建一个图像"
            # fileNewAction.setToolTip(helptext)
            # fileNewAction.setStatusTip(helptext)
            # fileNewAction.triggered.connect(self.fileNew)
            # QAction 一共拥有data 设置用户数据、setdata 设置数据格式、ischecked 检查选中、setchecked 设置选中、is/setEnabled 设置可用
            # setseoarator 设置分隔符或者常规动作、setshortcut 设置键盘快捷方式、setext、settooltips、setstatustip
            # 设置提示在不同的对象上，toggled 选中状态改变的时候发出信号、triggered 调用时发出信号
            # 然后就可以按照下面的方法添加到菜单或者工具栏上了
            # fileMenu.addAction(fileNewAction)
            # filetoolbar.addAction(fileNewAction)


            fileNewAction = self.createAction("&New...", self.fileNew,QKeySequence.New, "filenew", "Create an image file")
            fileOpenAction = self.createAction("&Open...", self.fileOpen,QKeySequence.Open, "fileopen","Open an existing image file")
            fileSaveAction = self.createAction("&Save", self.fileSave,QKeySequence.Save, "filesave", "Save the image")
            fileSaveAsAction = self.createAction("Save &As...",self.fileSaveAs, icon="filesaveas",tip="Save the image using a new name")
            filePrintAction = self.createAction("&Print", self.filePrint,QKeySequence.Print, "fileprint", "Print the image")
            fileQuitAction = self.createAction("&Quit", self.close,"Ctrl+Q", "filequit", "Close the application")
            editInvertAction = self.createAction("&Invert",self.editInvert, "Ctrl+I", "editinvert","Invert the image's colors", True, "toggled")
            editSwapRedAndBlueAction = self.createAction("Sw&ap Red and Blue",self.editSwapRedAndBlue, "Ctrl+A", "editswap","Swap the image's red and blue color components", True,"toggled")
            editZoomAction = self.createAction("&Zoom...", self.editZoom,"Alt+Z", "editzoom", "Zoom the image")
            editResizeAction = self.createAction("&Resize...", self.reSize,"Alt+R", "editresize", "改变图像尺寸大小")

            
            # 动作群组 只允许一个开，其余的都是关
            mirrorGroup=QActionGroup(self)
            editUnMirrorAction=self.createAction("&Unmirror",self.editUnMirror,"Ctrl+U","editunmirror","Unmirror the image",True,"toggled")
            mirrorGroup.addAction(editUnMirrorAction)
            editMirrorHorizontalAction = self.createAction("Mirror &Horizontally", self.editMirrorHorizontal,"Ctrl+H", "editmirrorhoriz","Horizontally mirror the image", True, "toggled")
            mirrorGroup.addAction(editMirrorHorizontalAction)
            editMirrorVerticalAction = self.createAction("Mirror &Vertically", self.editMirrorVertical,"Ctrl+V", "editmirrorvert","Vertically mirror the image", True, "toggled")
            mirrorGroup.addAction(editMirrorVerticalAction)
            editUnMirrorAction.setChecked(True)
            # 在初始化的时候就应该是打开的动作。选中一个动作会使其发送toggled信号，但QImage
            # 仍然是空的，所以不会对一个空图片进行操作的。
            
            helpAboutAction = self.createAction("&About Image Changer",self.helpAbout)
            helpHelpAction = self.createAction("&Help", self.helpHelp,QKeySequence.HelpContents)

            self.fileMenu=self.menuBar().addMenu("&File")
            self.fileMenuActions=(fileNewAction,fileOpenAction,fileSaveAction,fileSaveAsAction,None,filePrintAction,fileQuitAction)
            self.fileMenu.aboutToShow.connect(self.updateFileMenu)

            editMenu=self.menuBar().addMenu("&Edit")
            self.addActions(editMenu,(editInvertAction,editSwapRedAndBlueAction,editZoomAction,editResizeAction))
            # mirrorMenu是子菜单，而不是一级菜单，因此其父对象改变了
            mirrorMenu=editMenu.addMenu(QIcon(":/editmirror.png"),"&Mirror")
            self.addActions(mirrorMenu,(editUnMirrorAction,editMirrorHorizontalAction,editMirrorVerticalAction))
            helpMenu=self.menuBar().addMenu("&Help")
            self.addActions(helpMenu,(helpAboutAction,helpHelpAction))

            fileToolbar=self.addToolBar("File")
            fileToolbar.setObjectName("FileToolBar")
            self.addActions(fileToolbar,(fileNewAction,fileOpenAction,fileSaveAsAction))
            
            editToolbar=self.addToolBar("Edit")
            editToolbar.setObjectName("EditToolBar")
            self.addActions(editToolbar,(editInvertAction,editSwapRedAndBlueAction,editUnMirrorAction,editMirrorHorizontalAction,editMirrorVerticalAction))
            
            self.zoomSpinBox=QSpinBox()
            self.zoomSpinBox.setRange(1,400)
            self.zoomSpinBox.setSuffix(" %")
            self.zoomSpinBox.setValue(100)
            self.zoomSpinBox.setToolTip("Zoom the Image")
            self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
            self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
            self.zoomSpinBox.valueChanged.connect(self.showImage) # 如果参数改变，则自动重新显示图像

            editToolbar.addWidget(self.zoomSpinBox)
            self.addActions(self.imagelabel,(editInvertAction,editSwapRedAndBlueAction,editUnMirrorAction,editMirrorHorizontalAction,editMirrorVerticalAction))
            # 全部都要添加，不论是否在组内
            self.resetableActions=( (editInvertAction,False),
                                    (editSwapRedAndBlueAction,False),
                                    (editUnMirrorAction,True))
            
            settings=QSettings() # 程序使用默认的组织和作者名字来填充字段，也就是下面__main__后面对MW实例进行的设置
            # 这些是在__init__的过程中进行的，因此不会出现闪屏。
            self.recentFiles=settings.value("RecentFiles") or []
            # size=setting.value("MainWindow/Size",QVariant(QSize(600,500))).toSize()
            # self.resize(size)
            # position=setting.value("MainWindow/Position",QVariant(QPoint(0,0))).toPoint()
            # self.move(position)
            # 从上次保存的过程中恢复位置、窗口大小以及获得最近文件列表
            setting_geo=settings.value("MainWindow/Geometry")
            setting_state=settings.value("MainWindow/State")

            if setting_geo is not None:
                    self.restoreGeometry(setting_geo)
            if setting_state is not None:
                    self.restoreState(setting_state)

            # restoreState()和saveState()可以将内容从QByteArray中恢复或者保存内容
            # 包括窗口大小、位置、工具栏位置、对停靠的那些具有唯一对象名的窗口部件和工具栏来说，才可以起作用。所以前面那个Log List设置了对象名（ObjectName）
            # 这两句是什么意思？？？？？？？？？？？？？？？？？？？
            self.setWindowTitle("CM Image Changer")
            self.updateFileMenu()
            QTimer.singleShot(0,self.loadInitialFile)
            # 打开最后一个文件，如果存在


    def addActions(self,target,actions):
            for action in actions:
                    if action is None:
                            target.addSeparator()
                    else:
                            target.addAction(action)

    def loadInitialFile(self): #从最后的qsetting中存储的数据中取出文件名
            setting=QSettings()
            fname=setting.value("LastFile")
            if fname and QFile.exists(fname):
                    self.loadFile(fname)

    def updateStatus(self,message):
            self.statusBar().showMessage(message,5000)
            self.listWidget.addItem(message)
            if self.filename is not None:
                    self.setWindowTitle("Image Changer - %s[*]"%os.path.basename(self.filename))
            elif not self.image.isNull():
                    self.setWindowTitle("Image Changer - Unnamed[*]")
            else:
                    self.setWindowTitle("Image Changer[*]")
            self.setWindowModified(self.dirty)
            #???????????????????????????????????????????
    def updateFileMenu(self):
            self.fileMenu.clear()
            self.addActions(self.fileMenu,self.fileMenuActions[:-1])#不要quit
            current=(self.filename if self.filename is not None else None)
            recentFiles=[]
            for fname in self.recentFiles:
                    if fname != current and QFile.exists(fname):
                            recentFiles.append(fname)
            if recentFiles:
                    self.fileMenu.addSeparator()
                    for i,fname in enumerate(recentFiles):
                            action=QAction(QIcon(":/icon.png)"),"&%s %s"%(i+1,QFileInfo(fname).fileName()),self)
                            action.setData(QVariant(fname))
                            # action.triggered.connect(self.loadFile)
                            self.fileMenu.addAction(action)
                            action.triggered.connect(self.loadFile)
                    self.fileMenu.addSeparator()
                    self.fileMenu.addAction(self.fileMenuActions[-1])

    def closeEvent(self,event): #觉察到关闭事件后，进行数据的保存，保存到QSetting里面
            if self.okToContinue():
                    settings = QSettings()
                    filename = (QVariant(self.filename)  if self.filename is not None else QVariant())
                    settings.setValue("LastFile", filename)
                    recentFiles = (QVariant(self.recentFiles) if self.recentFiles else QVariant())
                    # 关闭的时候保存RecentFile列表，以便下次打开程序的时候，通过loadInitialFile 和loadfile打开最后保存的文件
                    settings.setValue("RecentFiles", recentFiles)
                    settings.setValue("MainWindow/Geometry", QVariant(self.saveGeometry()))
                    settings.setValue("MainWindow/State", QVariant(self.saveState()))
            else:
                    event.ignore()

    def okToContinue(self): #弹出对话框要求保存，做出选择后返回True 在很多函数继续之前需要判断之前状态
            if self.dirty:
                    reply=QMessageBox.question(self,"Unsaved Changes","Save unsaved changes?",QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
                    if reply == QMessageBox.Cancel:
                            return False
                    elif reply == QMessageBox.Yes:
                            return self.fileSave()
            return True   
            # 不保存状态下，在__init__中声明的变量重新复制，对于action也重新进行初始化。详见fileNew()



    def createAction(self,text,slot=None,shortcut=None,icon=None,tip=None,
                    checkable=False,signal="triggered"):
            action=QAction(text,self)
            if icon is not None:
                    action.setIcon(QIcon(":/%s.png"%icon))
            if shortcut is not None:
                    action.setShortcut(shortcut)
            if tip is not None:
                    action.setToolTip(tip)
                    action.setStatusTip(tip)
            if slot is not None:
                    getattr(action,signal).connect(slot)
            # self.connect(action,SIGNAL(signal),slot) qt4中的信号方法
            if checkable:
                    action.setCheckable(True)
            return action

    def fileNew(self):
            if not self.okToContinue(): #判断当前任务是否完成，提示进行保存或重新加载
                    return
            dialog =newimagedlg.NewImageDlg(self)
            if dialog.exec_():
                    try:
                            self.addRecentFile(self.filename) # 将上一个图像添加到recentFile中
                            self.image=QImage() #对一些关键变量进行初始化（__init__内部的）
                            for action,check in self.resetableActions:
                                    action.setChecked(check) #对action进行初始化
                            self.image=dialog.image() #把生成的图像赋值给images属性
                            self.filename=None
                            self.dirty=True
                            # self.showImage() #展示图片，然后设置通知栏的提示和Log提示
                            try:
                                    self.showImage()
                            except:
                                    self.showbug()
                            self.sizeLabel.setText("%s × %s"%(self.image.width(),self.image.height()))
                            self.updateStatus("创建一个新图像")
                    except:
                            self.showbug()
    def fileOpen(self):
            try:
                    if not self.okToContinue():
                            return
                    dir=(os.path.dirname(self.filename) if self.filename is not None else ".")
                    formats=(['*.%s'%(str(format,encoding="utf8").lower()) for format in QImageReader.supportedImageFormats()])
                    fname=QFileDialog.getOpenFileName(self,"Image Changer - Choose a Picture",dir,"Image files (%s)"%(" ".join(formats)))[0]
                    # 最后面那一个是过滤参数，用于图片的过滤 最后的[0]表示我们仅仅需要返回第一个参数，也就是fname即可。
                    if fname:
                            self.loadFile(fname)
                            # QMessageBox.warning(self,"Test","%s"%fname)
            except:self.showbug()

    def loadFile(self,fname=None): #filename只是保存了文件名，而fname则保存了地址
        try:
            # QMessageBox.warning(self,"INFO0",str(fname))
            if fname is False:
                # 从File菜单中载入图像，action在updatefilemenu的时候，设置了setdata的属性，将文件名放在data内
                action=self.sender()
                # QMessageBox.warning(self,"INFO1",str(fname))
                if isinstance(action,QAction):
                    fname=str(action.data())
                    # QMessageBox.warning(self,"INFO2",fname)
                    if not self.okToContinue():
                        return
                else:
                    return
                #对于历史图像在 loadInitialFile 中，已经从qsetting的recentfile中传输出来文件名了，因此直接到这一步
            if fname:
                self.filename=None
                image=QImage(fname)
                if image.isNull():
                    message="载入 %s 失败"%fname
                else:
                    self.addRecentFile(fname) # 第一步就是加入RecentFile列表
                    # self.image=QImage() ？？？？？？？？？？？？？？？？？？？？感觉没作用，注释掉了
                    for action,check in self.resetableActions:
                        action.setChecked(check)
                    self.image=image
                    self.filename=fname
                    self.showImage()
                    self.dirty=False #设置为新，当进行处理时再重新设置，这样的话，仅仅查看但不更改就不会提醒保存
                    self.sizeLabel.setText("%s × %s"%(image.width(),image.height()))
                    message="载入 %s"%os.path.basename(fname)
                self.updateStatus(message)
        except:self.showbug()
            
    def fileSave(self):
            if self.image.isNull():
                return True
            if self.filename is None:
                return self.fileSaveAs() # 对于新建一个来讲，一般载入图片必然会有filename属性
            else:
                if self.image.save(self.filename,None): #直接将命令写到if的判断中
                    self.updateStatus("Saved ad %s"%self.filename)
                    self.dirty=False
                    return True
                else:
                    self.updateStatus("Failed to Save %s"%self.filename)
                    return False

    def fileSaveAs(self): # 这个程序有个缺点，就是另存为之后没有进行状态的更新，dirty没有改变（或者说这是个feature）
            if self.image.isNull():
                return True
            try:
                fname=self.filename if self.filename is not None else "."
                formats=(['*.%s'%(str(format,encoding="utf8").lower()) for format in QImageReader.supportedImageFormats()])
                fname=str(QFileDialog.getSaveFileName(self,"Save it",fname,"Image Files (%s)"%(" ".join(formats)))[0])
                if fname:
                    if "." not in fname:
                        fname +=".png"
                    self.addRecentFile(fname)
                    self.filename=fname
                    return self.fileSave()
                return False
            except: self.showbug()

    def filePrint(self): #相关技术在13章打印图片中进行讲解
        try:
            if self.image.isNull():
                return
            if self.printer is None:
                self.printer=QPrinter(QPrinter.HighResolution)
                self.printer.setPageSize(QPrinter.Letter)
            form =QPrintDialog(self.printer,self)
            if form.exec_():
                painter=QPainter(self.printer)
                rect=painter.viewport()
                size=self.image.size()
                size.scale(rect.size(),Qt.KeepAspectRatio)
                painter.setViewport(rect.x(),rect.y(),size.width(),size.height())
                painter.drawImage(0,0,self.image)
        except:self.showbug()

    def editInvert(self,on): #这个函数接受一个bool的troggled参数，判断是否按下。由action的信号所传递
            if self.image.isNull():
                return
            self.image.invertPixels()
            self.showImage()
            self.dirty=True
            self.updateStatus("Inverted" if on else "Uninverted")

    def editSwapRedAndBlue(self, on):
        if self.image.isNull():
            return
        self.image = self.image.rgbSwapped()
        self.showImage()
        self.dirty = True
        self.updateStatus(("Swapped Red and Blue" if on else "Unswapped Red and Blue"))

    def editZoom(self):
            pass

    def editUnMirror(self,on):
        if self.image.isNull():
            return
        if self.mirroredhorizontally: #如果打开了水平变换在，则进行撤销操作，此过程传递给水平变换函数，但其因为on
        #参数为flase所以更新状态栏为UnMirror，但是不在此进行显示status的原因是因为在函数内显示更精准
            self.editMirrorHorizontal(False)
        if self.mirroredvertically:
            self.editMirrorVertical(False)
        # self.updateStatus("完成撤销操作") #如果这样显示的话，在init的时候就会显示出来这一内容，显然我们不想看见，因此在此函数内不进行显示

    def editMirrorHorizontal(self,on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(True, False)
        self.showImage()
        self.mirroredhorizontally = not self.mirroredhorizontally
        self.dirty = True
        self.updateStatus(("Mirrored Horizontally"   if on else "Unmirrored Horizontally"))

    def editMirrorVertical(self,on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(False, True)
        self.showImage()
        self.mirroredvertically = not self.mirroredvertically
        self.dirty = True
        self.updateStatus(("Mirrored Vertically"   if on else "Unmirrored Vertically"))

    def helpAbout(self):
        QMessageBox.about(self, "关于此软件",
                """<b>Image Changer</b> v {0}
                <p>Copyright &copy; 2017 Marvin Studio
                <p>All rights reserved.
                <p>This application can be used to perform
                simple image manipulations.
                <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system()))

    def helpHelp(self):
        try:
            form = helpform.HelpForm("index.html", self)
            form.show()
        except:self.showbug()
    def showImage(self,percent=None): #包含缩放比例的显示图片函数，通过spinbox进行调节factor
            if self.image.isNull():
                    return
            if percent is None: #如果有传入就用传入的数值，如果没有就用zoomspinbox的数值
                    percent =self.zoomSpinBox.value()
            factor = percent/100.0
            width=self.image.width()*factor
            height=self.image.height()*factor
            image=self.image.scaled(width,height,Qt.KeepAspectRatio) #保持长宽比例
            self.imagelabel.setPixmap(QPixmap.fromImage(image))

    def showbug(self):
            _err=traceback.format_exc()
            QMessageBox.warning(self,"warning","%s"%_err,QMessageBox.Ok)

    def addRecentFile(self,fname):
            if fname is None:
                    return
            if not self.recentFiles.__contains__(fname):
                    self.recentFiles.append(fname)
                    while len(self.recentFiles)>9:
                            self.recentFiles.pop(0)

    def reSize(self):
        if self.image.isNull():
            return
        # QMessageBox.warning(self,"warning","%s,%s"%(self.image.width(),self.image.height()),QMessageBox.Ok)
        form=resizedlg.ResizeDlg(self.image.width(),self.image.height(),self)
        if form.exec_():
            try:
                width,height=form.result()
                # QMessageBox.warning(self,"warning","%s,%s"%(width,height),QMessageBox.Ok)
            except:self.showbug()
            if width==self.image.width() and height==self.image.height():
                self.updateStatus("重设为和原始一样大小的值")
            else:
                self.image = self.image.scaled(width, height)
                self.showImage()
                self.updateStatus("大小改变为 %s × %s"%(width,height))
                self.dirty=True
                self.sizeLabel.setText("%s × %s"%(width,height))
                



        
def main():
    app=QApplication(sys.argv)
    # 一次性的传递这些参数，在QSetting中就可以直接使用，而在之后的QSetting调用中就不用再设置了。
    app.setOrganizationName("Marvin Studio")
    app.setOrganizationDomain("http://www.marvinstudio.cn")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon.png"))
    form=MainWindow()
    form.show()
    app.exec_()
main()