#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 23:41

from Seagull.BarTender.Print import Engine, Printers, Printer, LabelFormatDocument, Messages, Message, SaveOptions

class Bartender():
    def __init__(self):
        # self.btEngine = Engine(True)            # 创建 BarTender 的 Engine，参数True代表创建时自动调用Start函数
        self.btEngine = Engine()
        self.printers = Printers()
    def get_printer_list(self):
        pass
    def get_

