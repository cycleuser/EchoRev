# EchoRev

a GUI tool to help you reverse your input text.

这个小工具是让你可以正常从左往右输入，然后文字变成从右往左的。就是为了玩。

![](https://raw.githubusercontent.com/cycleuser/EchoRev/master/img/GUI.png)

## Installation and Usage


```Bash
pip install requests
pip install pyside6
pip install cryptography
pip install echorev 
python -c "import echorev;echorev.main()"
```

OR adding `--user` to avoid the `EnvironmentError`

```Bash
pip install requests --user 
pip install pyqt5.sip --user     
pip install pyqt5 --user  
pip install echorev --user  
python -c "import echorev;echorev.main()"
```