#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 20:22
from datetime import datetime
import os
import sys
import threading

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

import global_maneger
import webapi
from Bartender import Bartender
from FileSystem import FileSystem
from SerialThread import SerialThread
from testUI import Ui_Form

class MyUi(QWidget, Ui_Form):
    def __init__(self):
        super(MyUi, self).__init__()    # 分别调用了2个父类的初始化函数
        self.setupUi(self)                          # UI界面控件的初始化
        self.my_serial = SerialThread()             # 串口
        self.bartender = Bartender()                # Bartender打印引擎
        self.my_file_sys = FileSystem()
        self.init_configure()
        self.signal_connect()  # 信号与槽函数绑定
    # 信号与槽函数绑定
    def signal_connect(self):
        self.scan_printer_list_slot()
        self.scan_btwfile_list_slot()
        self.bnt_refreshFileList.clicked.connect(self.scan_btwfile_list_slot)
        self.bnt_tryReadFile.clicked.connect(self.try_read_file_slot)
        self.bnt_tryModifySourceContent.clicked.connect(self.try_modify_source_content_slot)
        self.bnt_webapi_login.clicked.connect(self.mes_login_slot)
        self.bnt_webapi_get.clicked.connect(self.mes_get_SN_slot)
        self.bnt_modify_btw_file.clicked.connect(self.mes_modify_SN_slot)

        self.bnt_startAutoRun.clicked.connect(self.circle_run_stop_slot)
        self.bnt_stopAutoRun.clicked.connect(self.circle_run_stop_slot)
        self.bnt_tryPrint.clicked.connect(self.try_print_slot)
        self.bnt_scanSerial.clicked.connect(self.scan_port_list_slot)               # 扫描串口
        self.bnt_openSerial.clicked.connect(self.open_port_list_slot)               # 打开串口
        self.bnt_closeSerial.clicked.connect(self.close_port_list_slot)             # 关闭串口
        self.PrintersList.clicked.connect(self.scan_printer_list_slot)              # 扫描打印机
        self.bartender.eventSignal.connect(self.bartender_event_slot)  # 打印引擎的事件信息
        self.FormatFileList.currentIndexChanged.connect(self.btwfile_changed_slot)
    def try_print_slot(self):
        nResult = self.bartender.my_print(self.PrintersList.currentText(), self.FormatFileList.currentText())
        if nResult == 0:
            self.my_log_print("试打印成功")
        else:
            self.my_log_print("试打印失败:\n" + str(nResult))
    def try_read_file_slot(self, filename=None):
        # 1.清空UI显示
        self.lineEdit_sourceCount.clear()
        self.SubstringList.clear()
        self.lineEdit_sourceContent.clear()

        # 2.设置btwfile，该函数会自动关闭保存旧的btw文件，然后打开新的btw文件
        if filename:
            res = self.bartender.set_btwfile_using(filename)
            self.FormatFileList.setCurrentText(filename)
        else:
            res = self.bartender.set_btwfile_using(self.FormatFileList.currentText())
        # 3.读取btw文件回显到UI
        if res:
            data_dict = self.bartender.get_data_dict()
            self.lineEdit_sourceCount.setText(str(len(data_dict)))
            for key in data_dict.keys():
                self.SubstringList.addItem(str(key))
            self.SubstringList.setCurrentIndex(1)
            self.lineEdit_sourceContent.setText(data_dict[str(self.SubstringList.currentText())])
            self.my_log_print("试读取文件成功")
    def try_modify_source_content_slot(self):
        data_dict = {}
        data_dict[self.SubstringList.currentText()] = int(self.lineEdit_sourceContent.text())
        self.bartender.set_data_dict(data_dict)
        self.my_log_print("完成修改数据源")
    def scan_printer_list_slot(self):
        printers, default_printer = self.bartender.get_printer_list()
        self.PrintersList.setCurrentText(default_printer)
        if len(printers):
            self.my_log_print("扫描打印机并刷新列表")
            self.PrintersList.clear()
            for printer in printers:
                self.PrintersList.addItem(printer, None)
    def scan_btwfile_list_slot(self):
        folder_path = os.getcwd()  # 获取当前路径
        file_list = os.listdir(folder_path + "\\btw\\")
        if file_list:
            self.my_log_print("扫描btw文件并刷新列表")
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
        self.bartender.close_btwfile()
    def scan_port_list_slot(self):   # 扫描串口并刷新列表
        port_dict = self.my_serial.scan()
        if len(port_dict):
            self.my_log_print("扫描串口并刷新列表")
            self.SerialList.clear()
            # 遍历字典
            for key, value in port_dict.items():
                self.SerialList.addItem(str(key))
    def open_port_list_slot(self):
        port = self.SerialList.currentText()
        baudrate = int(self.BaudrateList.currentText())
        if self.my_serial.start(port, baudrate):            # 启动2个子线程执行串口收发
            self.my_log_print("串口 "+str(port)+" 打开成功")
        else:
            self.my_log_print("串口 "+str(port)+" 打开失败")
    def close_port_list_slot(self):
        if self.my_serial.alive:
            self.my_serial.stop()
            self.my_log_print("串口关闭成功")
    def bartender_event_slot(self, msg):
        self.my_log_print(msg)
        if msg.find("发送") > 0:
            pass
            # 打印成功计数+1
        else:
            pass
            # 打印失败
    def circle_run_stop_slot(self):
        pass
    def circle_run_start_slot(self):
        pass
    def my_log_print(self, text):
        # 获取当前时间
        now_time = datetime.now().strftime('%T') + " : "
        text = now_time + text + '\n'
        # 由于使用append追加文本显示时会自动移除以前的内容，只保留50行
        self.LogPlain.append(text)     # 显示在UI，MaximumBlockCount属性提前在QT中设为50
        self.my_file_sys.logcat_into_file(text)   # 打印在txt文件
    # 软件启动后，读取配置文件并设置
    def init_configure(self):
        # 相关参数配置以字典形式返回
        self.my_log_print("读取配置文件并设置")
        self.conf_dict = self.my_file_sys.get_conf_dict("default.ini")
        if len(self.conf_dict) > 0:
            try:
                if self.conf_dict["employee_id"]:
                    self.lineEdit_employeeID.setText(self.conf_dict["employee_id"])
                if self.conf_dict["password"]:
                    self.lineEdit_password.setText(self.conf_dict["password"])
                if self.conf_dict["work_order"]:
                    self.lineEdit_workOrder.setText(self.conf_dict["work_order"])
            except Exception as ex:
                print(ex)

    # 软件关闭前，保存配置文件
    def save_configure(self):
        self.my_log_print("软件关闭前保存配置文件")
        try:
            self.conf_dict["employee_id"] = self.lineEdit_employeeID.text()
            self.conf_dict["password"] = self.lineEdit_password.text()
            self.conf_dict["work_order"] = self.lineEdit_workOrder.text()

            self.my_file_sys.save_defualt_configure(self.conf_dict, "default.ini")
        except Exception as ex:
            print(ex)
    # 重写app窗口关闭函数
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出', "是否要退出程序？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            reply = QMessageBox.question(self, '保存配置', "对config文件是否要保存修改？", QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save_configure()
        else:
            event.ignore()

    def mes_login_slot(self):
        # 由于登录需要时间，不能在这里等着，需要新建线程去完成
        self.login_thread = threading.Thread(target=self.mes_login_thread_loop)
        self.login_thread.start()
    def mes_login_thread_loop(self):
        if webapi.web_login():
            self.bnt_webapi_get.setEnabled(True)
            self.my_log_print("登录 mes 成功!")
        else:
            self.my_log_print("登录 mes 失败!")
    def mes_get_SN_slot(self):
        # 上传工单，由于get需要时间，不能在这里等着，需要新建线程去完成
        self.get_SN_thread = threading.Thread(target=self.mes_get_SN_thread_loop)
        self.get_SN_thread.start()

    def mes_get_SN_thread_loop(self):
        global_maneger.set_global_value('work_order', self.lineEdit_workOrder.text())
        if webapi.web_get():
            self.my_log_print("上传工单成功!")
            self.mes_init_SN()
            self.bnt_modify_btw_file.setEnabled(True)
            self.bnt_startAutoRun.setEnabled(True)
        else:
            self.my_log_print("上传工单失败!")

    def mes_init_SN(self):
        # 根据规则打开对应的btw文件
        filename = global_maneger.get_global_value('FUNCTION_NAME')
        self.lineEdit_btwFileName.setText(filename)
        self.bartender.set_btwfile_using(filename)
        # 初始化SN码，先检查mes是否有给出初始SN
        original_SN = global_maneger.get_global_value('SERIAL_NUMBER')
        if not original_SN:# 特殊情况：mes没有给出初始SN，需要根据规则生成一个初始SN
            # SN模板读取出来
            SN_template = global_maneger.get_global_value('PARAME_VALUE')
            list = SN_template.split()   # 将字符串按空格分段，返回字段列表，第一段是公司logo，第2段是产品料号
            ywd = datetime.now().isocalendar()  # (2020, 45, 7)tuple(年，周，日)
            y = str(ywd[0]%100).zfill(2)
            w = str(ywd[1]).zfill(2)
            d = str(ywd[2])
            original_SN = list[0] + ' ' + list[1] + ' ' + y + w + d + "00001"

        self.lineEdit_original_SN.setText(str(original_SN))
        self.lineEdit_TARGET_QTY.setText(str(global_maneger.get_global_value('TARGET_QTY')))
        self.lineEdit_SN_QTY.setText(str(global_maneger.get_global_value('SN_QTY')))

    def mes_modify_SN_slot(self):
        data_dict = {}
        data_dict['num'] = int(self.lineEdit_original_SN.text())
        self.bartender.set_data_dict(data_dict)
        self.my_log_print("完成修改数据源")


    def first_stage(self):
        pass
        # 0.接受串口指令启动打印
        # 1.打印
        # 2.调用图像检测获取结果
        # 3.偏移结果传给串口


    def second_stage(self):
        pass
        # 0.接受串口指令启动贴标后检测
        # 1.调用图像检测获取结果
        # 2.结果传给串口
        # 3.结果传给服务器

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)  # 实例化一个应用对象，sys.argv是一组命令行参数的列表。Python可以在shell里运行，这是一种通过参数来选择启动脚本的方式。
        myshow = MyUi()
        myshow.show()
        sys.exit(app.exec_())  # 确保主循环安全退出
    except Exception as ex:
        print(ex)