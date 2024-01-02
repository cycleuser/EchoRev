# !/usr/bin/python3
# -*- coding: utf-8 -*-


version = '0.0.8'
date = '2022-03-30'

dpi = 128
# coding:utf-8
from PyQt5.QtWidgets import QWidget, QToolTip,QPushButton, QMainWindow, QWidget, QTextEdit, QMessageBox, QApplication, QHBoxLayout, QVBoxLayout, QStatusBar, QMenu, QMenuBar, QAction, qApp, QLabel ,QSlider
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTranslator
import time, sys, os, re, webbrowser, requests, urllib, bs4, csv
from bs4 import BeautifulSoup
import urllib.request
import http.cookiejar
from selenium import webdriver # 从selenium导入webdriver
from selenium.webdriver.firefox.options import Options


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


class echograb(QMainWindow):
    linkLists=[]
    targetversion = '0'


    def __init__(self):
        super(echograb, self).__init__()
        self.setObjectName('MainWindow')
        self.resize(800, 600)
        self.setWindowTitle('echograb')
        self.setWindowIcon(QIcon(LocationOfMySelf+'/icon.png'))
        self.setAcceptDrops(True)
        self.main_widget = QWidget(self)

        self.main_frame = QWidget()
        self.textbox_input = GrowingTextEdit(self)
        self.textbox_input.textChanged.connect(self.Magic)

        self.get_button = QPushButton('&GetLinks')
        self.get_button .clicked.connect(self.getLinks)

        self.textbox_output = GrowingTextEdit(self)

        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.textbox_input)
        self.vbox.addWidget(self.get_button)
        self.vbox.addWidget(self.textbox_output)

        self.vbox.addLayout(self.hbox)


        self.main_widget.setLayout(self.vbox)
        self.setCentralWidget(self.main_widget)


        self.actionGetLinks = QAction(QIcon(LocationOfMySelf+'/get.png'), u'GitHub',self)
        self.actionGetLinks.setObjectName('actionGetLinks')
        self.actionGetLinks.triggered.connect(self.getLinks)

        self.actionWeb = QAction(QIcon(LocationOfMySelf+'/github.png'), u'GitHub',self)
        self.actionWeb.setObjectName('actionWeb')
        self.actionWeb.triggered.connect(self.goGitHub)

        self.actionVersionCheck = QAction(QIcon(LocationOfMySelf+'/update.png'), u'Version',self)
        self.actionVersionCheck.setObjectName('actionVersionCheck')
        self.actionVersionCheck.triggered.connect(self.getVersion)

        self.actionQuit =  QAction(QIcon(LocationOfMySelf+'/quit.png'), u'Quit',self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setShortcut('Ctrl+Q')
        self.actionQuit.triggered.connect(qApp.quit)

        self.menubar = self.menuBar()
        self.menubar.addAction(self.actionGetLinks)
        self.menubar.addAction(self.actionWeb)
        self.menubar.addAction(self.actionVersionCheck)
        self.menubar.addAction(self.actionQuit)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName('statusbar')
        self.statusbar.showMessage('The version is '+version+ '. Released at '+date)
        self.setStatusBar(self.statusbar)

        w=self.width()
        h=self.height()
        self.show()

    def getLinks(self,word):
        # url = 'https://space.bilibili.com/872462/video'
        url = self.textbox_input.toPlainText()
        print(url)
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options= options)
        browser.get(url) # 获取页面
        # self.statusbar.setText('Sleep for 1 second')
        html = browser.page_source
        browser.close()
        html=html.replace('href','\n')
        html=html.replace('target','\n')
        html=html.replace('''><''','')
        html=html.replace('''=''','')
        html=html.replace('''_''','')
        html=html.replace('''blank''','')
        html=html.replace('''title''','')
        html=html.replace('''meta''','')
        html=html.replace('''play''','')
        html=html.replace('''class''','')
        html=html.replace('''icon''','')
        html=html.replace('''span''','')
        html=html.replace('''></i>''','')
        html=html.replace('''><i''','')
        html=html.replace('''<''','')
        html=html.replace('''>''','')

        html_content = html.splitlines()
        video_list = []
        f = open("./result.txt", "w+")
        for i in html_content:
            if('''www.bilibili.com/video/BV''' in i):
                i=i.replace('"','\n')
                i=i.replace('''//''','''https://''')
                print(len(i))
                video_list.append(i)
        video_str = ''.join(video_list)
        video_str = ''.join([s for s in video_str.splitlines(True) if s.strip()])
        tmp_list = video_str.splitlines()
        print(len(tmp_list))
        new_list = []
        for i in tmp_list:
            if('''www.bilibili.com/video/BV''' in i):
                print(len(i))
                if i not in new_list:
                    new_list.append(i)
                    f.write(i+"\n")
        result= ''.join(new_list)
        print(result)
        f.close()
        # self.statusbar.setText('Done')
        # self.textbox_output.setText(result)

    def goGitHub(self):
        webbrowser.open('https://github.com/cycleuser/')
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)
        pass

    def getVersion(self):
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)
        # reply = QMessageBox.information(self, 'Version', self.talk)

        url = 'https://raw.githubusercontent.com/cycleuser/EchoRev/master/echorev/test.py'

        r= 0
        try:
            r = requests.get(url, allow_redirects=True)
            r.raise_for_status()
            NewVersion = 'self.target' + r.text.splitlines()[0]

        except requests.exceptions.ConnectionError as err:
            #print(err)
            r=0
            buttonReply = QMessageBox.information(self, u'NetWork Error', 'You are using echograb ' + version +'\n'+'Net work unavailable.')
            NewVersion ="targetversion = '0'"

        except requests.exceptions.HTTPError as err:
            #print(err)
            r=0
            buttonReply = QMessageBox.information(self, u'NetWork Error', 'You are using echograb '+ version +'\n'+'Net work unavailable.')
            NewVersion ="targetversion = '0'"


        exec(NewVersion)
        #print('web is', self.targetversion)
        #print(NewVersion)


        self.talk=  'Version Online is '+ self.targetversion +'\n'+'You are using echograb '+ version +'\n'+ 'released on '+ date + '\n'



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

                    webbrowser.open('https://github.com/cycleuser/echograb')
                else:
                    pass
                    #print('No clicked.')
            else:
                buttonReply = QMessageBox.information(self,   u'Version' ,
                                                      self.talk +  'This is the latest version.')

    def Magic(self):
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)
        result = ''

        if (self.textbox_input.toPlainText() != ''):
            str = (self.textbox_input.toPlainText())
            self.linkLists = str.split('\n')

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = echograb()
    sys.exit(app.exec_())
'''


def main():
    import sys

    app = QApplication(sys.argv)
    trans = QTranslator()
    # trans.load('cn')  # 没有后缀.qm
    app.installTranslator(trans)
    mainWin = echograb()
    #mainWin.retranslateUi()
    mainWin.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
