#!/usr/bin/env python
#coding:utf-8
import os
from distutils.core import setup
from echorev import *


here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.md')).read()
except:
    README = 'https://github.com/cycleuser/EchoRev/blob/master/README.md'


setup(name='echorev',
      version=version,
      description='a GUI tool to help you reverse your input text',
      longdescription=README,
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='https://github.com/cycleuser/EchoRev',
      packages=['echorev'],
      package_data={
          'echorev': ['*.py','*.png','*.qm','*.ttf','*.ini','*.md'],
      },
      include_package_data=True,


      install_requires=[
                        'PySide6',
                        'cryptography'
                         ],
     )