#!/usr/bin/env python3

try:
    from tkinter import Tk
    from tkinter.messagebox import showwarning
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QGridLayout, QLabel, QSpinBox)
except Exception as _err:
    Tk().withdraw()
    warn=showwarning("WARNING","WARNING Info:\n%s"%_err)


class ResizeDlg(QDialog):
    def __init__(self, width=222, height=333, parent=None):
        super(ResizeDlg, self).__init__(parent)

        # QMessageBox.warning(self,"WARN","%s,%s"%(self.width,self.height))
        

        widthLabel=QLabel("&Width:")
        self.widthSpinBox=QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)

        
        self.widthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        # setvalue必须放在setrange后面，否则会死的！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        self.widthSpinBox.setSuffix(" px")
        self.widthSpinBox.setRange(4,width*4)
        self.widthSpinBox.setValue(width)

        
        heightLabel=QLabel("&Height:")
        self.heightSpinBox=QSpinBox()
        heightLabel.setBuddy(self.heightSpinBox)

        
        self.heightSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        # setvalue必须放在setrange后面，否则会死的！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        self.heightSpinBox.setSuffix(" px")
        self.heightSpinBox.setRange(4,height*4)
        self.heightSpinBox.setValue(height)
        
        buttonBox=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        layout=QGridLayout()
        layout.addWidget(widthLabel,0,0)
        layout.addWidget(heightLabel,1,0)
        layout.addWidget(self.widthSpinBox,0,1)
        layout.addWidget(self.heightSpinBox,1,1)

        layout.addWidget(buttonBox,2,0,1,2)
        self.setLayout(layout)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Image Changer - Resize")

    def result(self):
        return self.widthSpinBox.value(),self.heightSpinBox.value()

if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    form=ResizeDlg()
    form.show()
    app.exec_()