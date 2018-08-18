#!/usr/bin/env python3

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import moviedata
import cmui_addeditmoviedlg

class AddEditMovieDlg(QDialog,cmui_addeditmoviedlg.Ui_Dialog):
    def __init__(self,movies,movie=None,parent=None):
        super(AddEditMovieDlg,self).__init__(parent)
        self.setupUi(self)

        self.movies=movies
        self.movie=movie
        if movie is not None:
            self.lineEdit.setText(movie.title)
            self.spinBox.setValue(movie.year)
            self.spinBox_2.setValue(movie.minutes)
            self.dateEdit.setDate(movie.acquired)
            self.dateEdit.setEnabled(False)
            self.lineEdit_2.setText(movie.locations)
            self.plainTextEdit.setPlainText(movie.notes)
            self.plainTextEdit.setFocus()
            self.buttonBox.button(QDialogButtonBox.Ok).setText("确定(&O)")
            self.setWindowTitle("My Movies - Edit Movie")
        else:
            today = QDate.currentDate()
            self.dateEdit.setDate(today)
            self.lineEdit.setFocus()
            self.spinBox.setRange(0,3000)
            self.spinBox.setSingleStep(1)
            self.spinBox.setSuffix(" 年")
            self.spinBox_2.setRange(0,300)
            self.spinBox_2.setSingleStep(5)
            self.spinBox_2.setSuffix(" 分钟")
            self.setWindowTitle("My Movies - Add Movie")
        
    def accept(self):
        title=self.lineEdit.text()
        year=self.spinBox.value()
        minutes=self.spinBox_2.value()
        locations=self.lineEdit_2.text()
        notes=self.plainTextEdit.toPlainText()
        # QMessageBox.warning(self,"Test",notes)
        if self.movie is None:
            acquired=self.dateEdit.date()
            self.movie=moviedata.Movie(title,year,minutes,acquired,locations,notes)
            self.movies.add(self.movie)
        else:
            self.movies.updateMovie(self.movie,title,year,minutes,locations,notes)
        QDialog.accept(self)

if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    form=AddEditMovieDlg(0)
    form.show()
    app.exec_()