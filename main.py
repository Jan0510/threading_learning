#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 20:22
from PyQt5.QtCore import pyqtSignal, QObject

import time
from datetime import datetime
import os
import sys
import threading

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QInputDialog, QLineEdit

import global_maneger
import webapi
from Bartender import Bartender
from FileSystem import FileSystem
from SerialThread import SerialThread
from testUI import Ui_Form

class MyUi(QWidget, Ui_Form, QObject):
    cv_api_signal = pyqtSignal(int)  # 输出信号，用于告知连接状态
    def __init__(self):
        super(MyUi, self).__init__()    # 分别调用了2个父类的初始化函数
        self.setupUi(self)                          # UI界面控件的初始化
        self.my_serial = SerialThread()             # 串口
        self.bartender = Bartender()                # Bartender打印引擎
        self.my_file_sys = FileSystem()             # 创建文件系统
        self.init_configure()                       # 读取配置文件完成某些用户配置
        global_maneger.global_maneger_init()        # 初始化全局变量表
        self.circle_run_active = False              # 自动运行
        self.signal_connect()  # 信号与槽函数绑定
    def __del__(self):
        self.bartender.__del__()
    # 信号与槽函数绑定
    def signal_connect(self):
        # 软件启动时列表刷新
        self.scan_printer_list_slot()
        self.scan_btwfile_list_slot()
        self.scan_port_list_slot()
        # 试打印group
        self.bnt_refreshFileList.clicked.connect(self.scan_btwfile_list_slot)
        self.bnt_tryReadFile.clicked.connect(self.try_read_file_slot)
        self.bnt_tryModifySourceContent.clicked.connect(self.try_modify_source_content_slot)
        # 用户操作group
        self.bnt_webapi_login.clicked.connect(self.mes_login_slot)
        self.bnt_push_work_order.clicked.connect(self.mes_push_work_order_slot)
        self.bnt_modify_btw_file.clicked.connect(self.mes_modify_SN_slot)
        self.bnt_startAutoRun.clicked.connect(self.circle_run_start_slot)
        self.bnt_stopAutoRun.clicked.connect(self.circle_run_stop_slot)
        self.bnt_tryPrint.clicked.connect(self.try_print_slot)
        # 串口与打印机group
        self.bnt_scanSerial.clicked.connect(self.scan_port_list_slot)               # 扫描串口
        self.bnt_openSerial.clicked.connect(self.open_port_list_slot)               # 打开串口
        self.bnt_closeSerial.clicked.connect(self.close_port_list_slot)             # 关闭串口
        self.PrintersList.clicked.connect(self.scan_printer_list_slot)              # 扫描打印机
        # 打印检测阶段group
        self.bnt_reset_print_stage.clicked.connect(self.reset_print_stage_slot)
        # 其他内部信号
        self.bartender.eventSignal.connect(self.bartender_event_slot)  # 打印引擎的事件信息
        self.btwFileList_copy.currentIndexChanged.connect(self.btwfile_changed_slot)
        self.my_serial.dataReadoutSignal.connect(self.serial_receive_slot)
        self.cv_api_signal.connect(self.cv_api_slot)
    def try_print_slot(self):
        if self.bartender.btFormat:
            nResult = self.bartender.my_print(self.PrintersList.currentText())
            if nResult == 0:
                self.my_log_print("试打印成功")
            else:
                self.my_log_print("试打印失败:\n" + str(nResult))
        else:
            self.my_log_print("试打印失败，未打开标签文件")
    def try_read_file_slot(self, filename=None):
        try:
            # 1.清空UI显示
            self.lineEdit_sourceCount.clear()
            self.SubstringList.clear()
            self.lineEdit_sourceContent.clear()

            # 2.设置btwfile，该函数会自动关闭保存旧的btw文件，然后打开新的btw文件
            if filename:
                res = self.bartender.set_btwfile_using(filename)
                self.btwFileList_copy.setCurrentText(filename)
            else:
                res = self.bartender.set_btwfile_using(self.btwFileList_copy.currentText())
            # 3.读取btw文件回显到UI
            if res:
                data_dict = self.bartender.get_data_dict()
                self.lineEdit_sourceCount.setText(str(len(data_dict)))
                for key in data_dict.keys():
                    self.SubstringList.addItem(str(key))
                self.SubstringList.setCurrentIndex(0)
                self.lineEdit_sourceContent.setText(data_dict[str(self.SubstringList.currentText())])
                self.my_log_print("试读取文件成功")
        except Exception as ex:
            print(ex)
    def try_modify_source_content_slot(self):
        try:
            data_dict = {}
            data_dict[self.SubstringList.currentText()] = str(self.lineEdit_sourceContent.text())
            self.bartender.set_data_dict(data_dict)
            self.my_log_print("完成修改数据源")
        except Exception as ex:
            print(ex)
    def scan_printer_list_slot(self):
        self.my_log_print("扫描打印机并刷新列表")
        self.PrintersList.clear()
        printers, default_printer = self.bartender.get_printer_list()
        for printer in printers:
            self.PrintersList.addItem(printer, None)
        self.PrintersList.setCurrentText(default_printer)
    def scan_btwfile_list_slot(self, targetfile=None):
        try:
            folder_path = os.getcwd()  # 获取当前路径
            file_list = os.listdir(folder_path + "\\btw\\")
            if targetfile:
                self.my_log_print("寻找："+str(targetfile)+"...")
                for file in file_list:
                    if file == targetfile:
                        self.my_log_print("已找到：" + str(targetfile) + "！")
                        return True
                return False
            if file_list:
                self.my_log_print("扫描btw文件并刷新列表")
                self.btwFileList_copy.clear()
                for file in file_list:
                    if file[-4] == "." and file[-3] == "b" and file[-2] == "t" and file[-1] == "w":
                        # 填充文件列表
                        self.btwFileList_copy.addItem(file, None)
        except Exception as ex:
            print(ex)
    def btwfile_changed_slot(self):
        # 1.清空UI显示
        try:
            self.lineEdit_sourceCount.clear()
            self.SubstringList.clear()
            self.lineEdit_sourceContent.clear()
            self.bartender.close_btwfile()
        except Exception as ex:
            print(ex)
    def scan_port_list_slot(self):   # 扫描串口并刷新列表
        port_dict = self.my_serial.scan()
        if len(port_dict):
            self.my_log_print("扫描串口并刷新列表")
            self.SerialList.clear()
            # 遍历字典
            for key, value in port_dict.items():
                self.SerialList.addItem(str(key))
    def open_port_list_slot(self):
        if not self.my_serial.alive:
            port = self.SerialList.currentText()
            baudrate = int(self.BaudrateList.currentText())
            if self.my_serial.start(port, baudrate):            # 启动2个子线程执行串口收发
                self.my_log_print("串口 "+str(port)+" 打开成功")
            else:
                self.my_log_print("串口 "+str(port)+" 打开失败")
    def close_port_list_slot(self):
        if self.my_serial.alive:
            if self.my_serial.stop():
                self.my_log_print("串口关闭成功")
            else:
                self.my_log_print("串口关闭失败")
    def serial_receive_slot(self, funccode):
        if funccode == 0xff:
            global_maneger.set_global_value('serial_connect', False)
            self.my_log_print("应答超时，已断开连接并自动关闭串口")
            if global_maneger.get_global_value('cmd_mode') > 0:
                # 停止2个子线程
                self.circle_run_active = False
                self.stage_print_active = False
                self.stage_recheck_active = False
                global_maneger.set_global_value('status_print', 0)
                global_maneger.set_global_value('status_recheck', 0)
                global_maneger.set_global_value('cmd_mode', 4)
                QMessageBox.warning(self, "应答超时", "已停止自动运行模式，请检查连接", QMessageBox.Ok)
        elif not global_maneger.get_global_value('serial_connect'):
            if funccode == 0x03:
                global_maneger.set_global_value('serial_connect', True)
                self.my_log_print("下位机已连接成功！")
    def bartender_event_slot(self, msg):
        # 监控bartender所有打印事件，当打印机打印完成后，会触发"任务发送"的事件
        self.my_log_print(msg)
        print(msg)
        # 变量status_print：0=忽略，1=启动打印，2=打印完成检测，3=检测完成待取，4=打印故障需检查的打印机
        if msg.find("发送") > 0:
            pass
    def circle_run_stop_slot(self):
        if not self.my_serial.alive:
            QMessageBox.warning(self, "下位机无连接", "请打开串口！", QMessageBox.Ok)
            return
        self.circle_run_active = False
        self.stage_print_active = False
        self.stage_recheck_active = False
        global_maneger.set_global_value('status_print', 0)
        global_maneger.set_global_value('status_recheck', 0)
        global_maneger.set_global_value('cmd_mode', 4)
        data = [0] * 3
        data[0] = global_maneger.get_global_value('status_print')
        data[1] = global_maneger.get_global_value('status_recheck')
        data[2] = global_maneger.get_global_value('cmd_mode')
        self.my_serial.serial_api_sender_stage(reg_num=3, addr=1, value=data)  # 等待串口发送
        self.my_log_print("自动运行停止...")
    def circle_run_start_slot(self):
        self.my_log_print("运行前检查...")
        if not self.my_serial.alive:
            QMessageBox.warning(self, "下位机无连接", "请打开串口！", QMessageBox.Ok)
            return
        if self.circle_run_active:
            QMessageBox.warning(self, "正在自动运行", "请不要重复启动！", QMessageBox.Ok)
            return
        if not self.scan_btwfile_list_slot(self.lineEdit_btwFileName.text()+'.btw'):
            QMessageBox.warning(self, "btw文件不存在", "请检查btw目录下的模板文件！", QMessageBox.Ok)
            return
        printer = self.PrintersList.currentText()
        if printer.find('110Xi4') == -1:
            QMessageBox.warning(self, "打印机选择有误", "请选择ZDesigner 110Xi4 600dpi！", QMessageBox.Ok)
            return
        if not global_maneger.get_global_value('serial_connect'):
            QMessageBox.warning(self, "为连接下位机", "请打开串口以连接下位机！", QMessageBox.Ok)
            return
        self.my_log_print("检查完毕，开始自动运行...")
        self.circle_run_active = True
        data = [0]*3
        data[0] = 0
        data[1] = 0
        data[2] = 1 # 0 = 忽略，1 = 自动模式，2 = 整机暂停，3 = 整机复位，4 = 整机停止
        self.my_serial.serial_api_sender_stage(reg_num=3, addr=1, value=data)  # 等待串口发送
        global_maneger.set_global_value('status_print', data[0])
        global_maneger.set_global_value('status_recheck', data[1])
        global_maneger.set_global_value('cmd_mode', data[2])
        # 启动2个线程，1个负责打印检测阶段，1个负责成品检测阶段
        self.stage_print_active = True
        self.stage_print_thread = threading.Thread(target=self.stage_print_thread_loop, daemon=True)
        self.stage_print_thread.start()
        self.stage_recheck_active = True
        self.stage_recheck_thread = threading.Thread(target=self.stage_recheck_thread_loop, daemon=True)
        self.stage_recheck_thread.start()
        self.bnt_stopAutoRun.setEnabled(True)
    def upgrade_print_status(self):
        stage_print_status = global_maneger.get_global_value('status_print')
        if stage_print_status == 0:
            self.print_stage_status.setText("忽略")
        if stage_print_status == 1:
            self.print_stage_status.setText("启动打印")
        if stage_print_status == 2:
            self.print_stage_status.setText("正在打印...")
        if stage_print_status == 3:
            self.print_stage_status.setText("打印完成待取...")
        if stage_print_status == 4:
            self.print_stage_status.setText("异常")
    def upgrade_recheck_status(self):
        stage_recheck_status = global_maneger.get_global_value('status_print')
        if stage_recheck_status == 0:
            self.recheck_stage_status.setText("忽略")
        if stage_recheck_status == 1:
            self.recheck_stage_status.setText("启动贴标质量检测")
        if stage_recheck_status == 2:
            self.recheck_stage_status.setText("正在检测...")
        if stage_recheck_status == 3:
            self.recheck_stage_status.setText("检测完成待取...")
        if stage_recheck_status == 4:
            self.recheck_stage_status.setText("异常")
    def stage_print_thread_loop(self):
        while self.circle_run_active and self.stage_print_active:
            self.upgrade_print_status()
            stage_print_status = global_maneger.get_global_value('status_print')
            # 1 打印
            if stage_print_status == 1:
                try:
                    # 1.1 检查btw中的SN与当前上位机维护的current_SN是否一致
                    self.my_log_print("打印前检查SN")
                    self.bartender.set_btwfile_using(self.lineEdit_btwFileName.text())
                    # 获取标签文件的SN，下面需要传给图像API进行检测比较
                    btw_current_SN = self.bartender.get_data_dict('num')
                    # 获取全局SN，与btw—SN进行比较检查
                    global_current_SN = global_maneger.get_global_value('current_SN')
                    # 如果btw文件里的SN与上位机维护的SN不一致，则修改btw文件内的SN
                    if btw_current_SN != global_current_SN:
                        print('btw_SN:'+str(btw_current_SN))
                        print('global_SN:'+str(global_current_SN))
                        self.bartender.set_data_dict({'num': global_current_SN})
                    # 1.2 打印，打印出来的SN是用的btw里的current_SN
                    res = self.bartender.my_print(self.PrintersList.currentText())
                    if res == 0:
                        # 1.3 打印成功后 计数器 +2
                        global_maneger.set_global_value('status_print', 2)  # 跳转到图像检测
                        self.my_serial.serial_api_sender_stage(reg_num=1, addr=1, value=2)  # 等待串口发送
                        num = global_maneger.get_global_value('print_num')
                        global_maneger.set_global_value('print_num', num + 2)
                        self.print_num.setText(str(global_maneger.get_global_value('print_num')))
                        self.my_log_print("bartender打印函数返回结果=0，打印完成")
                    else:
                        # 打印没成功时，SN不变
                        global_maneger.set_global_value('status_print', 4)      # 打印故障
                        self.my_log_print("bartender打印函数返回结果=1，打印故障")
                        self.my_serial.serial_api_sender_stage(reg_num=1, addr=1, value=4) # 等待串口发送
                        self.stage_1_active = False
                        return
                except Exception as ex:
                    print(ex)
            # 2 检测打印质量
            elif stage_print_status == 2:
                try:
                    # 2.1 SN_1与SN_2将会作为图像api的参数
                    SN_1 = global_maneger.get_global_value('current_SN')
                    # SN:EASTECH FSBB10036-0B03 YYWWKSSSSS，以空格分隔
                    SN_2 = SN_1[0: (len(SN_1) - 5)] + str(int(SN_1[(len(SN_1) - 5): len(SN_1)]) + 1).zfill(5)
                    SN_add2 = SN_1[0: (len(SN_1) - 5)] + str(int(SN_1[(len(SN_1) - 5): len(SN_1)]) + 2).zfill(5)
                    # 对变量 current_SN +2
                    global_maneger.set_global_value('current_SN', SN_add2)
                    # 2.2 调用图像API获得结果
                    self.cv_api_1(SN_1, SN_2)        # CR code打印质量
                    print("调用图像cv_api_1")
                    while not (1 == global_maneger.get_global_value('cv_api_1_res')):
                        print("cv_api_1_res= " + str(global_maneger.get_global_value('cv_api_1_res')))
                        time.sleep(0.5)
                    global_maneger.set_global_value('cv_api_1_res', 0)
                    res1 = global_maneger.get_global_value('print_res_1')
                    res2 = global_maneger.get_global_value('print_res_2')
                    self.cv_api_2()        # 获取标签偏移量
                    print("调用图像cv_api_2")
                    while not (1 == global_maneger.get_global_value('cv_api_2_res')):
                        print("cv_api_2_res= " + str(global_maneger.get_global_value('cv_api_1_res')))
                        time.sleep(0.5)
                    global_maneger.set_global_value('cv_api_2_res', 0)
                    # 2.3 更新打印检测成功、失败计数，然后显示在UI。不保存
                    self.my_log_print("打印后检测完成，现在更新打印检测成功、失败计数")
                    if res1:
                        num = global_maneger.get_global_value('print_check_OK_num')
                        global_maneger.set_global_value('print_check_OK_num', num + 1)
                        self.print_check_OK_num.setText(str(global_maneger.get_global_value('print_check_OK_num')))
                        global_maneger.get_global_value('queue_SN_1').put(SN_1)
                    else:
                        num = global_maneger.get_global_value('print_check_NG_num')
                        global_maneger.set_global_value('print_check_NG_num', num + 1)
                        self.print_check_NG_num.setText(str(global_maneger.get_global_value('print_check_NG_num')))
                    if res2:
                        num = global_maneger.get_global_value('print_check_OK_num')
                        global_maneger.set_global_value('print_check_OK_num', num + 1)
                        self.print_check_OK_num.setText(str(global_maneger.get_global_value('print_check_OK_num')))
                        global_maneger.get_global_value('queue_SN_2').put(SN_2)
                    else:
                        num = global_maneger.get_global_value('print_check_NG_num')
                        global_maneger.set_global_value('print_check_NG_num', num + 1)
                        self.print_check_NG_num.setText(str(global_maneger.get_global_value('print_check_NG_num')))
                    # 2.4 调用串口发送api，把检测结果发送给下位机
                    data = [0] * 6
                    data[0] = global_maneger.get_global_value('x_1')
                    data[1] = global_maneger.get_global_value('y_1')
                    data[2] = global_maneger.get_global_value('print_res_1')
                    data[3] = global_maneger.get_global_value('x_2')
                    data[4] = global_maneger.get_global_value('y_2')
                    data[5] = global_maneger.get_global_value('print_res_2')
                    self.my_serial.serial_api_sender_stage(reg_num=6, addr=11, value=data)  # 等待串口发送
                    global_maneger.set_global_value('status_print', 3)
                    self.my_serial.serial_api_sender_stage(reg_num=1, addr=1, value=3)  # 等待串口发送
                    print("2.3 调用串口发送api，把检测结果发送给下位机")
                except Exception as ex:
                    print(ex)
            elif stage_print_status == 3:
                print("status_print==3，待取")
                time.sleep(1)
            elif stage_print_status == 4:
                print("4 status_prink==4，异常")
                time.sleep(1)
    def stage_recheck_thread_loop(self):
        while self.circle_run_active and self.stage_recheck_active:
            self.upgrade_recheck_status()
            stage_recheck_status = global_maneger.get_global_value('status_recheck')
            if stage_recheck_status == 1:
                # 1.调用图像检测获取结果
                self.cv_api_3()
                print("1.调用图像cv_api_3")
                global_maneger.set_global_value('status_recheck', 2)
                self.my_serial.serial_api_sender_stage(reg_num=1, addr=2, value=2)  # 等待串口发送
            elif stage_recheck_status == 2:
                # 2.正在检测，等待结果
                while not (1 == global_maneger.get_global_value('cv_api_3_res')):
                    print("cv_api_3_res= " + str(global_maneger.get_global_value('cv_api_3_res')))
                    time.sleep(0.5)
                global_maneger.set_global_value('cv_api_3_res', 0)
                res1 = global_maneger.get_global_value('recheck_res_1')
                res2 = global_maneger.get_global_value('recheck_res_2')
                self.my_log_print("贴标后图像检测完成，现在更新打印检测成功、失败计数")
                # 工单与SN上传mes服务器
                if global_maneger.get_global_value('queue_SN_1').empty():
                    self.my_log_print("发生异常：SN_1队列空！")
                    global_maneger.set_global_value('status_recheck', 4)
                    self.my_serial.serial_api_sender_stage(reg_num=1, addr=2, value=4)  # 等待串口发送
                SN_1 = global_maneger.get_global_value('queue_SN_1').get()
                if global_maneger.get_global_value('queue_SN_2').empty():
                    self.my_log_print("发生异常：SN_2队列空！")
                    global_maneger.set_global_value('status_recheck', 4)
                    self.my_serial.serial_api_sender_stage(reg_num=1, addr=2, value=4)  # 等待串口发送
                SN_2 = global_maneger.get_global_value('queue_SN_2').get()
                if res1:
                    # 成品计数器+1
                    num = global_maneger.get_global_value('recheck_OK_num')
                    global_maneger.set_global_value('recheck_OK_num', num + 1)
                    self.recheck_OK_num.setText(str(num + 1))
                    # 工单目前生产量+1
                    num = global_maneger.get_global_value('SN_QTY')
                    global_maneger.set_global_value('SN_QTY', num + 1)
                    self.lineEdit_SN_QTY.setText(str(global_maneger.get_global_value('SN_QTY')))
                    if not webapi.web_post(SN_1):
                        self.my_log_print("SN_1上传mes系统失败！")
                else:
                    num = global_maneger.get_global_value('recheck_NG_num')
                    global_maneger.set_global_value('recheck_NG_num', num + 1)
                    self.print_recheck_NG_num.setText(str(global_maneger.get_global_value('recheck_NG_num')))
                    self.my_log_print("SN_1成品检测 NG +1！")
                if res2:
                    # 成品计数器+1
                    num = global_maneger.get_global_value('recheck_OK_num')
                    global_maneger.set_global_value('recheck_OK_num', num + 1)
                    self.recheck_OK_num.setText(str(global_maneger.get_global_value('recheck_OK_num')))
                    # 工单目前生产量+1
                    num = global_maneger.get_global_value('SN_QTY')
                    global_maneger.set_global_value('SN_QTY', num + 1)
                    self.lineEdit_SN_QTY.setText(str(global_maneger.get_global_value('SN_QTY')))
                    if not webapi.web_post(SN_2):
                        self.my_log_print("SN_2上传mes系统失败！")
                else:
                    num = global_maneger.get_global_value('recheck_NG_num')
                    global_maneger.set_global_value('recheck_NG_num', num + 1)
                    self.recheck_NG_num.setText(str(global_maneger.get_global_value('recheck_NG_num')))
                    self.my_log_print("SN_2成品检测 NG +1！")
                print("4.结果发送给下位机")
                data = [0] * 2
                data[0] = global_maneger.get_global_value('recheck_res_1')
                data[1] = global_maneger.get_global_value('recheck_res_2')
                self.my_serial.serial_api_sender_stage(reg_num=2, addr=17, value=data)  # 等待串口发送
                global_maneger.set_global_value('status_recheck', 3)
                self.my_serial.serial_api_sender_stage(reg_num=1, addr=2, value=3)  # 等待串口发送
            elif stage_recheck_status == 3:
                # 3.结果出来后更新计数器
                print("3 status_recheck==3，待取")
                time.sleep(1)
            elif stage_recheck_status == 4:
                print("4 status_recheck==4，异常")
                time.sleep(1)
    def my_log_print(self, text):
        self.my_log_print_thread = threading.Thread(target=self.my_log_print_thread_loop, daemon=True, args=(text,))
        self.my_log_print_thread.start()
    def my_log_print_thread_loop(self, text):
        # 获取当前时间
        now_time = datetime.now().strftime('%T') + " : "
        text = now_time + text + '\n'
        # 由于使用append追加文本显示时会自动移除以前的内容，只保留50行
        self.LogPlain.append(text)     # 显示在UI，MaximumBlockCount属性提前在QT中设为50
        self.LogPlain.moveCursor(QTextCursor.End)
        self.my_file_sys.logcat_into_file(text)   # 打印在txt文件
    # 软件启动后，读取配置文件并设置
    def init_configure(self):
        # 相关参数配置以字典形式返回
        self.my_log_print("读取配置文件并设置")
        conf_dict = self.my_file_sys.get_conf_dict("default.ini")
        if len(conf_dict) > 0:
            try:
                if conf_dict["employee_id"]:
                    self.lineEdit_employeeID.setText(conf_dict["employee_id"])
                if conf_dict["password"]:
                    self.lineEdit_password.setText(conf_dict["password"])
                if conf_dict["work_order"]:
                    self.lineEdit_workOrder.setText(conf_dict["work_order"])
            except Exception as ex:
                print(ex)
    # 软件关闭前，保存配置文件
    def save_configure(self, filename='default.ini'):
        try:
            conf_dict = {}
            conf_dict["employee_id"] = self.lineEdit_employeeID.text()
            conf_dict["password"] = self.lineEdit_password.text()
            conf_dict["work_order"] = self.lineEdit_workOrder.text()
            if self.my_file_sys.if_diff(conf_dict):
                reply = QMessageBox.question(self, '保存配置', "对config文件是否要保存修改？",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply:
                    self.my_file_sys.save_defualt_configure(conf_dict, filename)
        except Exception as ex:
            print(ex)
    # 重写app窗口关闭函数
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出', "是否要退出程序？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.save_configure()
        else:
            event.ignore()
    def mes_login_slot(self):
        # 由于登录需要时间，不能在这里等着，需要新建线程去完成
        if not global_maneger.get_global_value('mes_login'):
            self.login_thread = threading.Thread(target=self.mes_login_thread_loop)
            self.login_thread.start()
    def mes_login_thread_loop(self):
        if webapi.web_login():
            self.bnt_push_work_order.setEnabled(True)
            self.my_log_print("登录 mes 成功!")
            global_maneger.set_global_value('mes_login', True)
        else:
            self.my_log_print("登录 mes 失败!")
    def mes_push_work_order_slot(self):
        # 上传工单，由于get需要时间，不能在这里等着，需要新建线程去完成
        self.bnt_push_work_order.setDisabled(True)
        self.push_work_order_thread = threading.Thread(target=self.mes_push_work_order_thread_loop, daemon=True)
        self.push_work_order_thread.start()
    def mes_push_work_order_thread_loop(self):
        global_maneger.set_global_value('work_order', self.lineEdit_workOrder.text())
        try:
            if webapi.web_get():
                self.my_log_print("上传工单成功!")
                self.mes_init_SN()
                self.bnt_modify_btw_file.setEnabled(True)
                self.bnt_startAutoRun.setEnabled(True)
            else:
                self.my_log_print("上传工单: "+self.lineEdit_workOrder.text()+" 失败!")
            self.bnt_push_work_order.setEnabled(True)
        except Exception as ex:
            print(ex)
    def mes_init_SN(self):
        # 根据规则打开对应的btw文件
        filename = global_maneger.get_global_value('FUNCTION_NAME')
        self.lineEdit_btwFileName.setText(filename)
        self.bartender.set_btwfile_using(filename)
        # 初始化SN码，先检查mes是否有给出初始SN
        original_SN = global_maneger.get_global_value('SERIAL_NUMBER')
        ywd = datetime.now().isocalendar()  # (2020, 45, 7)tuple(年，周，日)
        y = str(ywd[0] % 100).zfill(2)
        w = str(ywd[1]).zfill(2)
        d = str(ywd[2])
        self.my_log_print("今天是 " + str(y) + " 年 " + str(w) + " 周 " + str(d) + " 日！")
        time.sleep(0.1)
        if not original_SN:     # 特殊情况1：mes没有给出初始SN，需要根据规则生成一个初始SN
            # SN模板读取出来
            SN_template = global_maneger.get_global_value('PARAME_VALUE')
            sections = SN_template.split()   # 将字符串按空格分段，返回字段列表，第一段是公司logo，第2段是产品料号
            original_SN = sections[0] + ' ' + sections[1] + ' ' + y + w + d + "00001"
            self.my_log_print("SN为空，已生成SN：" + '\n' + str(original_SN))
        else:
            sections = original_SN.split()
            sec3 = sections[2]
            if d != sec3[4]:    # 特殊情况2：mes给出初始SN，与当天的日期不符，重新开始一个SN
                new_SN = sections[0] + ' ' + sections[1] + ' ' + y + w + d + "00001"
                self.my_log_print("SN:" + original_SN + "已过期，重新生成SN：" + str(new_SN))
        # 重新生成初始SN码后，写入全局变量
        global_maneger.set_global_value('current_SN', str(new_SN))
        # 将SN码写入btw文件，以生成新的CR code
        self.bartender.set_data_dict({'num': str(new_SN)})
        # 更新到UI显示
        self.lineEdit_original_SN.setText(str(new_SN))
        time.sleep(0.1)
        self.lineEdit_TARGET_QTY.setText(str(global_maneger.get_global_value('TARGET_QTY')))
        self.lineEdit_SN_QTY.setText(str(global_maneger.get_global_value('SN_QTY')))
        self.my_log_print("SN初始化成功!")
        # 读取文件的序列化配置和副本配置
        data_dict = self.bartender.get_substring_config('num')
        self.my_log_print("SN序列化间隔为：" + str(data_dict['SerializeBy']))
        self.my_log_print("SN同一序列号使用次数：" + str(data_dict['SerializeEvery']))
        self.my_log_print("标签连续打印数量：" + str(data_dict['NumberOfSerializedLabels']))
        self.my_log_print("标签打印副本数量：" + str(data_dict['NumberOfSerializedLabels']))
    def mes_modify_SN_slot(self):
        self.bartender.set_data_dict({'num': self.lineEdit_original_SN.text()})
        global_maneger.set_global_value('current_SN', self.lineEdit_original_SN.text())
        self.my_log_print("完成修改数据源")
    def reset_print_stage_slot(self):
        global_maneger.set_global_value('status_print', 0)
        self.my_serial.serial_api_sender_stage(reg_num=1, addr=1, value=0)
    def reset_recheck_stage_slot(self):
        global_maneger.set_global_value('status_recheck', 0)
        self.my_serial.serial_api_sender_stage(reg_num=1, addr=2, value=0)
    def cv_api_slot(self, n):
        self.cv_api_signal.disconnect(self.cv_api_slot)
        if n == 1:
            text, okPressed = QInputDialog.getText(self, "打印检测结果", "输入2个0/1值，以空格分隔", QLineEdit.Normal, "1 1")
            if okPressed:
                sections = text.split()
                if len(sections) == 2:
                    global_maneger.set_global_value('print_res_1', int(sections[0]))
                    global_maneger.set_global_value('print_res_2', int(sections[1]))

                else:
                    QMessageBox.warning(self, "警告", "输入格式不符！", QMessageBox.Ok)
                    global_maneger.set_global_value('print_res_1', 1)
                    global_maneger.set_global_value('print_res_2', 1)
                global_maneger.set_global_value('cv_api_1_res', 1)
        if n == 2:
            text, okPressed = QInputDialog.getText(self, "偏移检测结果", "输入4个偏移量，以空格分隔", QLineEdit.Normal, "1 2 3 4")
            if okPressed:
                sections = text.split()
                if len(sections) == 4:
                    global_maneger.set_global_value('x_1', int(sections[0]))
                    global_maneger.set_global_value('y_1', int(sections[1]))
                    global_maneger.set_global_value('x_2', int(sections[2]))
                    global_maneger.set_global_value('y_2', int(sections[3]))
                else:
                    QMessageBox.warning(self, "警告", "输入格式不符！", QMessageBox.Ok)
                    global_maneger.set_global_value('x_1', 1)
                    global_maneger.set_global_value('y_1', 2)
                    global_maneger.set_global_value('x_2', 3)
                    global_maneger.set_global_value('y_2', 4)
                global_maneger.set_global_value('cv_api_2_res', 1)

        if n == 3:
            text, okPressed = QInputDialog.getText(self, "贴标检测结果", "输入2个0/1值，以空格分隔", QLineEdit.Normal, "1 1")
            if okPressed:
                sections = text.split()
                if len(sections) == 2:
                    global_maneger.set_global_value('recheck_res_1', int(sections[0]))
                    global_maneger.set_global_value('recheck_res_2', int(sections[1]))
                else:
                    QMessageBox.warning(self, "警告", "输入格式不符！", QMessageBox.Ok)
                    global_maneger.set_global_value('recheck_res_1', 1)
                    global_maneger.set_global_value('recheck_res_2', 1)
                    global_maneger.set_global_value('cv_api_3_res', 1)
                global_maneger.set_global_value('cv_api_3_res', 1)
        self.cv_api_signal.connect(self.cv_api_slot)
    def cv_api_1(self, s1, s2):
        self.cv_api_signal.emit(1)
    def cv_api_2(self):
        self.cv_api_signal.emit(2)
    def cv_api_3(self):
        self.cv_api_signal.emit(3)
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)  # 实例化一个应用对象，sys.argv是一组命令行参数的列表。Python可以在shell里运行，这是一种通过参数来选择启动脚本的方式。
        myshow = MyUi()
        myshow.show()
        sys.exit(app.exec_())  # 确保主循环安全退出
    except Exception as ex:
        print(ex)