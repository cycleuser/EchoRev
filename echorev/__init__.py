#!/usr/bin/python3
# -*- coding: utf-8 -*-

version = '0.0.8'
date = '2024-10-17'

dpi = 128
# coding:utf-8

from PySide6.QtWidgets import QMainWindow, QWidget, QTextEdit, QMessageBox, QApplication, QHBoxLayout, QVBoxLayout, QStatusBar, QMenu, QMenuBar, QLabel, QSlider
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtCore import Qt, QTranslator
import sys, os, re, webbrowser, requests

LocationOfMySelf = os.path.dirname(__file__)

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
        self.setWindowIcon(QIcon(LocationOfMySelf + '/icon.png'))
        self.setAcceptDrops(True)
        self.main_widget = QWidget(self)

        self.main_frame = QWidget()
        self.textbox_input = GrowingTextEdit(self)
        self.textbox_input.textChanged.connect(self.Magic)
        self.textbox_output = GrowingTextEdit(self)

        self.slider_label = QLabel('Horizontal Reverse')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 2)
        self.slider.setValue(0)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Magic)  # int

        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.hbox.addWidget(self.slider_label)
        self.hbox.addWidget(self.slider)
        self.vbox.addWidget(self.textbox_input)
        self.vbox.addWidget(self.textbox_output)

        self.vbox.addLayout(self.hbox)

        self.main_widget.setLayout(self.vbox)
        self.setCentralWidget(self.main_widget)

        self.actionWeb = QAction(QIcon(LocationOfMySelf + '/github.png'), u'GitHub', self)
        self.actionWeb.setObjectName('actionWeb')

        self.actionVersionCheck = QAction(QIcon(LocationOfMySelf + '/update.png'), u'Version', self)
        self.actionVersionCheck.setObjectName('actionVersionCheck')

        self.actionQuit = QAction(QIcon(LocationOfMySelf + '/quit.png'), u'Quit', self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setShortcut('Ctrl+Q')

        self.actionWeb.triggered.connect(self.goGitHub)
        self.actionVersionCheck.triggered.connect(self.checkVersion)
        self.actionQuit.triggered.connect(QApplication.quit)

        self.menubar = self.menuBar()
        self.menuHelp = self.menubar.addMenu('&Help')

        self.menuHelp.addAction(self.actionWeb)
        self.menuHelp.addAction(self.actionVersionCheck)
        self.menuHelp.addAction(self.actionQuit)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName('statusbar')
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)
        self.setStatusBar(self.statusbar)

        w = self.width()
        h = self.height()
        self.slider.setFixedWidth(w / 10)

        self.show()

    def is_Chinese(self, word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    def goGitHub(self):
        webbrowser.open('https://github.com/cycleuser/EchoRev')
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)

    def checkVersion(self):
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)
        # reply = QMessageBox.information(self, 'Version', self.talk)

        url = 'https://raw.githubusercontent.com/cycleuser/EchoRev/master/echorev/__init__.py'

        r = 0
        try:
            r = requests.get(url, allow_redirects=True)
            r.raise_for_status()
            NewVersion = 'self.target' + r.text.splitlines()[0]

        except requests.exceptions.ConnectionError as err:
            # print(err)
            r = 0
            buttonReply = QMessageBox.information(self, u'NetWork Error', 'You are using EchoRev ' + version + '\n' + 'Net work unavailable.')
            NewVersion = "targetversion = '0'"

        except requests.exceptions.HTTPError as err:
            # print(err)
            r = 0
            buttonReply = QMessageBox.information(self, u'NetWork Error', 'You are using EchoRev ' + version + '\n' + 'Net work unavailable.')
            NewVersion = "targetversion = '0'"

        exec(NewVersion)
        # print('web is', self.targetversion)
        # print(NewVersion)

        self.talk = 'Version Online is ' + self.targetversion + '\n' + 'You are using EchoRev ' + version + '\n' + 'released on ' + date + '\n'

        if r != 0:

            # print('now is', version)
            if (version < self.targetversion):

                buttonReply = QMessageBox.question(self, u'Version',
                                                   self.talk + 'New version available.\n Download and update?',
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    # print('Yes clicked.')
                    # qApp.quit
                    # pip.main(['install', 'geopytool', '--upgrade --no-cache-dir'])

                    # self.UpDate

                    webbrowser.open('https://github.com/cycleuser/EchoRev')
                else:
                    pass
                    # print('No clicked.')
            else:
                buttonReply = QMessageBox.information(self, u'Version',
                                                      self.talk + 'This is the latest version.')

    def Magic(self):
        result = ''

        slider_value = int(self.slider.value())

        if slider_value == 0:
            self.slider_label.setText('Horizontal Reverse')
        elif slider_value == 1:
            self.slider_label.setText('Vertical Reverse')
        else:
            self.slider_label.setText('Traditional Chinese')

        if (self.textbox_input.toPlainText() != ''):
            str = (self.textbox_input.toPlainText())
            # print(str)
            str_list = list(str)
            # print(str_list)

            raw_list = str.split('\n')
            # print(raw_list)
            rev_list = []
            out_list = []

            if slider_value == 0:
                for i in raw_list:
                    rev_list.append(i[::-1])
                # print(rev_list)
                pass
            else:
                max_lenth = 0
                for i in raw_list:
                    if len(i) > max_lenth:
                        max_lenth = len(i)

                for i in range(max_lenth):
                    tmp_str = ''
                    for j in raw_list:
                        try:
                            tmp_str = tmp_str + ''.join(j[i])

                        except(IndexError):
                            if self.is_Chinese(raw_list):
                                tmp_str = tmp_str + ''.join('\u3000')
                            else:
                                tmp_str = tmp_str + ''.join('\u0020')

                            print(tmp_str)

                    print(tmp_str)
                    if slider_value == 1:
                        pass
                        out_list.append(''.join(tmp_str))
                    elif slider_value == 2:
                        out_list.append(''.join(tmp_str)[::-1])
                    else:
                        pass

                print('raw is', raw_list)
                print('\n out is', out_list)

                rev_list = out_list

            for k in rev_list:
                result = result + ''.join(k) + '\n'

            # result= ''.join(rev_list)
            # print(result)

            self.textbox_output.setText(result)
            self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)
            self.show()

def main():
    import sys

    app = QApplication(sys.argv)
    trans = QTranslator()
    # trans.load('cn')  # 没有后缀.qm
    app.installTranslator(trans)
    mainWin = echorev()
    # mainWin.retranslateUi()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())