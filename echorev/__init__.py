#!/usr/bin/python3
# -*- coding: utf-8 -*-

version = '0.0.9'  # 定义版本号
date = '2024-10-18'  # 定义发布日期

dpi = 128  # 定义DPI
# coding:utf-8

# 导入所需的模块
from PySide6.QtWidgets import QMainWindow, QWidget, QTextEdit, QMessageBox, QApplication, QFileDialog, QHBoxLayout, QVBoxLayout, QStatusBar, QMenu, QMenuBar, QLabel, QSlider
from PySide6.QtGui import QPixmap, QIcon, QAction, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QTranslator
import sys, os, re, webbrowser, requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

LocationOfMySelf = os.path.dirname(__file__)  # 获取当前文件所在目录

class GrowingTextEdit(QTextEdit):
    # 自定义的文本编辑器类，继承自QTextEdit
    def __init__(self, watermark_text="", *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.watermark_text = watermark_text
        self.document().contentsChanged.connect(self.sizeChange)  # 连接内容变化信号到sizeChange槽

        self.heightMin = 0  # 最小高度
        self.heightMax = 8  # 最大高度

    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self.watermark_text:
            painter = QPainter(self.viewport())
            painter.setPen(QColor(200, 200, 200, 128))  # 设置水印颜色和透明度
            painter.setFont(QFont("Arial", 20, QFont.Bold))  # 设置水印字体和大小
            painter.drawText(self.rect(), Qt.AlignCenter, self.watermark_text)  # 在中心绘制水印文本
            painter.end()

    def sizeChange(self):
        # 当内容变化时调整高度
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)

