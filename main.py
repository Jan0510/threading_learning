#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 20:22
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

class MyUi(QWidget, Ui_Form):
    def __init__(self):
        super(MyUi, self).__init__()    # 分别调用了2个父类的初始化函数
        self.setupUi(self)                          # UI界面控件的初始化
        self.my_serial = SerialThread()             # 串口
        self.bartender = Bartender()                # Bartender打印引擎
        self.my_file_sys = FileSystem()             # 创建文件系统
        self.init_configure()                       # 读取配置文件完成某些用户配置
        global_maneger.global_maneger_init()        # 初始化全局变量表
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
            self.btwFileList_copy.clear()
            for file in file_list:
                if file[-4] == "." and file[-3] == "b" and file[-2] == "t" and file[-1] == "w":
                    # 填充文件列表
                    self.btwFileList_copy.addItem(file, None)
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
        elif not global_maneger.get_global_value('serial_connect'):
            global_maneger.set_global_value('serial_connect', True)
            self.my_log_print("下位机已连接成功！")

        # 将串口返回的状态数据回显到UI上
    def bartender_event_slot(self, msg):
        # 监控bartender所有打印事件，当打印机打印完成后，会触发"任务发送"的事件
        self.my_log_print(msg)
        # 变量status_print：0=忽略，1=启动打印，2=打印完成检测，3=检测完成待取，4=打印故障需检查的打印机
        if msg.find("发送") > 0:
            pass
    def circle_run_stop_slot(self):
        self.stage_print_active = False
        self.stage_recheck_active = False
        global_maneger.set_global_value('cmd_mode', 4)
    def circle_run_start_slot(self):
        self.my_log_print("运行前检查...")
        printer = self.PrintersList.currentText()
        if printer.find('110Xi4') == -1:
            QMessageBox.warning(self, "打印机选择有误", "请选择ZDesigner 110Xi4 600dpi！", QMessageBox.Ok)
            return
        if not global_maneger.get_global_value('serial_connect'):
            QMessageBox.warning(self, "为连接下位机", "请打开串口以连接下位机！", QMessageBox.Ok)
            return
        # 0 = 忽略，1 = 自动模式，2 = 整机暂停，3 = 整机复位，4 = 整机停止
        if global_maneger.get_global_value('cmd_mode') != 1:
            global_maneger.set_global_value('cmd_mode', 1)
            # 启动2个线程，1个负责打印检测阶段，1个负责成品检测阶段
            self.stage_print_active = True
            self.stage_print_thread = threading.Thread(target=self.stage_print_thread_loop, daemon=True)
            self.stage_print_thread.start()
            self.stage_recheck_active = True
            self.stage_recheck_thread = threading.Thread(target=self.stage_recheck_thread_loop, daemon=True)
            self.stage_recheck_thread.start()
    def stage_print_thread_loop(self):
        # 该子线程借助全局变量与主线程交互
        while global_maneger.get_global_value('cmd_mode') == 1 and self.stage_print_active:
            # 获取步骤号,0 = 忽略，1 = 启动打印，2 = 打印完成开始图像检测，3 = 检测完成待取，4 = 打印故障需检查的打印机
            stage_print_status = global_maneger.get_global_value('status_print')
            # 1 打印
            if stage_print_status == 1:
                # 1.1 检查btw中的SN与当前上位机维护的current_SN是否一致
                self.my_log_print("打印前检查SN")
                self.bartender.set_btwfile_using(self.lineEdit_btwFileName.text())
                # 获取标签文件的SN，下面需要传给图像API进行检测比较
                btw_current_SN = self.bartender.get_data_dict('num')
                # 获取全局SN，与btw—SN进行比较检查
                self.global_current_SN = global_maneger.get_global_value('current_SN')
                if btw_current_SN != self.global_current_SN:
                    QMessageBox.warning(self, 'SN不一致', 'btw_SN与global_SN不一致', QMessageBox.Ok)
                    print('btw_SN:'+str(btw_current_SN))
                    print('global_SN:'+str(self.global_current_SN))
                    return
                # 1.2 SN检查无误后，自增1。global_current_SN与global_current_SN_1将会作为图像api的参数。
                sections = self.global_current_SN.split()    # SN:EASTECH FSBB10036-0B03 YYWWKSSSSS，以空格分隔
                self.global_current_SN_1 = sections[0]+' '+sections[1]+' '+str(int(sections[2]) + 1)

                # 1.3 自增2后更新global_current_SN，该SN码是下一次打印的SN码
                # btw_current_SN会在打印后由bartend.exe自增，所以只需要维护global_SN
                self.global_current_SN = sections[0]+' '+sections[1]+' '+str(int(sections[2]) + 2)
                global_maneger.set_global_value('current_SN', str(self.global_current_SN))
                # 1.4 打印，打印出来的SN是用的btw里的current_SN
                res = self.bartender.my_print(self.PrintersList.currentText())
                if res == 0:
                    global_maneger.set_global_value('status_print', 2)  # 跳转到图像检测
                    num = global_maneger.get_global_value('print_num')
                    global_maneger.set_global_value('print_num', num + 2)
                    self.print_num.setText(num)
                    self.my_log_print("bartender打印函数返回结果=0，打印完成")
                else:
                    global_maneger.set_global_value('status_print', 4)      # 打印故障
                    self.my_log_print("bartender打印函数返回结果=1，打印故障")
                    self.my_serial.serial_api_sender_stage(reg_num=1, addr=1, value=4) # 等待串口发送
                    # 打印故障，向用户提示需检查的打印机，UI显示打印检测阶段的状态
                    QMessageBox.warning(self, '打印故障', '请先点击 ‘停止’ 按钮，再检查打印机', QMessageBox.Ok)
                    self.stage_1_active = False
                    return
            # 2 图像检测打印质量
            elif stage_print_status == 2:
                # 2.1 调用图像API获得结果
                if not self.cv_api_1():         # CR code打印质量
                    return
                res1 = global_maneger.get_global_value('print_res_1')
                res2 = global_maneger.get_global_value('print_res_2')
                if not self.cv_api_2():         # 获取标签偏移量
                    return

                data[0] = global_maneger.get_global_value()
                data[1] = global_maneger.get_global_value()
                data[2] = global_maneger.get_global_value()
                data[3] = global_maneger.get_global_value()
                data[4] = global_maneger.get_global_value()
                data[5] = global_maneger.get_global_value()
                # 2.2 更新打印检测成功、失败计数，然后显示在UI。不保存
                self.my_log_print("图像检测完成，更新打印检测成功、失败计数")
                if res1 and res1:
                    num = global_maneger.get_global_value('print_check_OK_num')
                    global_maneger.set_global_value('print_check_OK_num', num + 2)
                    self.print_check_OK_num.setText(num)
                elif res1 or res2:
                    num = global_maneger.get_global_value('print_check_OK_num')
                    global_maneger.set_global_value('print_check_OK_num', num + 1)
                    self.print_check_OK_num.setText(num)
                    num = global_maneger.get_global_value('print_check_NG_num')
                    global_maneger.set_global_value('print_check_NG_num', num + 1)
                    self.print_check_NG_num.setText(num)
                else:
                    num = global_maneger.get_global_value('print_check_NG_num')
                    global_maneger.set_global_value('print_check_NG_num', num + 2)
                    self.print_check_NG_num.setText(num)
                # 2.3 调用串口发送api，把检测结果发送给下位机
                global_maneger.set_global_value('status_print', 3)
                self.my_serial.serial_api_sender_stage(reg_num=1, addr=1, value=3)    # 等待串口发送
                self.my_serial.serial_api_sender_stage(reg_num=6, addr=11, value=data)  # 等待串口发送

    def stage_recheck_thread_loop(self):
        while global_maneger.get_global_value('cmd_mode')==1 and self.stage_recheck_active:
            stage_recheck_status = global_maneger.get_global_value('status_recheck')
            # 0=忽略，1=启动成品检查，2=检查完成待取
            if stage_recheck_status == 1:
                res1, res2 = self.cv_api_3()
                # 更新计数
                global_maneger.set_global_value('recheck_res_1', res1)
                global_maneger.set_global_value('recheck_res_2', res2)
                global_maneger.set_global_value('status_recheck', 2)
                self.call_serial_sender_api('recheck')  # 等待串口发送
        # 0.接受串口指令启动贴标后检测
        # 1.调用图像检测获取结果
        # 2.结果传给串口
        # 3.结果传给服务器
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
                original_SN = sections[0] + ' ' + sections[1] + ' ' + y + w + d + "00001"
                self.my_log_print("SN已过期，重新生成SN：" + str(original_SN))
        # 重新生成初始SN码后，写入全局变量
        global_maneger.set_global_value('current_SN', str(original_SN))
        # 将SN码写入btw文件，以生成新的CR code
        self.bartender.set_data_dict({'num': str(original_SN)})
        # 更新到UI显示
        self.lineEdit_original_SN.setText(str(original_SN))
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
        data_dict = {}
        data_dict['num'] = int(self.lineEdit_original_SN.text())
        self.bartender.set_data_dict(data_dict)
        self.my_log_print("完成修改数据源")
    def reset_print_stage_slot(self):
        global_maneger.set_global_value('status_print', 0)
        self.my_serial.serial_api_sender_stage(reg_num=1, addr=1, value=0)
    def cv_api_1(self):
        while True:
            text, okPressed = QInputDialog.getText(self, "打印检测结果", "输入2个0/1值，以空格分隔", QLineEdit.Normal, "1 1")
            if okPressed:
                sections = text.split()
                if len(sections) == 2:
                    global_maneger.set_global_value('print_res_1', bool(sections[0]))
                    global_maneger.set_global_value('print_res_2', bool(sections[1]))
                    return True
                QMessageBox.warning(self, "警告", "输入格式不符！", QMessageBox.Ok)
    def cv_api_2(self):
        while True:
            text, okPressed = QInputDialog.getText(self, "偏移检测结果", "输入4个偏移量，以空格分隔", QLineEdit.Normal, "1 2 3 4")
            if okPressed:
                sections = text.split()
                if len(sections) == 4:
                    global_maneger.set_global_value('x_1', int(sections[0]))
                    global_maneger.set_global_value('y_1', int(sections[1]))
                    global_maneger.set_global_value('x_2', int(sections[2]))
                    global_maneger.set_global_value('y_1', int(sections[3]))
                    return True
                QMessageBox.warning(self, "警告", "输入格式不符！", QMessageBox.Ok)

    def cv_api_3(self):
        return True, True
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)  # 实例化一个应用对象，sys.argv是一组命令行参数的列表。Python可以在shell里运行，这是一种通过参数来选择启动脚本的方式。
        myshow = MyUi()
        myshow.show()
        sys.exit(app.exec_())  # 确保主循环安全退出
    except Exception as ex:
        print(ex)