#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 20:22
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

from Bartender import Bartender
from Logcat import Logcat
from SerialThread import SerialThread
from testUI import Ui_Form
folder_path = os.getcwd()  # 获取当前路径
sys.path.append(folder_path)  # 加载当前路径
class MyUi(QWidget, Ui_Form):
    def __init__(self):
        super(MyUi, self).__init__()    # 分别调用了2个父类的初始化函数
        self.setupUi(self)                          # UI界面控件的初始化
        self.my_serial = SerialThread()             # 串口
        self.bartender = Bartender()                # Bartender打印引擎
        self.my_logcat = Logcat(folder_path+"\\Logfiles\\")                   # 日志
        self.signal_connect()  # 信号与槽函数绑定
    # 信号与槽函数绑定
    def signal_connect(self):
        self.scan_btwfile_list_slot()
        self.FormatFileList.clicked.connect(self.scan_btwfile_list_slot)            # 扫描btw文件
        self.scan_printer_list_slot()
        self.PrintersList.clicked.connect(self.scan_printer_list_slot)              # 扫描打印机
        self.scan_port_list_slot()
        self.bnt_scanSerial.clicked.connect(self.scan_port_list_slot)               # 扫描串口
        self.bnt_openSerial.clicked.connect(self.open_port_list_slot)               # 打开串口
        self.bnt_closeSerial.clicked.connect(self.close_port_list_slot)             # 关闭串口
        self.bartender.eventSignal.connect(self.bartender_event_slot)  # 打印引擎的事件信息
        self.bnt_tryPrint.clicked.connect(self.tryprint_slot)
    def tryprint_slot(self):
        nResult = self.bartender.my_print()
        if nResult:
            print(str(nResult))
    def scan_printer_list_slot(self):
        printers = self.bartender.get_printer_list()
        if len(printers):
            print("扫描打印机并刷新列表")
            self.PrintersList.clear()
            for printer in printers:
                self.PrintersList.addItem(printer, None)
    def scan_btwfile_list_slot(self):
        btwdir_path = folder_path + "\\btw\\"
        file_list = os.listdir(btwdir_path)
        if file_list:
            print("扫描btw文件并刷新列表")
            self.FormatFileList.clear()
            for file in file_list:
                if file[-4] == "." and file[-3] == "b" and file[-2] == "t" and file[-1] == "w":
                    # 填充文件列表
                    self.FormatFileList.addItem(file, None)
    def change_current_btwfile_slot(self):
        # 1.修改当前btw文件名变量
        self.usingLabelFormatFile = self.FormatFileList.currentText()
        # 2.防止当前btw文件名为空
        if self.usingLabelFormatFile:
            # 3.关闭保存旧文件，防止旧文件名为空
            if self.oldbtwfile:
                if self.oldbtwfile != self.usingLabelFormatFile:
                    reply = QMessageBox.question(self, '标签文件', "对标签文件是否要保存修改？", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
                    self.bartender.set_btwfile_using(self.usingLabelFormatFile, reply)
            # 4.同步更新旧文件变量
            self.oldbtwfile = self.usingLabelFormatFile
    def scan_port_list_slot(self):   # 扫描串口并刷新列表
        port_dict = self.my_serial.scan()
        if len(port_dict):
            print("扫描串口并刷新列表")
            self.SerialList.clear()
            # 遍历字典
            for key, value in port_dict.items():
                self.SerialList.addItem(str(key))
    def open_port_list_slot(self):
        port = self.SerialList.currentText()
        baudrate = int(self.BaudrateList.currentText())
        if self.my_serial.start(port, baudrate):            # 启动2个子线程执行串口收发
            print("串口打开成功")
        else:
            print("串口打开失败")
    def close_port_list_slot(self):
        if self.my_serial.alive:
            self.my_serial.stop()
            print("串口关闭成功")
    def bartender_event_slot(self):
        pass
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)  # 实例化一个应用对象，sys.argv是一组命令行参数的列表。Python可以在shell里运行，这是一种通过参数来选择启动脚本的方式。
        myshow = MyUi()
        myshow.show()
        sys.exit(app.exec_())  # 确保主循环安全退出
    except Exception as ex:
        print(ex)