class echorev(QMainWindow):
    # 主窗口类，继承自QMainWindow

    targetversion = '0'  # 目标版本号
    def __init__(self):
        super(echorev, self).__init__()
        self.private_key = None  # 私钥
        self.public_key = None  # 公钥
        self.private_key_path = ''
        self.public_key_path = ''

        self.build_ui()  # 创建UI

    def build_ui(self):
        self.setObjectName('MainWindow')  # 设置对象名称
        self.resize(800, 600)  # 调整窗口大小

        self.setWindowTitle('EchoRev')  # 设置窗口标题
        self.setWindowIcon(QIcon(LocationOfMySelf + '/icon.png'))  # 设置窗口图标
        self.setAcceptDrops(True)  # 允许拖放操作
        self.main_widget = QWidget(self)  # 创建主部件

        self.main_frame = QWidget()  # 创建主框架
        self.textbox_input = GrowingTextEdit(watermark_text="Text Input")  # 创建输入文本框
        self.textbox_input.textChanged.connect(self.Magic)  # 连接文本变化信号到Magic槽
        self.textbox_output = GrowingTextEdit(watermark_text="Text Output")  # 创建输出文本框

        self.textbox_crype = GrowingTextEdit(watermark_text="Text Crype")  # 创建加密文本框
        # self.textbox_crype.textChanged.connect(self.MagicCrype)  
        self.textbox_decrypt = GrowingTextEdit(watermark_text="Text Decrypt") # 创建解密文本框
        # self.textbox_decrypt.textChanged.connect(self.MagicDecrypt)

        self.slider_label = QLabel('Horizontal Reverse')  # 创建滑块标签
        self.slider = QSlider(Qt.Horizontal)  # 创建水平滑块
        self.slider.setRange(0, 2)  # 设置滑块范围
        self.slider.setValue(0)  # 设置滑块初始值
        self.slider.setTracking(True)  # 设置滑块跟踪
        self.slider.setTickPosition(QSlider.TicksBothSides)  # 设置滑块刻度位置
        self.slider.valueChanged.connect(self.Magic)  # 连接滑块值变化信号到Magic槽

        self.hbox = QHBoxLayout()  # 创建水平布局        
        self.hbox_up = QHBoxLayout()  # 创建水平布局        
        self.hbox_down = QHBoxLayout()  # 创建水平布局

        self.vbox = QVBoxLayout()  # 创建垂直布局
        self.hbox.addWidget(self.slider)  # 将滑块添加到水平布局
        self.hbox.addWidget(self.slider_label)  # 将滑块标签添加到水平布局

        self.hbox_up.addWidget(self.textbox_input) 
        self.hbox_up.addWidget(self.textbox_crype)
        self.hbox_down.addWidget(self.textbox_output)
        self.hbox_down.addWidget(self.textbox_decrypt)

        self.vbox.addLayout(self.hbox_up)  # 将水平布局添加到垂直布局
        self.vbox.addLayout(self.hbox_down)

        self.vbox.addLayout(self.hbox)  # 将水平布局添加到垂直布局
        self.main_widget.setLayout(self.vbox)  # 设置主部件的布局
        self.setCentralWidget(self.main_widget)  # 设置中央部件

        # 创建菜单动作
        self.actionWeb = QAction(u'GitHub', self)
        self.actionWeb.setObjectName('actionWeb')
        self.actionWeb.triggered.connect(self.goGitHub)
        
        self.actionVersionCheck = QAction(u'Version', self)
        self.actionVersionCheck.setObjectName('actionVersionCheck')
        self.actionVersionCheck.triggered.connect(self.checkVersion)
        
        self.actionQuit = QAction(u'Quit', self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setShortcut('Ctrl+Q')  # 设置快捷键     
        self.actionQuit.triggered.connect(QApplication.quit)
        
        self.actionGenerateKeys = QAction(u'Generate Keys', self)
        self.actionGenerateKeys.setObjectName('actionGenerateKeys')
        self.actionGenerateKeys.setShortcut('Ctrl+G')  # 设置快捷键
        self.actionGenerateKeys.triggered.connect(self.generate_keys)

        self.actionLoadPrivateKey = QAction(u'Load Private Key', self)
        self.actionLoadPrivateKey.setObjectName('actionLoadPrivateKey')
        self.actionLoadPrivateKey.triggered.connect(self.load_private_key)

        self.actionLoadPublicKey = QAction(u'Load Public Key', self)
        self.actionLoadPublicKey.setObjectName('actionLoadPublicKey')
        self.actionLoadPublicKey.triggered.connect(self.load_public_key)

        self.actionCrype = QAction(u'Crype', self)
        self.actionCrype.setObjectName('actionCrype')
        self.actionCrype.triggered.connect(self.MagicCrype)

        self.actionDecrypt = QAction(u'Decrypt', self)
        self.actionDecrypt.setObjectName('actionDecrypt')
        self.actionDecrypt.triggered.connect(self.MagicDecrypt)

        self.menubar = self.menuBar()  # 创建菜单栏
        # self.menuHelp = self.menubar.addMenu('&Help')  # 添加帮助菜单

        # 将动作添加到帮助菜单
        self.menubar.addAction(self.actionGenerateKeys)  # 将动作添加到菜单栏
        self.menubar.addAction(self.actionLoadPrivateKey)
        self.menubar.addAction(self.actionLoadPublicKey)
        self.menubar.addAction(self.actionCrype)
        self.menubar.addAction(self.actionDecrypt)
        self.menubar.addAction(self.actionWeb)
        self.menubar.addAction(self.actionVersionCheck)
        self.menubar.addAction(self.actionQuit)

        self.statusbar = QStatusBar(self)  # 创建状态栏
        self.statusbar.setObjectName('statusbar')
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)  # 显示版本信息
        self.setStatusBar(self.statusbar)  # 设置状态栏

        w = self.width()  # 获取窗口宽度
        h = self.height()  # 获取窗口高度
        self.slider.setFixedWidth(w / 10)  # 设置滑块固定宽度

        self.show()  # 显示窗口

    def is_Chinese(self, word):
        # 判断字符串中是否包含中文字符
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False
        

    def goGitHub(self):
        # 打开GitHub页面
        webbrowser.open('https://github.com/cycleuser/EchoRev')
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)  # 显示版本信息

    def checkVersion(self):
        # 检查版本更新
        self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)  # 显示版本信息

        url = 'https://raw.githubusercontent.com/cycleuser/EchoRev/master/echorev/__init__.py'  # 版本检查URL

        r = 0
        try:
            r = requests.get(url, allow_redirects=True)  # 发送GET请求
            r.raise_for_status()  # 检查请求状态
            NewVersion = 'self.target' + r.text.splitlines()[0]  # 获取新版本号

        except:
            # 处理连接错误
            r = 0
            buttonReply = QMessageBox.information(self, u'NetWork Error', 'You are using EchoRev ' + version)
            

        self.talk = 'You are using EchoRev ' + version + '\n' + 'released on ' + date + '\n'

        buttonReply = QMessageBox.information(self, u'Version',
                                                      self.talk)

    def Magic(self):
        # 处理文本框内容和滑块值变化
        result = ''

        slider_value = int(self.slider.value())  # 获取滑块值

        if slider_value == 0:
            self.slider_label.setText('Horizontal Reverse')  # 设置滑块标签
        elif slider_value == 1:
            self.slider_label.setText('Vertical Reverse')
        else:
            self.slider_label.setText('Traditional Chinese')

        if (self.textbox_input.toPlainText() != ''):
            str = (self.textbox_input.toPlainText())  # 获取输入文本框内容
            str_list = list(str)  # 将字符串转换为列表

            raw_list = str.split('\n')  # 按行分割字符串
            rev_list = []
            out_list = []

            if slider_value == 0:
                for i in raw_list:
                    rev_list.append(i[::-1])  # 水平反转每行字符串
            else:
                max_lenth = 0
                for i in raw_list:
                    if len(i) > max_lenth:
                        max_lenth = len(i)  # 获取最长行的长度

                for i in range(max_lenth):
                    tmp_str = ''
                    for j in raw_list:
                        try:
                            tmp_str = tmp_str + ''.join(j[i])  # 逐字符拼接
                        except(IndexError):
                            if self.is_Chinese(raw_list):
                                tmp_str = tmp_str + ''.join('\u3000')  # 中文空格
                            else:
                                tmp_str = tmp_str + ''.join('\u0020')  # 英文空格

                    if slider_value == 1:
                        out_list.append(''.join(tmp_str))  # 垂直反转
                    elif slider_value == 2:
                        out_list.append(''.join(tmp_str)[::-1])  # 传统中文反转
                    else:
                        pass

                rev_list = out_list

            for k in rev_list:
                result = result + ''.join(k) + '\n'  # 拼接结果字符串

            self.textbox_output.setText(result)  # 设置输出文本框内容
            self.statusbar.showMessage('The version is ' + version + '. Released at ' + date)  # 显示版本信息
            self.show()



    def generate_keys(self):

        if self.private_key_path != '' and  self.public_key_path != '':
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Key paths already exist and may have been loaded.")
            msg_box.setInformativeText("Do you want to continue and overwrite them?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            ret = msg_box.exec()

            if ret == QMessageBox.No:
                print("Generating new keys cancelled by the user.")
                return
            else:
                print("Generating new keys chosen by the user.")
                pass
        
        # Open a file dialog to select a directory

        print('Going to generate keys')

        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_filter = "PEM Files (*.pem);;All Files (*)"
        self.private_key_path, _ = QFileDialog.getSaveFileName(None,  "Select Private Key File", "", file_filter, options=options)
        
        if not self.private_key_path:
            print("No file selected to save private key. Exiting.")
            return

        # if os.path.exists(self.private_key_path) :
        #     # Ask the user if they want to overwrite the existing files
        #     msg_box = QMessageBox()
        #     msg_box.setIcon(QMessageBox.Warning)
        #     msg_box.setText("Key files already exist in the selected directory.")
        #     msg_box.setInformativeText("Do you want to overwrite it?")
        #     msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        #     msg_box.setDefaultButton(QMessageBox.No)
        #     ret = msg_box.exec()

        #     if ret == QMessageBox.No:
        #         print("Operation cancelled by the user.")
        #         return

        self.public_key_path, _ = QFileDialog.getSaveFileName(None, "Select Public Key File", "", file_filter, options=options)
        if not self.public_key_path:
            print("No file selected to save public key. Exiting.")
            return
        
        # Check if the key files already exist
        # if os.path.exists(self.public_key_path):
        #     # Ask the user if they want to overwrite the existing files
        #     msg_box = QMessageBox()
        #     msg_box.setIcon(QMessageBox.Warning)
        #     msg_box.setText("Key files already exist in the selected directory.")
        #     msg_box.setInformativeText("Do you want to overwrite it?")
        #     msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        #     msg_box.setDefaultButton(QMessageBox.No)
        #     ret = msg_box.exec()

        #     if ret == QMessageBox.No:
        #         print("Operation cancelled by the user.")
        #         return


        # Generate RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Serialize the private key and save to file
        with open(self.private_key_path, 'wb') as priv_file:
            priv_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Serialize the public key and save to file
        with open(self.public_key_path, 'wb') as pub_file:
            pub_file.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        QMessageBox().information(None, 'Keys Saved', f'Private key generated and saved to {self.private_key_path}\nPublic key generated and saved to {self.public_key_path}')




    def load_private_key(self):
        if self.private_key_path != '':
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Key paths already exist and may have been loaded.")
            msg_box.setInformativeText("Do you want to continue and chose new keys?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            ret = msg_box.exec()
            if ret == QMessageBox.No:
                print("Loading new keys cancelled by the user.")
                return
            else:
                print("Loading new keys chosen by the user.")
                pass
        
        print('Going to load keys')
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_filter = "PEM Files (*.pem);;All Files (*)"
        self.private_key_path, _ = QFileDialog.getOpenFileName(None,  "Select Private Key File", "", file_filter, options=options)
        if not self.private_key_path:
            print("No file selected to save private key. Exiting.")
            return
        


    def load_public_key(self):
        if self.public_key_path != '':
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Key paths already exist and may have been loaded.")
            msg_box.setInformativeText("Do you want to continue and chose new keys?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            ret = msg_box.exec()
            if ret == QMessageBox.No:
                print("Loading new keys cancelled by the user.")
                return
            else:
                print("Loading new keys chosen by the user.")
                pass
        
        print('Going to load keys')
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_filter = "PEM Files (*.pem);;All Files (*)"
        self.public_key_path, _ = QFileDialog.getOpenFileName(None, "Select Public Key File", "", file_filter, options=options)
        if not self.public_key_path:
            print("No file selected to save public key. Exiting.")
            return


    def encrypt_message(self,message):
        # 加载公钥
        # with open('public_key.pem', 'rb') as pub_file:
        with open(self.public_key_path, 'rb') as pub_file:
            public_key = serialization.load_pem_public_key(
                pub_file.read(),
            )

        # 使用公钥加密文本
        encrypted_message = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_message

    def decrypt_message(self,encrypted_message):
        # 加载私钥
        # with open('private_key.pem', 'rb') as priv_file:
        with open(self.private_key_path, 'rb') as priv_file:
            private_key = serialization.load_pem_private_key(
                priv_file.read(),
                password=None,
            )

        # 使用私钥解密文本
        decrypted_message = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_message



    def MagicCrype(self):
        if self.public_key_path == '':
            print("Public key file not found.")
            self.load_public_key()
        # 获取要加密的文本
        plaintext = self.textbox_decrypt.toPlainText()

        if not plaintext:
            print("No text to encrypt.")
            return

        # 加载公钥
        try:
            with open(self.public_key_path, 'rb') as pub_file:
                public_key = serialization.load_pem_public_key(pub_file.read(), backend=default_backend())
        except FileNotFoundError:
            print(f"Public key file not found: {self.public_key_path}")
            return

        # # 使用公钥加密文本
        # print(self.public_key_path)
        # encrypted_message = public_key.encrypt(
        #     plaintext.encode('utf-8'),
        #     padding.OAEP(
        #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
        #         algorithm=hashes.SHA256(),
        #         label=None
        #     )
        # )

        # # 将加密后的文本显示在textbox_crype
        # self.textbox_crype.setPlainText(encrypted_message.hex())
        # print("Text encrypted successfully.")

        # 分块加密
        max_length = 24 # 对于2048位RSA密钥和OAEP填充，最大输入长度约为190字节
        encrypted_chunks = []
        for i in range(0, len(plaintext), max_length):
            chunk = plaintext[i:i + max_length].encode('utf-8')
            encrypted_chunk = public_key.encrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted_chunks.append(encrypted_chunk)

        # 将所有加密的小块组合在一起
        encrypted_message = b''.join(encrypted_chunks)

        # 将加密后的文本显示在textbox_crype
        self.textbox_crype.setPlainText(encrypted_message.hex())

        print("Text encrypted successfully.")

    def MagicDecrypt(self):
        if self.private_key_path == '':
            print("Private key file not found.")
            self.load_private_key()
        # 获取要解密的密文
        encrypted_message_hex = self.textbox_crype.toPlainText()

        if not encrypted_message_hex:
            print("No text to decrypt.")
            return

        # 将十六进制字符串转换为字节
        try:
            encrypted_message = bytes.fromhex(encrypted_message_hex)
        except ValueError:
            print("Invalid hex string.")
            return

        # 加载私钥
        try:
            with open(self.private_key_path, 'rb') as priv_file:
                private_key = serialization.load_pem_private_key(priv_file.read(), password=None, backend=default_backend())
        except FileNotFoundError:
            print(f"Private key file not found: {self.private_key_path}")
            return

        # 分块解密
        max_length = 256  # 对于4096位RSA密钥和OAEP填充，最大输出长度约为512字节
        decrypted_chunks = []
        for i in range(0, len(encrypted_message), max_length):
            chunk = encrypted_message[i:i + max_length]
            try:
                decrypted_chunk = private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                decrypted_chunks.append(decrypted_chunk)
            except Exception as e:
                print(f"Decryption failed: {e}")
                return

        # 将所有解密的小块组合在一起
        decrypted_message = b''.join(decrypted_chunks)

        # 将解密后的文本显示在textbox_decrypt
        self.textbox_decrypt.setPlainText(decrypted_message.decode('utf-8'))

        print("Text decrypted successfully.")


def main():
    # 主函数
    import sys

    app = QApplication(sys.argv)  # 创建应用程序对象
    trans = QTranslator()  # 创建翻译器对象
    app.installTranslator(trans)  # 安装翻译器
    mainWin = echorev()  # 创建主窗口对象
    mainWin.show()  # 显示主窗口
    sys.exit(app.exec())  # 进入应用程序主循环

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])  # 去除脚本文件扩展名
    sys.exit(main())  # 运行主函数