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

import math
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qrc_resources


DATE_FORMAT = "MMM d, yyyy"


class Statement(object):    #声明_对象

    def __init__(self, company, contact, address):
        self.company = company  #公司
        self.contact = contact  #联系人
        self.address = address  #地址
        self.transactions = [] # List of (QDate, float) two-tuples::两个-元组


    def balance(self):  #结算::返回amount总和.
        return sum([amount for date, amount in self.transactions])


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.printer = QPrinter()   #创建打印对象
        self.printer.setPageSize(QPrinter.Letter)   #设置页格式
        self.generateFakeStatements()   #生成_伪_清单
        self.table = QTableWidget()     #TableWidget::表_部件
        self.populateTable()    #填充_表格部件

        cursorButton = QPushButton("Print via Q&Cursor")
        htmlButton = QPushButton("Print via &HTML")
        painterButton = QPushButton("Print via Q&Painter")
        quitButton = QPushButton("&Quit")

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(cursorButton)
        buttonLayout.addWidget(htmlButton)
        buttonLayout.addWidget(painterButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(cursorButton, SIGNAL("clicked()"),
                     self.printViaQCursor)
        self.connect(htmlButton, SIGNAL("clicked()"),
                     self.printViaHtml)
        self.connect(painterButton, SIGNAL("clicked()"),
                     self.printViaQPainter)
        self.connect(quitButton, SIGNAL("clicked()"), self.accept)

        self.setWindowTitle("Printing")


    def generateFakeStatements(self):   #生成_伪_清单
        self.statements = []
        statement = Statement("Consality", "Ms S. Royal",
                "234 Rue Saint Hyacinthe, 750201, Paris")
        statement.transactions.append((QDate(2007, 8, 11), 2342))
        statement.transactions.append((QDate(2007, 9, 10), 2342))
        statement.transactions.append((QDate(2007, 10, 9), 2352))
        statement.transactions.append((QDate(2007, 10, 17), -1500))
        statement.transactions.append((QDate(2007, 11, 12), 2352))
        statement.transactions.append((QDate(2007, 12, 10), 2352))
        statement.transactions.append((QDate(2007, 12, 20), -7500))
        statement.transactions.append((QDate(2007, 12, 20), 250))
        statement.transactions.append((QDate(2008, 1, 10), 2362))
        self.statements.append(statement)

        statement = Statement("Demamitur Plc", "Mr G. Brown",
                "14 Tall Towers, Tower Hamlets, London, WC1 3BX")
        statement.transactions.append((QDate(2007, 5, 21), 871))
        statement.transactions.append((QDate(2007, 6, 20), 542))
        statement.transactions.append((QDate(2007, 7, 20), 1123))
        statement.transactions.append((QDate(2007, 7, 20), -1928))
        statement.transactions.append((QDate(2007, 8, 13), -214))
        statement.transactions.append((QDate(2007, 9, 15), -3924))
        statement.transactions.append((QDate(2007, 9, 15), 2712))
        statement.transactions.append((QDate(2007, 9, 15), -273))
        statement.transactions.append((QDate(2007, 11, 8), -728))
        statement.transactions.append((QDate(2008, 2, 7), 228))
        statement.transactions.append((QDate(2008, 3, 13), -508))
        statement.transactions.append((QDate(2008, 3, 22), -2481))
        statement.transactions.append((QDate(2008, 4, 5), 195))
        self.statements.append(statement)


    def populateTable(self):    #填充_表格部件
        headers = ["Company", "Contact", "Address", "Balance"]
        self.table.setColumnCount(len(headers)) #setColumnCount::设置_栏_数
        self.table.setHorizontalHeaderLabels(headers)   #setHorizontalHeaderLabels::设置_水平_头_标签
        self.table.setRowCount(len(self.statements))
        for row, statement in enumerate(self.statements):
            self.table.setItem(row, 0,
                    QTableWidgetItem(statement.company))
            self.table.setItem(row, 1,
                    QTableWidgetItem(statement.contact))
            self.table.setItem(row, 2,
                    QTableWidgetItem(statement.address))
            item = QTableWidgetItem("$ {:,.2f}".format(
                                    statement.balance()))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.table.setItem(row, 3, item)
        self.table.resizeColumnsToContents()    #调整_栏_to_内容::调整栏宽度适配内容.

    #用Html方式生成文字表格后打印.
    def printViaHtml(self):
        html = ""
        for i, statement in enumerate(self.statements):
            date = QDate.currentDate().toString(DATE_FORMAT)    #获得当前时间.
            address = Qt.escape(statement.address).replace( ",", "<br>")    #escape::换码
            contact = Qt.escape(statement.contact)
            balance = statement.balance()
            html += ("<p align=right><img src=':/logo.png'></p>"
                     "<p align=right>Greasy Hands Ltd."
                     "<br>New Lombard Street"
                     "<br>London<br>WC13 4PX<br>{0}</p>"
                     "<p>{1}</p><p>Dear {2},</p>"
                     "<p>The balance of your account is {3}.").format(
                     date, address, contact, "$ {:,.2f}".format(balance))
            if balance < 0:
                html += (" <p><font color=red><b>Please remit the "
                         "amount owing immediately.</b></font>")
            else:
                html += (" We are delighted to have done business "
                         "with you.")
            html += ("</p><p>&nbsp;</p><p>"
                     "<table border=1 cellpadding=2 "
                     "cellspacing=2><tr><td colspan=3>" #<tr>==行,<td>==单元格
                     "Transactions</td></tr>")
            for date, amount in statement.transactions:
                color, status = "black", "Credit"
                if amount < 0:
                    color, status = "red", "Debit"
                html += ("<tr><td align=right>{0}</td>"
                         "<td>{1}</td><td align=right>"
                         "<font color={2}>{3}</font></td></tr>".format(
                         date.toString(DATE_FORMAT), status, color,
                         "$ {:,.2f}".format(abs(amount))))
            html += "</table></p>"
            html += ("<p style='page-break-after:always;'>"     #page-break-after:插入分页符,after:在指定组件之后插入.(ps::http://bbs.csdn.net/topics/380127102)
                     if i + 1 < len(self.statements) else "<p>")
            html += ("We hope to continue doing "
                     "business with you,<br>Yours sincerely,"
                     "<br><br>K.&nbsp;Longrey, Manager</p>")
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QTextDocument()
            document.setHtml(html)
            document.print_(self.printer)

    #用光标方法生成文字和表格后打印.
    def printViaQCursor(self):
        dialog = QPrintDialog(self.printer, self)
        if not dialog.exec_():
            return
        logo = QPixmap(":/logo.png")
        headFormat = QTextBlockFormat()
        headFormat.setAlignment(Qt.AlignLeft)
        headFormat.setTextIndent(   #设置_文本_缩进
                self.printer.pageRect().width() - logo.width() - 216)
        bodyFormat = QTextBlockFormat()
        bodyFormat.setAlignment(Qt.AlignJustify)    #AlignJustify::对齐_两端(两端对齐)
        lastParaBodyFormat = QTextBlockFormat(bodyFormat)
        lastParaBodyFormat.setPageBreakPolicy(      #设置_分页_规则
                QTextFormat.PageBreak_AlwaysAfter)
        rightBodyFormat = QTextBlockFormat()
        rightBodyFormat.setAlignment(Qt.AlignRight)

        headCharFormat = QTextCharFormat()
        headCharFormat.setFont(QFont("Helvetica", 10))
        bodyCharFormat = QTextCharFormat()
        bodyCharFormat.setFont(QFont("Times", 11))
        redBodyCharFormat = QTextCharFormat(bodyCharFormat)
        redBodyCharFormat.setForeground(Qt.red)

        tableFormat = QTextTableFormat()
        tableFormat.setBorder(1)
        tableFormat.setCellPadding(2)
        document = QTextDocument()  #创建文本文件对象.
        cursor = QTextCursor(document)  #创建 文本_光标::以文本文件对象创建一个光标.
        mainFrame = cursor.currentFrame() #光标.当前_框架 ???
        page = 1
        for statement in self.statements:
            cursor.insertBlock(headFormat, headCharFormat)  #insertBlock::插入_块
            cursor.insertImage(":/logo.png")
            for text in ("Greasy Hands Ltd.", "New Lombard Street",
                         "London", "WC13 4PX",
                         QDate.currentDate().toString(DATE_FORMAT)):
                cursor.insertBlock(headFormat, headCharFormat)
                cursor.insertText(text)
            for line in statement.address.split(", "):
                cursor.insertBlock(bodyFormat, bodyCharFormat)
                cursor.insertText(line)
            cursor.insertBlock(bodyFormat)  #以bodyFormat格式插入空行
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            cursor.insertText("Dear {},".format(statement.contact))
            cursor.insertBlock(bodyFormat)
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            balance = statement.balance()
            cursor.insertText("The balance of your account is $ {:,.2f}."
                              .format(balance))
            if balance < 0:
                cursor.insertBlock(bodyFormat, redBodyCharFormat)
                cursor.insertText("Please remit the amount owing "
                                  "immediately.")
            else:
                cursor.insertBlock(bodyFormat, bodyCharFormat)
                cursor.insertText("We are delighted to have done "
                                  "business with you.")
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            cursor.insertText("Transactions:")
            table = cursor.insertTable(len(statement.transactions), 3,  #插入表格(行,列)
                                       tableFormat)
            row = 0
            for date, amount in statement.transactions:
                cellCursor = table.cellAt(row, 0).firstCursorPosition() #firstCursorPosition::第一_光标_位置()
                cellCursor.setBlockFormat(rightBodyFormat)  #光标_单元格.设置_块_格式
                cellCursor.insertText(date.toString(DATE_FORMAT), bodyCharFormat)
                cellCursor = table.cellAt(row, 1).firstCursorPosition()
                if amount > 0:
                    cellCursor.insertText("Credit", bodyCharFormat)
                else:
                    cellCursor.insertText("Debit", bodyCharFormat)
                cellCursor = table.cellAt(row, 2).firstCursorPosition()
                cellCursor.setBlockFormat(rightBodyFormat)
                format = bodyCharFormat
                if amount < 0:
                    format = redBodyCharFormat
                cellCursor.insertText("$ {:,.2f}".format(amount), format)
                row += 1    #行 +=1
            cursor.setPosition(mainFrame.lastPosition())    #主_框架.最后_位置()::定位到主框架最后位置.
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            cursor.insertText("We hope to continue doing business "
                              "with you,")
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            cursor.insertText("Yours sincerely")
            cursor.insertBlock(bodyFormat)
            if page == len(self.statements):
                cursor.insertBlock(bodyFormat, bodyCharFormat)
            else:
                cursor.insertBlock(lastParaBodyFormat, bodyCharFormat)
            cursor.insertText("K. Longrey, Manager")
            page += 1
        document.print_(self.printer)   #document对象向printer对象输出内容.


    def printViaQPainter(self):
        dialog = QPrintDialog(self.printer, self)
        if not dialog.exec_():
            return
        LeftMargin = 72 #左_边缘
        sansFont = QFont("Helvetica", 10)
        sansLineHeight = QFontMetrics(sansFont).height()
        serifFont = QFont("Times", 11)  #衬线字体
        fm = QFontMetrics(serifFont)
        DateWidth = fm.width(" September 99, 2999 ")    #日期栏_宽度
        CreditWidth = fm.width(" Credit ")      #信贷栏_宽度
        AmountWidth = fm.width(" W999999.99 ")  #合计栏_宽度
        serifLineHeight = fm.height()
        logo = QPixmap(":/logo.png")
        painter = QPainter(self.printer)        #Painter::画(画纸).
        pageRect = self.printer.pageRect()
        page = 1
        for statement in self.statements:
            painter.save()
            y = 0
            x = pageRect.width() - logo.width() - LeftMargin
            painter.drawPixmap(x, 0, logo)
            y += logo.height() + sansLineHeight
            painter.setFont(sansFont)
            painter.drawText(x, y, "Greasy Hands Ltd.")
            y += sansLineHeight
            painter.drawText(x, y, "New Lombard Street")
            y += sansLineHeight
            painter.drawText(x, y, "London")
            y += sansLineHeight
            painter.drawText(x, y, "WC13 4PX")
            y += sansLineHeight
            painter.drawText(x, y,
                    QDate.currentDate().toString(DATE_FORMAT))
            y += sansLineHeight
            painter.setFont(serifFont)
            x = LeftMargin
            for line in statement.address.split(", "):
                painter.drawText(x, y, line)
                y += serifLineHeight
            y += serifLineHeight
            painter.drawText(x, y, "Dear {},".format(statement.contact))
            y += serifLineHeight
            balance = statement.balance()
            painter.drawText(x, y, "The balance of your "
                    "account is $ {:,.2f}".format(balance))
            y += serifLineHeight
            if balance < 0:
                painter.setPen(Qt.red)
                text = "Please remit the amount owing immediately."
            else:
                text = ("We are delighted to have done business "
                        "with you.")
            painter.drawText(x, y, text)
            painter.setPen(Qt.black)
            y += int(serifLineHeight * 1.5)
            painter.drawText(x, y, "Transactions:")
            y += serifLineHeight
            option = QTextOption(Qt.AlignRight|Qt.AlignVCenter)
            for date, amount in statement.transactions:
                x = LeftMargin
                h = int(fm.height() * 1.3)
                painter.drawRect(x, y, DateWidth, h)
                painter.drawText(
                        QRectF(x + 3, y + 3, DateWidth - 6, h - 6),
                        date.toString(DATE_FORMAT), option)
                x += DateWidth
                painter.drawRect(x, y, CreditWidth, h)
                text = "Credit"
                if amount < 0:
                    text = "Debit"
                painter.drawText(
                        QRectF(x + 3, y + 3, CreditWidth - 6, h - 6),
                        text, option)
                x += CreditWidth
                painter.drawRect(x, y, AmountWidth, h)
                if amount < 0:
                    painter.setPen(Qt.red)
                painter.drawText(
                        QRectF(x + 3, y + 3, AmountWidth - 6, h - 6),
                        "$ {:,.2f}".format(amount), option)
                painter.setPen(Qt.black)
                y += h
            y += serifLineHeight
            x = LeftMargin
            painter.drawText(x, y, "We hope to continue doing "
                                   "business with you,")
            y += serifLineHeight
            painter.drawText(x, y, "Yours sincerely")
            y += serifLineHeight * 3
            painter.drawText(x, y, "K. Longrey, Manager")
            x = LeftMargin
            y = pageRect.height() - 54
            painter.drawLine(x, y, pageRect.width() - LeftMargin, y)
            y += 2
            font = QFont("Helvetica", 9)
            font.setItalic(True)
            painter.setFont(font)
            option = QTextOption(Qt.AlignCenter)    #TextOption::文件选项
            option.setWrapMode(QTextOption.WordWrap)    #自动换行
            painter.drawText(
                    QRectF(x, y, pageRect.width() - 2 * LeftMargin, 31),
                    "The contents of this letter are for information "
                    "only and do not form part of any contract.",
                    option)
            page += 1
            if page <= len(self.statements):
                self.printer.newPage()
            painter.restore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()

