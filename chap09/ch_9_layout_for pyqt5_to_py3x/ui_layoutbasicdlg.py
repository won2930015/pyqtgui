# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Corkine\Documents\工作文件夹\PyQt4toQt5_example\ch_9_layout\layoutbasicdlg.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_layoutBasicDlg(object):
    def setupUi(self, layoutBasicDlg):
        layoutBasicDlg.setObjectName("layoutBasicDlg")
        layoutBasicDlg.resize(660, 453)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(layoutBasicDlg.sizePolicy().hasHeightForWidth())
        layoutBasicDlg.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(layoutBasicDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(layoutBasicDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_6 = QtWidgets.QPushButton(layoutBasicDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_3.addWidget(self.pushButton_6)
        self.pushButton_5 = QtWidgets.QPushButton(layoutBasicDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setMaximumSize(QtCore.QSize(200, 50))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(layoutBasicDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(layoutBasicDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(layoutBasicDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 45))
        self.pushButton_2.setSizeIncrement(QtCore.QSize(0, 0))
        self.pushButton_2.setBaseSize(QtCore.QSize(0, 0))
        self.pushButton_2.setAutoDefault(True)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(layoutBasicDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(layoutBasicDlg)
        QtCore.QMetaObject.connectSlotsByName(layoutBasicDlg)

    def retranslateUi(self, layoutBasicDlg):
        _translate = QtCore.QCoreApplication.translate
        layoutBasicDlg.setWindowTitle(_translate("layoutBasicDlg", "布局测试对话框"))
        self.textBrowser.setHtml(_translate("layoutBasicDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">所有的项目可以设置四种不同的布局策略，分别是：</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1、扩张，在这种情况下，系统会自动扩张该方向，可设置最小和最大来限制扩张。如果希望两个组件大小成比例，可以设置不同伸展因子的扩张，这样的话，如果没有设置最小和最大，在默认情况下，这两个组件即会产生相应大小变化。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2、最适：一般规定即为表现状态，但是因为父布局的原因，所以一般设置最小和最大来限制。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3、最大：可以设置最大和最小，但是重点在于最大</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4、最小：可以设置最大和最小，但是重点在于最小</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">所有的子部件布局策略可能因为父对象的冲突而失效，比如第三排的右边默认值根据此横向布局中左边按钮的纵向高度45限制，其高度最小也是45，虽然没有对自身设置过。</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">在窗口整体布局中，选择对象查看器，对父对象进行布局选择。</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">所有的部件布局遵从父布局规则，即便冲突，根据父布局为准，比如父布局决定按钮文字必须完整显示，如果冲突，以父布局为准。</p></body></html>"))
        self.pushButton_6.setText(_translate("layoutBasicDlg", "横向：最小；纵向：最大"))
        self.pushButton_5.setText(_translate("layoutBasicDlg", "均扩张：最高50 最宽200"))
        self.pushButton_3.setText(_translate("layoutBasicDlg", "默认：纵向最小，横向扩张(伸展因子3)"))
        self.pushButton_4.setText(_translate("layoutBasicDlg", "默认：纵向最小，横向扩张(伸展因子2)"))
        self.pushButton_2.setText(_translate("layoutBasicDlg", "纵向最小(高度45)，横向扩张"))
        self.pushButton.setText(_translate("layoutBasicDlg", "默认(但根据父对象改变)：纵向最小，横向扩张"))

