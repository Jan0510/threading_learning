#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 23:41
import os
import sys
import clr
from PyQt5.QtCore import pyqtSignal, QObject

FolderPath = os.getcwd()  # 获取当前路径
sys.path.append(FolderPath)  # 加载当前路径
clr.FindAssembly("Seagull.BarTender.Print.dll")
clr.AddReference("Seagull.BarTender.Print")
# clr.FindAssembly("mscorlib.dll")
# clr.AddReference("mscorlib")
from Seagull.BarTender.Print import Engine, Printers, Printer, LabelFormatDocument, Messages, Message, SaveOptions
from System import EventHandler
class Bartender(QObject):
    eventSignal = pyqtSignal(str)  # 输出信号，用于告知调用者，发送和接受情况
    def __init__(self):
        super(Bartender, self).__init__()
        self.btEngine = Engine(True)            # 创建 BarTender 的 Engine，参数True代表创建时自动调用Start函数
        # EventHandler 来自 System，在C#中EventHandler其实是一个模板，由于在python里面不用声明类型所以直接使用了模板
        self.btEngine.JobCancelled += EventHandler(self.btEngine_JobCancelledSlot)
        self.btEngine.JobErrorOccurred += EventHandler(self.btEngine_JobErrorOccurredSlot)
        self.btEngine.JobMonitorErrorOccurred += EventHandler(self.btEngine_JobMonitorErrorOccurredSlot)
        self.btEngine.JobPaused += EventHandler(self.btEngine_JobPausedSlot)
        self.btEngine.JobQueued += EventHandler(self.btEngine_JobQueuedSlot)
        self.btEngine.JobRestarted += EventHandler(self.btEngine_JobRestartedSlot)
        self.btEngine.JobResumed += EventHandler(self.btEngine_JobResumedSlot)
        self.btEngine.JobSent += EventHandler(self.btEngine_JobSentSlot)
        self.btFormat = None
        self.btwfile_using = None
    def __del__(self):
        if self.btEngine.IsAlive:
            # 停止引擎
            self.btEngine.Stop()
            # 释放资源
            self.btEngine.Dispose()
    # 返回打印机列表[]
    def get_printer_list(self):
        printers = Printers()  # 获取打印机列表
        printer_list = []
        for printer in printers:
            printer_list.append(printer.PrinterName)
        printer_list.append(printers.Default.PrinterName)      # 最后再补充一个默认打印机
        return printer_list, printers.Default.PrinterName
    def get_data_dict(self, key=None):
        data_dict = {}
        if self.btFormat:
            if key:
                return self.btFormat.SubStrings[key].Value
            for substring in self.btFormat.SubStrings:
                data_dict[substring.Name] = substring.Value
        return data_dict
    def set_data_dict(self, data_dict):
        if len(data_dict) and self.btFormat:
            for key, value in data_dict.items():
                for substring in self.btFormat.SubStrings:
                    if substring.Name == key:
                        self.btFormat.SubStrings.SetSubString(key, value)
    def get_substring_config(self, substring):
        data_dict = {}
        if self.btFormat:
            # Substring类
            data_dict['SerializeBy'] = self.btFormat.SubStrings[substring].SerializeBy  # 返回str
            data_dict['SerializeEvery'] = self.btFormat.SubStrings[substring].SerializeEvery  # 返回str
            # PrintSetup类
            data_dict['NumberOfSerializedLabels'] = self.btFormat.PrintSetup.NumberOfSerializedLabels
            data_dict['IdenticalCopiesOfLabel'] = self.btFormat.PrintSetup.IdenticalCopiesOfLabel
        return data_dict
    def set_substring_config(self, substring, data_dict):
        if self.btFormat:
            # Substring类
            self.btFormat.SubStrings[substring].SerializeBy = data_dict['SerializeBy']
            self.btFormat.SubStrings[substring].SerializeEvery = data_dict['SerializeEvery']
            # PrintSetup类
            self.btFormat.PrintSetup.NumberOfSerializedLabels = data_dict['NumberOfSerializedLabels']
            self.btFormat.PrintSetup.IdenticalCopiesOfLabel = data_dict['IdenticalCopiesOfLabel']
            return True
        return False
    def set_btwfile_using(self, new_btwfile_name):
        # 不能重复打开
        if new_btwfile_name and self.btwfile_using == new_btwfile_name:
            return True
        # 关闭并保存旧文件，打开新文件
        try:
            new_file_path = FolderPath + "\\btw\\" + new_btwfile_name
            if self.btFormat:
                self.btFormat.Close(SaveOptions.SaveChanges)
            self.btFormat = self.btEngine.Documents.Open(new_file_path)
            self.btwfile_using = new_btwfile_name
            return True
        except Exception as ex:
            print(ex)
            return False
    def close_btwfile(self):
        if self.btFormat:
            self.btFormat.Close(SaveOptions.SaveChanges)
    def my_print(self, printer):             # 返回nResult，0=成功，1=失败
        # 判断bartender是否启动
        if self.btEngine.IsAlive:
            pass
        else:
            self.btEngine.Start()
        btMessages = Messages()                 # 打印返回的消息
        waitForCompletionTimeout = 100          # 打印超时定时器 ms
        try:                                    # 开始打印
            self.btFormat.PrintSetup.PrinterName = printer
            # 调用库的打印函数，将数据推入打印队列
            nResult = self.btFormat.Print("printjob", waitForCompletionTimeout, btMessages)
            return int(nResult)                      # 0=成功，1=失败
        except Exception as ex:
            print(ex)
            return 1
    # 任务发送时触发
    def btEngine_JobSentSlot(self, sender, event):
        self.eventSignal.emit(" ID :" + str(event.ID)+"\n"+"任务发送：" + event.Name + " "+event.Status+"\n")

    # 任务回溯时触发
    def btEngine_JobResumedSlot(self, sender, event):
        self.eventSignal.emit(" ID :" + str(event.ID)+"\n"+"任务恢复：" + event.Name + " "+event.Status+"\n")

    # 任务重启时触发
    def btEngine_JobRestartedSlot(self, sender, event):
        self.eventSignal.emit(" ID :" + str(event.ID)+"\n"+"任务重启：" + event.Name + " "+event.Status+"\n")

    # 任务暂停时触发
    def btEngine_JobPausedSlot(self, sender, event):
        self.eventSignal.emit(" ID :" + str(event.ID)+"\n"+"任务暂停：" + event.Name + " "+event.Status+"\n")

    # 监控出错时触发
    def btEngine_JobMonitorErrorOccurredSlot(self, sender, event):
        self.eventSignal.emit(" ID :" + str(event.ID)+"\n"+"监控出错：" + event.Name + " "+event.Status+"\n")

    # 打印出错时触发
    def btEngine_JobErrorOccurredSlot(self, sender, event):
        self.eventSignal.emit(" ID :" + str(event.ID)+"\n"+"任务出错：" + event.Name + " "+event.Status+"\n")

    # 打印任务关闭时触发
    def btEngine_JobCancelledSlot(self, sender, event):
        self.eventSignal.emit(" ID :" + str(event.ID)+"\n"+"任务关闭：" + event.Name + " "+event.Status+"\n")

    # 打印任务入列时触发
    def btEngine_JobQueuedSlot(self, sender, event):
        self.eventSignal.emit(" ID :" + str(event.ID)+"\n"+"任务入列：" + event.Name + " "+event.Status+"\n")


