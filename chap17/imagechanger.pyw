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
#相关列程   6-imagechanger.pyw,
#         12-pagedesignet.pyw/multipedes.pyw(动画),
#         13-printing.pyw,pythoneditor.pyw(python文本编辑器)

import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import helpform
#import newimagedlg
import newimagedlg
import resizedlg
import qrc_resources


__version__ = "1.0.1"


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.mirroredvertically = False     #镜像_垂直
        self.mirroredhorizontally = False   #镜像_水平

        self.imageLabel = QLabel()  #用于装载图像.
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu) #setContextMenuPolicy::设置_上下文_菜单_策略, ActionsContextMenu::动作_上下文_菜单.
        self.setCentralWidget(self.imageLabel)

        logDockWidget = QDockWidget("Log", self)    #QDockWidget::船坞控件
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|    #setAllowedAreas::设置_允许_区域
                                      Qt.RightDockWidgetArea)
        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)   #自带内置方法.

        self.printer = None #创建 打印器 变量.

        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)#setFrameStyle::设置_框架_样式,
                                                                      # QFrame.StyledPanel::可变_面板,QFrame.Sunken::凹陷的
        status = self.statusBar()   #创建 状态条.
        status.setSizeGripEnabled(False) #设置_尽寸_调整_启用==False
        status.addPermanentWidget(self.sizeLabel)   #addPermanentWidget::加入_永久_控件
        self.statusBar().showMessage(self.tr("Ready"), 5000)

        fileNewAction = self.createAction(self.tr("&New..."),
                self.fileNew, QKeySequence.New, "filenew",
                self.tr("Create an image file"))
        fileOpenAction = self.createAction(self.tr("&Open..."),
                self.fileOpen, QKeySequence.Open, "fileopen",
                self.tr("Open an existing image file"))
        fileSaveAction = self.createAction(self.tr("&Save"),
                self.fileSave, QKeySequence.Save, "filesave",
                self.tr("Save the image"))
        fileSaveAsAction = self.createAction(self.tr("Save &As..."),
                self.fileSaveAs, icon="filesaveas",
                tip=self.tr("Save the image using a new name"))
        filePrintAction = self.createAction(self.tr("&Print"),
                self.filePrint, QKeySequence.Print, "fileprint",
                self.tr("Print the image"))
        fileQuitAction = self.createAction(self.tr("&Quit"),
                self.close, self.tr("Ctrl+Q"), "filequit",
                self.tr("Close the application"))
        editInvertAction = self.createAction(self.tr("&Invert"),    #editInvertAction::编缉_反相_动作
                self.editInvert, self.tr("Ctrl+I"), "editinvert",
                self.tr("Invert the image's colors"), True,
                "toggled(bool)")
        editSwapRedAndBlueAction = self.createAction(   #编辑_互换_红|蓝_动作
                self.tr("Sw&ap Red and Blue"),
                self.editSwapRedAndBlue, self.tr("Ctrl+A"), "editswap",
                self.tr("Swap the image's red and blue "
                        "color components"), True, "toggled(bool)")
        editZoomAction = self.createAction(self.tr("&Zoom..."), #editZoomAction::编辑_缩放_动作
                self.editZoom, self.tr("Alt+Z"), "editzoom",
                self.tr("Zoom the image"))
        editResizeAction = self.createAction(self.tr("&Resize..."), #editResizeAction ::编辑_调整尺寸_动作
                self.editResize, self.tr("Ctrl+R"), "editresize",
                self.tr("Resize the image"))
        mirrorGroup = QActionGroup(self)    #mirrorGroup::镜像_组.
        editUnMirrorAction = self.createAction(self.tr("&Unmirror"),    #editUnMirrorAction::编辑_取消_镜像_动作
                self.editUnMirror, self.tr("Ctrl+U"), "editunmirror",
                self.tr("Unmirror the image"), True, "toggled(bool)")
        mirrorGroup.addAction(editUnMirrorAction)
        editMirrorHorizontalAction = self.createAction( #editMirrorHorizontalAction::编辑_镜像_水平_动作
                self.tr("Mirror &Horizontally"),
                self.editMirrorHorizontal, self.tr("Ctrl+H"),
                "editmirrorhoriz",
                self.tr("Horizontally mirror the image"), True,
                "toggled(bool)")
        mirrorGroup.addAction(editMirrorHorizontalAction)
        editMirrorVerticalAction = self.createAction(   #editMirrorVerticalAction::编辑_镜像_垂直_动作
                self.tr("Mirror &Vertically"), self.editMirrorVertical,
                self.tr("Ctrl+V"), "editmirrorvert",
                self.tr("Vertically mirror the image"), True,
                "toggled(bool)")
        mirrorGroup.addAction(editMirrorVerticalAction)
        editUnMirrorAction.setChecked(True)     #setChecked::设置_选中 ==True
        helpAboutAction = self.createAction(    #helpAboutAction::关于_帮助_动作
                self.tr("&About Image Changer"), self.helpAbout)
        helpHelpAction = self.createAction(self.tr("&Help"),    #helpHelpAction::帮助_帮助_动作 ???
                self.helpHelp, QKeySequence.HelpContents)

        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenuActions = (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, None,
                filePrintAction, fileQuitAction)
        self.connect(self.fileMenu, SIGNAL("aboutToShow()"),    #关于_显示_时.
                     self.updateFileMenu)
        editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        self.addActions(editMenu, (editInvertAction,
                editSwapRedAndBlueAction, editZoomAction,
                editResizeAction))
        mirrorMenu = editMenu.addMenu(QIcon(":/editmirror.png"),    #加入子菜单::设置图标, 子菜单名.
                self.tr("&Mirror"))
        self.addActions(mirrorMenu, (editUnMirrorAction, editMirrorHorizontalAction, editMirrorVerticalAction))
        helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.addActions(helpMenu, (helpAboutAction, helpHelpAction))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")    #setObjectName::设置_对象_名(设置文件工具条对象名.)
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction, fileSaveAsAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editInvertAction,
                editSwapRedAndBlueAction, editUnMirrorAction,
                editMirrorVerticalAction, editMirrorHorizontalAction))
        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")    #setSuffix::设置_后缀
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip(self.tr("Zoom the image"))
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(Qt.NoFocus) #设置_焦点_策略
        self.connect(self.zoomSpinBox,
                     SIGNAL("valueChanged(int)"), self.showImage)
        editToolbar.addWidget(self.zoomSpinBox)

        self.addActions(self.imageLabel, (editInvertAction,
                editSwapRedAndBlueAction, editUnMirrorAction,
                editMirrorVerticalAction, editMirrorHorizontalAction))

        self.resetableActions = ((editInvertAction, False),     #resetableActions::复位_动作
                                 (editSwapRedAndBlueAction, False),
                                 (editUnMirrorAction, True))

        settings = QSettings()
        self.recentFiles = settings.value("RecentFiles") or []  #最近_文件.
        self.restoreGeometry(settings.value("MainWindow/Geometry",  #restoreGeometry::恢复_几何.
                QByteArray()))  #没有时返回::QByteArray 类量对象.
        self.restoreState(settings.value("MainWindow/State",    #restoreState::恢复_状态.
                QByteArray()))
        
        self.setWindowTitle(self.tr("Image Changer"))
        self.updateFileMenu()   #更新_文件_菜单.
        QTimer.singleShot(0, self.loadInitialFile)


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
            action.setCheckable(True)   #setCheckable::设置_能_可选的
        return action


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def closeEvent(self, event):
        if self.okToContinue(): #okToContinue::确认_继续(退出时保存各种状态)
            settings = QSettings()
            settings.setValue("LastFile", self.filename)    #最后_文件名.
            settings.setValue("RecentFiles", self.recentFiles or [])
            settings.setValue("MainWindow/Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
        else:
            event.ignore()


    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self,
                            self.tr("Image Changer - Unsaved Changes"), #图像_改变- 未保存改变
                            self.tr("Save unsaved changes?"),   #保存 未何存 改变 ?
                            QMessageBox.Yes|QMessageBox.No|
                            QMessageBox.Cancel)
            if reply == QMessageBox.Cancel: #取消操作.
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True


    def loadInitialFile(self):  #装载_初始_文件.
        settings = QSettings()
        fname = settings.value("LastFile")
        if fname and QFile.exists(fname):
            self.loadFile(fname)


    def updateStatus(self, message):    #更新_状态.
        self.statusBar().showMessage(message, 5000)
        self.listWidget.addItem(message)
        if self.filename is not None:
            self.setWindowTitle(self.tr("Image Changer - {}[*]").format(
                                os.path.basename(self.filename)))
        elif not self.image.isNull():
            self.setWindowTitle(self.tr("Image Changer - Unnamed[*]"))
        else:
            self.setWindowTitle(self.tr("Image Changer[*]"))
        self.setWindowModified(self.dirty)  #setWindowModified::设置_窗口_修改 属性.


    def updateFileMenu(self):
        self.fileMenu.clear()   #clear清除
        self.addActions(self.fileMenu, self.fileMenuActions[:-1])   #加入 0至 n-1项
        current = self.filename
        recentFiles = []
        for fname in self.recentFiles:
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
        if recentFiles:
            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QAction(QIcon(":/icon.png"),
                        "&{} {}".format(i + 1,
                        QFileInfo(fname).fileName()), self)
                action.setData(fname)
                self.connect(action, SIGNAL("triggered()"),
                             self.loadFile)
                self.fileMenu.addAction(action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileMenuActions[-1])   #加入最后一项


    def fileNew(self):
        if not self.okToContinue():
            return
        dialog = newimagedlg.NewImageDlg(self)
        if dialog.exec_():
            self.addRecentFile(self.filename)
            self.image = QImage()
            for action, check in self.resetableActions:
                action.setChecked(check)
            self.image = dialog.image()
            self.filename = None
            self.dirty = True
            self.showImage()
            self.sizeLabel.setText("{} x {}".format(self.image.width(),
                                                    self.image.height()))
            self.updateStatus(self.tr("Created new image"))


    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        formats = (["*.{}".format(format.data().decode("ascii").lower())
                   for format in QImageReader.supportedImageFormats()]) #supportedImageFormats::支持_图像_格式.
        fname = QFileDialog.getOpenFileName(self,
                    self.tr("Image Changer - Choose Image"), dir,
                    self.tr("Image files ({})").format(" ".join(formats)))
        if fname:
            self.loadFile(fname)


    def loadFile(self, fname=None):
        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = action.data()
                if not self.okToContinue():
                    return
            else:
                return
        if fname:
            self.filename = None
            image = QImage(fname)
            if image.isNull():
                message = self.tr("Failed to read {}").format(fname)    #Failed to read ::读_失败.
            else:
                self.addRecentFile(fname)
                self.image = QImage()
                for action, check in self.resetableActions:
                    action.setChecked(check)
                self.image = image
                self.filename = fname
                self.showImage()
                self.dirty = False
                self.sizeLabel.setText("{} x {}".format(
                                       image.width(), image.height()))
                message = self.tr("Loaded {}").format(os.path.basename(fname))
            self.updateStatus(message)


    def addRecentFile(self, fname): #加入_最近_文件
        if fname is None:
            return
        if fname not in self.recentFiles:
            self.recentFiles = [fname] + self.recentFiles[:8]   #记录最近打开的8+1个文件.


    def fileSave(self):
        if self.image.isNull():
            return True
        if self.filename is None:
            return self.fileSaveAs()
        else:
            if self.image.save(self.filename, None):
                self.updateStatus(self.tr("Saved as {}").format(self.filename))
                self.dirty = False
                return True
            else:
                self.updateStatus(self.tr("Failed to save {}").format(
                                  self.filename))
                return False


    def fileSaveAs(self):
        if self.image.isNull():
            return True
        fname = self.filename if self.filename is not None else "."
        formats = (["*.{}".format(format.data().decode("ascii").lower())    #生成:图像格式列表.
                   for format in QImageWriter.supportedImageFormats()]) #supportedImageFormats::支持_图像_格式
        fname = QFileDialog.getSaveFileName(self,
                        self.tr("Image Changer - Save Image"), fname,
                        self.tr("Image files ({})").format(" ".join(formats)))
        if fname:
            if "." not in fname:
                fname += ".png"
            self.addRecentFile(fname)   #加入_最近_文件
            self.filename = fname
            return self.fileSave()
        return False


    def filePrint(self):
        if self.image.isNull():
            return
        if self.printer is None:
            self.printer = QPrinter(QPrinter.HighResolution)
            self.printer.setPageSize(QPrinter.Letter)
        form = QPrintDialog(self.printer, self)
        if form.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(),
                                size.height())
            painter.drawImage(0, 0, self.image)


    def editInvert(self, on):   #编辑_反相.
        if self.image.isNull():
            return
        self.image.invertPixels()
        self.showImage()
        self.dirty = True
        self.updateStatus(self.tr("Inverted") if on else
                          self.tr("Uninverted"))


    def editSwapRedAndBlue(self, on):
        if self.image.isNull():
            return
        self.image = self.image.rgbSwapped()    #rgbSwapped::rbg调换
        self.showImage()
        self.dirty = True
        self.updateStatus(self.tr("Swapped Red and Blue") if on else
                          self.tr("Unswapped Red and Blue"))


    def editUnMirror(self, on):
        if self.image.isNull():
            return
        if self.mirroredhorizontally:
            self.editMirrorHorizontal(False)
        if self.mirroredvertically:
            self.editMirrorVertical(False)


    def editMirrorHorizontal(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(True, False)   #.mirrored::镜像(水平,垂直)
        self.showImage()
        self.mirroredhorizontally = not self.mirroredhorizontally
        self.dirty = True
        self.updateStatus(self.tr("Mirrored Horizontally") if on else
                          self.tr("Unmirrored Horizontally"))


    def editMirrorVertical(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(False, True)
        self.showImage()
        self.mirroredvertically = not self.mirroredvertically
        self.dirty = True
        self.updateStatus(self.tr("Mirrored Vertically") if on else
                          self.tr("Unmirrored Vertically"))


    def editZoom(self):
        if self.image.isNull():
            return
        percent, ok = QInputDialog.getInteger(self,
                self.tr("Image Changer - Zoom"),
                self.tr("Percent:"), self.zoomSpinBox.value(), 1, 400)
        if ok:
            self.zoomSpinBox.setValue(percent)


    def editResize(self):
        if self.image.isNull():
            return
        form = resizedlg.ResizeDlg(self.image.width(),
                                   self.image.height(), self)
        if form.exec_():
            width, height = form.result()
            if (width == self.image.width() and
                height == self.image.height()):
                self.statusBar().showMessage(
                        self.tr("Resized to the same size"), 5000)
            else:
                self.image = self.image.scaled(width, height)
                self.showImage()
                self.dirty = True
                size = "{} x {}".format(self.image.width(),
                                        self.image.height())
                self.sizeLabel.setText(size)
                self.updateStatus(self.tr("Resized to {}").format(size))


    def showImage(self, percent=None):  #显示_图像
        if self.image.isNull():
            return
        if percent is None: #percent::百份比
            percent = self.zoomSpinBox.value()
        factor = percent / 100.0    #factor::系数
        width = self.image.width() * factor
        height = self.image.height() * factor
        image = self.image.scaled(width, height, Qt.KeepAspectRatio)    #scale::比例,KeepAspectRatio::保持_纵横_比
        self.imageLabel.setPixmap(QPixmap.fromImage(image))


    def helpAbout(self):
        QMessageBox.about(self,
                self.tr("About Image Changer"),
                self.tr("""<b>Image Changer</b> v {0}
                <p>Copyright &copy; 2007-10 Qtrac Ltd. 
                All rights reserved.
                <p>This application can be used to perform
                simple image manipulations.
                <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system())))


    def helpHelp(self):
        form = helpform.HelpForm("index.html", self)
        form.show()


def main():
    app = QApplication(sys.argv)

    # Force language by passing it on the command line, e.g.
    #   imagechanger.pyw LANG=fr
    # or
    #   imagechanger.pyw LANG=de_DE.UTF-8
    # etc.
    locale = None   #locale::地区
    if len(sys.argv) > 1 and "=" in sys.argv[1]:
        key, value = sys.argv[1].split("=")
        if key == "LANG" and value:
            locale = value
    if locale is None:
        locale = QLocale.system().name()    #locale::地区
        print(locale)
    qtTranslator = QTranslator()
    if qtTranslator.load("qt_" + locale, ":/"):
        app.installTranslator(qtTranslator)
    appTranslator = QTranslator()
    if appTranslator.load("imagechanger_" + locale, ":/"):
        app.installTranslator(appTranslator)

    app.setOrganizationName("Qtrac Ltd.")   #设置_组织/机构_名
    app.setOrganizationDomain("qtrac.eu")   #设置_组织/机构_领域
    app.setApplicationName(app.translate("main", "Image Changer"))  #设置_应用_名
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()

