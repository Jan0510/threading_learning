#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/30 23:48

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal

class MyComboBox(QComboBox):
    clicked = pyqtSignal()          #创建一个信号
    def showPopup(self):            #重写showPopup函数
        self.clicked.emit()         #发送信号
        super(MyComboBox, self).showPopup()     # 调用父类的showPopup()