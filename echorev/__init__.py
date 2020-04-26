#!/usr/bin/python3
# -*- coding: utf-8 -*-


version = '0.0.1'
date = '2020-02-15'
author = 'CycleUser'

dpi = 128
# coding:utf-8

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QTextEdit, QApplication, QVBoxLayout, QStatusBar
import sys, os, re

LocationOfMySelf=os.path.dirname(__file__)

class GrowingTextEdit(QTextEdit):

    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)

        self.heightMin = 0
        self.heightMax = 8

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)


class echorev(QMainWindow):
    def __init__(self):

        super(echorev, self).__init__()
        self.setObjectName('MainWindow')
        self.resize(800, 600)

        self.setWindowTitle('echorev')
        self.setAcceptDrops(True)
        self.main_widget = QWidget(self)

        self.main_frame = QWidget()
        self.textbox_input = GrowingTextEdit(self)
        self.textbox_input.textChanged.connect(self.Magic)
        self.textbox_output = GrowingTextEdit(self)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.textbox_input)
        self.vbox.addWidget(self.textbox_output)

        self.main_widget.setLayout(self.vbox)
        self.setCentralWidget(self.main_widget)

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName('statusbar')
        self.statusbar.showMessage('Writen by '+ author+'. The version is '+version+ '. Released at '+date)
        self.setStatusBar(self.statusbar)



        self.show()

    def Magic(self):

        if (self.textbox_input.toPlainText() != ''):
            one_str = (self.textbox_input.toPlainText())
            print(one_str)
            one_str_list = list(one_str)
            print(one_str_list)
            one_str_list.reverse()
            result= ''.join(one_str_list)
            print(result)
            self.textbox_output.setText(result)
            self.show()
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = echorev()
    sys.exit(app.exec_())
'''


def main():
    import sys

    app = QApplication(sys.argv)
    trans = QtCore.QTranslator()
    # trans.load('cn')  # 没有后缀.qm
    app.installTranslator(trans)
    mainWin = echorev()
    #mainWin.retranslateUi()
    mainWin.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
