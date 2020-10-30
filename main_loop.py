#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 20:22
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from SerialThread import SerialThread
from testUI import Ui_Form

class MyUi(QWidget, Ui_Form):
    def __init__(self):
        super(MyUi, self).__init__()    # 分别调用了2个父类的初始化函数
        # UI界面控件的初始化
        self.setupUi(self)
        self.my_serial = SerialThread()             # 串口
        self.signal_connect()                       # 信号与槽函数绑定
    # 信号与槽函数绑定
    def signal_connect(self):
        self.bnt_scanSerial.clicked.connect(self.scan_port_list)            # 扫描串口
        self.bnt_openSerial.clicked.connect(self.open_port_list)            # 打开串口
        self.bnt_closeSerial.clicked.connect(self.close_port_list)           # 关闭串口

    def scan_port_list(self):   # 扫描串口并刷新列表
        print("扫描串口并刷新列表")
        port_dict = self.my_serial.scan()
        if len(port_dict) == 0:
            print("没有串口")
            return False
        self.SerialList.clear()
        # 遍历字典
        for key, value in port_dict.items():
            self.SerialList.addItem(str(key))
    def open_port_list(self):
        port = self.SerialList.currentText()
        baudrate = int(self.BaudrateList.currentText())
        if self.my_serial.start(port, baudrate):            # 启动2个子线程执行串口收发
            print("串口打开成功")
        else:
            print("串口打开失败")
    def close_port_list(self):
        if self.my_serial.alive:
            self.my_serial.stop()
            print("串口关闭成功")
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)  # 实例化一个应用对象，sys.argv是一组命令行参数的列表。Python可以在shell里运行，这是一种通过参数来选择启动脚本的方式。
        myshow = MyUi()
        myshow.show()
        sys.exit(app.exec_())  # 确保主循环安全退出
    except Exception as ex:
        print(ex)