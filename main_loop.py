#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 20:22
import datetime
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
        self.oldbtwfile = None
    # 信号与槽函数绑定
    def signal_connect(self):
        self.scan_printer_list_slot()
        self.scan_btwfile_list_slot()
        self.read_file_slot()
        self.bnt_refreshFileList.clicked.connect(self.scan_btwfile_list_slot)
        self.bnt_readFile.clicked.connect(self.read_file_slot)
        self.bnt_sourceContentModify.clicked.connect(self.source_modify_slot)
        self.bnt_Start.clicked.connect(self.circle_run_start)
        self.bnt_Stop.clicked.connect(self.circle_run_stop)
        self.bnt_tryPrint.clicked.connect(self.try_print_slot)
        self.bnt_scanSerial.clicked.connect(self.scan_port_list_slot)               # 扫描串口
        self.bnt_openSerial.clicked.connect(self.open_port_list_slot)               # 打开串口
        self.bnt_closeSerial.clicked.connect(self.close_port_list_slot)             # 关闭串口
        self.PrintersList.clicked.connect(self.scan_printer_list_slot)              # 扫描打印机
        self.bartender.eventSignal.connect(self.bartender_event_slot)  # 打印引擎的事件信息
        self.FormatFileList.currentIndexChanged.connect(self.btwfile_changed_slot)
    def try_print_slot(self):
        btw_file_path = folder_path + "\\btw\\" + self.FormatFileList.currentText()
        self.bartender.set_btwfile_using(btw_file_path)
        nResult = self.bartender.my_print(self.PrintersList.currentText())
        if nResult == 0:
            print("打印成功")
        else:
            print("打印失败")
    def scan_printer_list_slot(self):
        printers, default_printer = self.bartender.get_printer_list()
        self.PrintersList.setCurrentText(default_printer)
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
    def btwfile_changed_slot(self):
        # 1.清空UI显示
        self.lineEdit_sourceCount.clear()
        self.SubstringList.clear()
        self.lineEdit_sourceContent.clear()
    def read_file_slot(self):
        # 1.清空UI显示
        self.lineEdit_sourceCount.clear()
        self.SubstringList.clear()
        self.lineEdit_sourceContent.clear()

        # 2.设置btwfile，该函数会自动关闭保存旧的btw文件，然后打开新的btw文件
        btw_file_path = folder_path+"\\btw\\"+self.FormatFileList.currentText()
        res = self.bartender.set_btwfile_using(btw_file_path)

        # 3.读取btw文件回显到UI
        if res:
            data_dict = self.bartender.get_data_dict()
            self.lineEdit_sourceCount.setText(str(len(data_dict)))
            for key in data_dict.keys():
                self.SubstringList.addItem(str(key))
            self.lineEdit_sourceContent.setText(data_dict[str(self.SubstringList.currentText())])

    def source_modify_slot(self):
        data_dict = {}
        data_dict[self.SubstringList.currentText()] = int(self.lineEdit_sourceContent.text())
        self.bartender.set_data_dict(data_dict)
    def scan_port_list_slot(self):   # 扫描串口并刷新列表
        port_dict = self.my_serial.scan()
        if len(port_dict):
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
    def bartender_event_slot(self, msg):
        print(msg)
        self.my_log_print(self)
    def circle_run_stop(self):
        pass
    def circle_run_start(self):
        pass
    def my_log_print(self, text):
        # 获取当前时间
        now_time = datetime.datetime.now().strftime('%T') + " : "
        text = now_time + text + '\n'
        self.LogPlain.insertPlainText(text)     # 显示在UI
        self.my_logcat.logcat_into_file(text)   # 存在txt文件
        if self.Log.blockCount() > 20:
            self.Log.clear()
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)  # 实例化一个应用对象，sys.argv是一组命令行参数的列表。Python可以在shell里运行，这是一种通过参数来选择启动脚本的方式。
        myshow = MyUi()
        myshow.show()
        sys.exit(app.exec_())  # 确保主循环安全退出
    except Exception as ex:
        print(ex)