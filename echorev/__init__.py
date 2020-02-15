#!/usr/bin/python3
# -*- coding: utf-8 -*-


version = '0.0.4'
date = '2020-02-16'

dpi = 128
# coding:utf-8

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QTextEdit, QMessageBox, QApplication, QVBoxLayout, QStatusBar, QMenu, QMenuBar, QAction, qApp
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys, os, re, webbrowser, requests

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

    targetversion = '0'
    def __init__(self):

        super(echorev, self).__init__()
        self.setObjectName('MainWindow')
        self.resize(800, 600)

        self.setWindowTitle('EchoRev')
        self.setWindowIcon(QIcon(LocationOfMySelf+'/icon.png'))
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

        self.actionWeb = QAction(QIcon(LocationOfMySelf+'/github.png'), u'GitHub',self)
        self.actionWeb.setObjectName('actionWeb')

        self.actionVersionCheck = QAction(QIcon(LocationOfMySelf+'/update.png'), u'Version',self)
        self.actionVersionCheck.setObjectName('actionVersionCheck')

        self.actionQuit =  QAction(QIcon(LocationOfMySelf+'/quit.png'), u'Quit',self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setShortcut('Ctrl+Q')

        self.actionWeb.triggered.connect(self.goGitHub)
        self.actionVersionCheck.triggered.connect(self.checkVersion)
        self.actionQuit.triggered.connect(qApp.quit)

        self.menubar = self.menuBar()
        self.menuHelp = self.menubar.addMenu('&Help')

        self.menuHelp.addAction(self.actionWeb)
        self.menuHelp.addAction(self.actionVersionCheck)
        self.menuHelp.addAction(self.actionQuit)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName('statusbar')
        self.statusbar.showMessage('The version is '+version+ '. Released at '+date)
        self.setStatusBar(self.statusbar)

        self.show()
    def goGitHub(self):
        webbrowser.open('https://github.com/cycleuser/EchoRev')
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)


    def checkVersion(self):
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)
        #reply = QMessageBox.information(self, 'Version', self.talk)

        url = 'https://github.com/cycleuser/EchoRev/master/echorev/__init__.py'


        r= 0
        try:
            r = requests.get(url, allow_redirects=True)
            r.raise_for_status()
            NewVersion = 'self.target' + r.text.splitlines()[0]

        except requests.exceptions.ConnectionError as err:
            #print(err)
            r=0
            buttonReply = QMessageBox.information(self, u'NetWork Error', 'You are using EchoRev ' + version +'\n'+'Net work unavailable.')
            NewVersion ="targetversion = '0'"

        except requests.exceptions.HTTPError as err:
            #print(err)
            r=0
            buttonReply = QMessageBox.information(self, u'NetWork Error', 'You are using EchoRev '+ version +'\n'+'Net work unavailable.')
            NewVersion ="targetversion = '0'"


        exec(NewVersion)
        #print('web is', self.targetversion)
        #print(NewVersion)


        self.talk=  'Version Online is '+ self.targetversion +'\n'+'You are using EchoRev '+ version +'\n'+ 'released on '+ date + '\n'



        if r != 0:


            #print('now is',version)
            if (version < self.targetversion):

                buttonReply = QMessageBox.question(self,  u'Version' ,
                                                   self.talk +   'New version available.\n Download and update?' ,
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    #print('Yes clicked.')
                    #qApp.quit
                    #pip.main(['install', 'geopytool', '--upgrade --no-cache-dir'])


                    #self.UpDate

                    webbrowser.open('https://github.com/cycleuser/EchoRev')
                else:
                    pass
                    #print('No clicked.')
            else:
                buttonReply = QMessageBox.information(self,   u'Version' ,
                                                      self.talk +  'This is the latest version.')

    def Magic(self):

        if (self.textbox_input.toPlainText() != ''):
            one_str = (self.textbox_input.toPlainText())
            #print(one_str)
            one_str_list = list(one_str)
            #print(one_str_list)
            one_str_list.reverse()
            result= ''.join(one_str_list)
            #print(result)
            self.textbox_output.setText(result)
            self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)
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
