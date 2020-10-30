# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/4/14 10:32

import datetime as dt
import serial
import serial.tools.list_ports

import clr
import os
import sys

FolderPath = os.getcwd()  # 获取当前路径
sys.path.append(FolderPath)  # 加载当前路径
clr.FindAssembly("Seagull.BarTender.Print.dll")
clr.AddReference("Seagull.BarTender.Print")
clr.FindAssembly("mscorlib.dll")
clr.AddReference("mscorlib")
from Seagull.BarTender.Print import Engine, Printers, Printer, LabelFormatDocument, Messages, Message, SaveOptions
from System import EventHandler
from app import Ui_Form
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtCore import QTimer


class myAutoPrintAppication(QWidget, Ui_Form):
    def __init__(self):
        super(myAutoPrintAppication, self).__init__()  # 分别调用了2个父类的初始化函数
        # UI界面控件的初始化
        self.setupUi(self)
        # 创建 BarTender 的 Engine，参数True代表创建时自动调用Start函数
        self.btEngine = Engine(True)
        # 构造一个Serial类对象
        self.ser = serial.Serial()
        # 创建一个日志文档
        self.openLogFile()
        # UI控件的信号绑定
        self.signalCombine()
        # 刷新打印机/标签文件列表
        self.refreshListSlot()
        # 串口检测
        self.port_check()
        # 按钮使能初始化
        self.bnt_disenable()
    # 按钮使能初始化-禁能
    def bnt_disenable(self):
        self.bnt_closeSerial.setEnabled(0)      # 禁能
        self.bnt_openSerial.setEnabled(0)       # 禁能
        self.bnt_connect.setEnabled(0)          # 禁能
        self.bnt_break.setEnabled(0)            # 禁能
    # 创建一个日志
    def openLogFile(self):
        LogdirPath = FolderPath + "\\Log\\"
        # 日志文件都存放在文件夹Log中
        if (os.path.exists(LogdirPath)):
            pass
        else:
            os.mkdir(LogdirPath)

        # 'a'表示可连续写入到文件，保留原内容，在原内容之后写入。'w'会自动清空文件内容。
        Logfilename = "%s_Log.txt" % dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.txtLogFile = open(LogdirPath + Logfilename, "w")  # 设置文件对象，放在脚本文件夹下
        # 打印日志信息
        self.logInfoPrint("Application Start...")
    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        # 获取串口列表，调用list把一个字典转换成一个列表，port_list是个2维数组。
        port_list = list(serial.tools.list_ports.comports())
        # 清除控件的内容
        self.SerialList.clear()
        for port in port_list:
            # 把port_list里的每个对象转换成字典键值对，port[0]是COM0，port[1]是COM1对应的信息
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            #"%s:%d"%("ab",3) => "ab:3"，%s表示格化式一个对象为字符串，%d表示整数。
            # 为窗口控件的下拉列表增加项
            self.SerialList.addItem(port[0])
        # 判断有无串口
        if len(self.Com_Dict) == 0:
            self.serial_state_info.setText("无可用串口")
            self.bnt_openSerial.setEnabled(0)
            return 0
        else:
            self.bnt_openSerial.setEnabled(1)
            return 1
    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息，该按钮是列表按钮
        imf_s = self.SerialList.currentText()   # 经过串口检测函数，该列表按钮已经有了可选内容，获取用户选择的内容
        if imf_s != "":                         # 如果没有选，则显示的内容照旧
            self.serial_state_info.setText(self.Com_Dict[self.SerialList.currentText()])
            # 判断是否之前有串口被打开
            if self.ser.isOpen():
                # 之前有串口被打开还未关闭，则打开按钮继续禁能
                self.bnt_openSerial.setEnabled(0)
            else:
                # 当前还没有串口被打开
                self.bnt_openSerial.setEnabled(1)
                self.bnt_closeSerial.setEnabled(0)
                self.bnt_connect.setEnabled(0)
                self.bnt_break.setEnabled(0)
    # 打开串口
    def port_open(self):
        # try...except..处理异常的结构，使程序不会闪退，而是返回错误信息并跳过
        # 被监控的程序段
        try:
            # 打开串口前先检测是否有串口可用
            if_serial_Exist = self.port_check()
            if if_serial_Exist == 0:
                return None
            self.ser.port = self.SerialList.currentText()  # 串口号
            self.ser.baudrate = 115200  # 波特率
            self.ser.bytesize = 8  # 数据位
            self.ser.stopbits = 1  # 停止位
            self.ser.parity = 'N'  # 校验位
            # 打开串口
            self.ser.open()
        # 若发送异常则执行的程序段
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(2)
        # 打开成功后，按钮禁能
        if self.ser.isOpen():
            self.bnt_scanSerial.setEnabled(False)   # 禁能
            self.bnt_openSerial.setEnabled(False)   # 禁能
            self.bnt_closeSerial.setEnabled(True)   # 使能
            self.bnt_connect.setEnabled(True)       # 使能
            self.serial_state_info.setText("串口状态（已开启）")
    # 关闭串口
    def port_close(self):
        try:
            # 关闭接收定时器
            self.timer.stop()
            self.ser.close()
        except:
            pass
        self.bnt_scanSerial.setEnabled(True)
        self.bnt_openSerial.setEnabled(True)
        self.bnt_closeSerial.setEnabled(False)
        self.bnt_connect.setEnabled(False)
        self.bnt_break.setEnabled(False)
        self.serial_state_info.setText("串口状态（已关闭）")
    # 串口数据接收函数，由定时器触发
    def data_receive(self):
        pass

    # 信号与槽函数绑定
    def signalCombine(self):
        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)
        # 串口检测按钮
        self.bnt_scanSerial.clicked.connect(self.port_check)  # 按钮clicked事件，连接函数port_check

        # 串口选择按钮的信息显示
        self.SerialList.currentTextChanged.connect(self.port_imf)  # 文本显示

        # 打开串口按钮
        self.bnt_openSerial.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.bnt_closeSerial.clicked.connect(self.port_close)

        # 打印机改变时
        self.PrintersList.currentTextChanged.connect(self.printerChangeSlot)
        # 标签文件改变时
        self.FormatFileList.currentTextChanged.connect(self.lableFormatFileChangeSolt)
        # 刷新列表按钮
        self.bnt_refreshPrintersList.clicked.connect(self.refreshListSlot)
        # 试打印按钮
        self.bnt_tryPrint.clicked.connect(self.tryPrintSlot)
        # EventHandler 来自 System，在C#中EventHandler其实是一个模板，由于在python里面不用声明类型
        # 所以直接使用了模板
        self.btEngine.JobCancelled += EventHandler(self.btEngine_JobCancelledSlot)
        self.btEngine.JobErrorOccurred += EventHandler(self.btEngine_JobErrorOccurredSlot)
        self.btEngine.JobMonitorErrorOccurred += EventHandler(self.btEngine_JobMonitorErrorOccurredSlot)
        self.btEngine.JobPaused += EventHandler(self.btEngine_JobPausedSlot)
        self.btEngine.JobQueued += EventHandler(self.btEngine_JobQueuedSlot)
        self.btEngine.JobRestarted += EventHandler(self.btEngine_JobRestartedSlot)
        self.btEngine.JobResumed += EventHandler(self.btEngine_JobResumedSlot)
        self.btEngine.JobSent += EventHandler(self.btEngine_JobSentSlot)
        # 切换数据源时
        self.comboBox_sourceName.currentTextChanged.connect(self.sourceNameChangeSlot)
        # 修改数据源内容时
        self.bnt_sourceContentModify.clicked.connect(self.sourceContentChangeSlot)

    # 任务发送时触发
    def btEngine_JobSentSlot(self, sender, event):
        self.logInfoPrint("任务发送：" + event.Name + " " + event.Status)
        self.logInfoPrint(" ID :" + str(event.ID))
        self.logInfoPrint("ClientName：" + str(event.ClientName))
        self.logInfoPrint("PrinterInfo：" + str(event.PrinterInfo))
        self.logInfoPrint("TotalPages：" + str(event.TotalPages))
        self.logInfoPrint("PagesPrinted：" + str(event.PagesPrinted))
        self.logInfoPrint("UserName：" + str(event.UserName))

    # 任务回溯时触发
    def btEngine_JobResumedSlot(self, sender, event):
        self.logInfoPrint("任务回溯：" + event.Name + " " + event.Status)
        self.logInfoPrint(" ID :" + str(event.ID))
        self.logInfoPrint("ClientName：" + str(event.ClientName))
        self.logInfoPrint("PrinterInfo：" + str(event.PrinterInfo))
        self.logInfoPrint("TotalPages：" + str(event.TotalPages))
        self.logInfoPrint("PagesPrinted：" + str(event.PagesPrinted))
        self.logInfoPrint("UserName：" + str(event.UserName))

    # 任务重启时触发
    def btEngine_JobRestartedSlot(self, sender, event):
        self.logInfoPrint("任务重启：" + event.Name + " " + event.Status)
        self.logInfoPrint(" ID :" + str(event.ID))
        self.logInfoPrint("ClientName：" + str(event.ClientName))
        self.logInfoPrint("PrinterInfo：" + str(event.PrinterInfo))
        self.logInfoPrint("TotalPages：" + str(event.TotalPages))
        self.logInfoPrint("PagesPrinted：" + str(event.PagesPrinted))
        self.logInfoPrint("UserName：" + str(event.UserName))

    # 任务暂停时触发
    def btEngine_JobPausedSlot(self, sender, event):
        self.logInfoPrint("任务暂停：" + event.Name + " " + event.Status)
        self.logInfoPrint(" ID :" + str(event.ID))
        self.logInfoPrint("ClientName：" + str(event.ClientName))
        self.logInfoPrint("PrinterInfo：" + str(event.PrinterInfo))
        self.logInfoPrint("TotalPages：" + str(event.TotalPages))
        self.logInfoPrint("PagesPrinted：" + str(event.PagesPrinted))
        self.logInfoPrint("UserName：" + str(event.UserName))

    # 监控出错时触发
    def btEngine_JobMonitorErrorOccurredSlot(self, sender, event):
        self.logInfoPrint("监控出错：" + event.Name + " " + event.Status)
        self.logInfoPrint(" ID :" + str(event.ID))
        self.logInfoPrint("ClientName：" + str(event.ClientName))
        self.logInfoPrint("PrinterInfo：" + str(event.PrinterInfo))
        self.logInfoPrint("TotalPages：" + str(event.TotalPages))
        self.logInfoPrint("PagesPrinted：" + str(event.PagesPrinted))
        self.logInfoPrint("UserName：" + str(event.UserName))

    # 打印出错时触发
    def btEngine_JobErrorOccurredSlot(self, sender, event):
        self.logInfoPrint("任务出错：" + event.Name + " " + event.Status)
        self.logInfoPrint(" ID :" + str(event.ID))
        self.logInfoPrint("ClientName：" + str(event.ClientName))
        self.logInfoPrint("PrinterInfo：" + str(event.PrinterInfo))
        self.logInfoPrint("TotalPages：" + str(event.TotalPages))
        self.logInfoPrint("PagesPrinted：" + str(event.PagesPrinted))
        self.logInfoPrint("UserName：" + str(event.UserName))

    # 打印任务关闭时触发
    def btEngine_JobCancelledSlot(self, sender, event):
        self.logInfoPrint("任务关闭：" + event.Name + " " + event.Status)
        self.logInfoPrint(" ID :" + str(event.ID))
        self.logInfoPrint("ClientName：" + str(event.ClientName))
        self.logInfoPrint("PrinterInfo：" + str(event.PrinterInfo))
        self.logInfoPrint("TotalPages：" + str(event.TotalPages))
        self.logInfoPrint("PagesPrinted：" + str(event.PagesPrinted))
        self.logInfoPrint("UserName：" + str(event.UserName))

    # 打印任务入列时触发
    def btEngine_JobQueuedSlot(self, sender, event):
        self.logInfoPrint("任务入列：" + event.Name + " " + event.Status)
        self.logInfoPrint(" ID :" + str(event.ID))
        self.logInfoPrint("ClientName：" + str(event.ClientName))
        self.logInfoPrint("PrinterInfo：" + str(event.PrinterInfo))
        self.logInfoPrint("TotalPages：" + str(event.TotalPages))
        self.logInfoPrint("PagesPrinted：" + str(event.PagesPrinted))
        self.logInfoPrint("UserName：" + str(event.UserName))

    # 改变打印机时触发
    def printerChangeSlot(self):
        # 修改打印机变量
        self.usingPrinter = self.PrintersList.currentText()
        # 打印日志信息
        self.logInfoPrint("当前使用的打印机是：" + self.usingPrinter)

    # 切换数据源时触发
    def sourceNameChangeSlot(self):
        name = self.comboBox_sourceName.currentText()
        for substring in self.btFormat.SubStrings:
            if name == substring.Name:
                self.lineEdit_sourceContent.setText(str(substring.Value))

    # 修改数据源内容时触发
    def sourceContentChangeSlot(self):
        name = self.comboBox_sourceName.currentText()
        for substring in self.btFormat.SubStrings:
            if name == substring.Name:
                self.btFormat.SubStrings.SetSubString(name, self.lineEdit_sourceContent.text())
                self.logInfoPrint("修改数据源" + name + "的内容为：" + self.lineEdit_sourceContent.text())

    # 刷新列表槽函数
    def refreshListSlot(self):
        # 重新读取打印机列表
        # 创建打印机集合
        self.printers = Printers()
        # 列举打印机
        self.logInfoPrint("当前有 " + str(self.printers.Count) + " 台打印机")
        # 填充打印机列表
        self.PrintersList.clear()
        for printer in self.printers:
            self.logInfoPrint("打印设备：" + printer.PrinterName)
            self.PrintersList.addItem(printer.PrinterName, None)
        self.PrintersList.setCurrentText(self.printers.Default.PrinterName)
        self.logInfoPrint("默认打印机是：" + self.printers.Default.PrinterName)
        # 当前使用的打印机是默认打印机
        self.usingPrinter = self.printers.Default.PrinterName

        # 标签文件列表
        self.labelFormatFileList = []
        self.FormatFileList.clear()
        # 从指定目录下筛选出.btw文件
        btwdirPath = FolderPath + "\\btw\\"
        for file in os.listdir(btwdirPath):

            if file[-4] == "." and file[-3] == "b" and file[-2] == "t" and file[-1] == "w":
                # 填充文件列表
                self.FormatFileList.addItem(file, None)
                self.logInfoPrint("标签文件：" + file)
                self.labelFormatFileList.append(file)
        if self.labelFormatFileList:
            self.logInfoPrint("找到了 " + str(len(self.labelFormatFileList)) + " 个标签文件")
            self.usingLabelFormatFile = self.FormatFileList.currentText()
        else:
            self.logInfoPrint("没有找到标签文件")
            self.usingLabelFormatFile = None

    # 改变标签文件时触发
    def lableFormatFileChangeSolt(self):
        # 修改文件变量
        self.usingLabelFormatFile = self.FormatFileList.currentText()
        # 显示文件预览
        if self.usingLabelFormatFile:
            self.openLableFormatDoc()
        # 打印日志信息
        self.logInfoPrint("当前使用的标签文件是：" + self.usingLabelFormatFile)

    # 试打印
    def tryPrintSlot(self):
        self.myPrint()

    # 打印日志信息
    def logInfoPrint(self, text):
        # 获取当前时间
        now_time = dt.datetime.now().strftime('%T') + " : "
        self.Log.insertPlainText(now_time + text)
        self.Log.insertPlainText('\n')
        self.txtLogFile.writelines(now_time + text)  # 写入列表
        self.txtLogFile.write('\n')
        self.txtLogFile.flush()     # 强制刷新，使数据从缓冲区推入txt文件中

    # 打开标签文件
    def openLableFormatDoc(self):
        # 打开一个.btw文件
        try:
            btwdirPath = FolderPath + "\\btw\\"
            self.btFormat = self.btEngine.Documents.Open(btwdirPath + self.usingLabelFormatFile)
            self.logInfoPrint("打开标签文件：" + str(self.usingLabelFormatFile) + " 成功！")
            self.logInfoPrint("当前打开了" + str(self.btEngine.Documents.Count) + " 个标签文件")
            # 是否支持序列化
            if self.btFormat.PrintSetup.SupportsSerializedLabels:
                self.logInfoPrint("支持序列化")
            else:
                self.logInfoPrint("不支持序列化")
            # 数据源个数
            self.lineEdit_sourceCount.setText(str(self.btFormat.SubStrings.Count))
            self.logInfoPrint("SubStrings Count:" + str(self.btFormat.SubStrings.Count))
            # 数据源名称
            self.comboBox_sourceName.clear()
            for substring in self.btFormat.SubStrings:
                self.comboBox_sourceName.addItem(str(substring.Name), None)
                self.logInfoPrint("SubString Name: " + str(substring.Name))
                self.logInfoPrint("SubString Type: " + str(substring.Type))
                self.logInfoPrint("SubString Value: " + str(substring.Value))
                self.logInfoPrint("SerializeBy: " + str(substring.SerializeBy))
                self.logInfoPrint("SerializeEvery: " + str(substring.SerializeEvery))

            # self.logInfoPrint("RecordRange ：" + str(self.btFormat.PrintSetup.RecordRange))
            # 副本数
            self.logInfoPrint("IdenticalCopiesOfLabel ：" + str(self.btFormat.PrintSetup.IdenticalCopiesOfLabel))
            # 序列长度
            self.logInfoPrint("NumberOfSerializedLabels：" + str(self.btFormat.PrintSetup.NumberOfSerializedLabels))

        except Exception as e:
            self.logInfoPrint(str(e))

    # 打印设置
    def configPrintSetup(self):
        self.btFormat.PrintSetup.PrinterName = self.usingPrinter  # 打印机

    # 打印操作
    def myPrint(self):
        # 判断bartender是否启动
        if self.btEngine.IsAlive:
            pass
        else:
            self.btEngine.Start()
        # 打印返回的消息
        btMessages = Messages()
        # 打印超时定时器 ms
        waitForCompletionTimeout = 10000
        # 打印
        try:
            self.logInfoPrint("开始打印...")
            # 正在打印的标签拥有的数据源个数
            self.logInfoPrint("SubStrings Count:" + str(self.btFormat.SubStrings.Count))
            # 标签中的数据源字段，键值对
            for substring in self.btFormat.SubStrings:
                self.logInfoPrint("SubString Name: " + str(substring.Name))
                self.logInfoPrint("SubString Value: " + str(substring.Value))
            # 调用库的打印函数，将数据推入打印队列
            nResult = self.btFormat.Print("printjob", waitForCompletionTimeout, btMessages)
            self.logInfoPrint("Print status = " + str(nResult))

            Count = int(self.lineEdit_PrintCount.text()) + 1
            self.lineEdit_PrintCount.setText(str(Count))
            if nResult != 0:
                Count = int(self.lineEdit_FailedCount.text()) + 1
                self.lineEdit_FailedCount.setText(str(Count))

        except Exception as e:
            print(e)
            Count = int(self.lineEdit_FailedCount.text()) + 1
            self.lineEdit_FailedCount.setText(str(Count))

        # 如果该标签支持序列化打印，那么每次打印后，序列号都会被Bartender修改，需要更新在窗口上
        # 是否支持序列化
        if self.btFormat.PrintSetup.SupportsSerializedLabels:
            # 更新窗口的内容
            self.sourceNameChangeSlot()
        self.logInfoPrint("消息集合中有" + str(btMessages.Count) + "条消息")
        self.logInfoPrint("**********************")
        for m in btMessages:
            self.logInfoPrint("Category = " + str(m.Category))
            self.logInfoPrint("ID = " + str(m.ID))
            self.logInfoPrint("Severity = " + str(m.Severity))
            self.logInfoPrint("Text = " + str(m.Text))
            self.logInfoPrint("********")

    # 重写app窗口关闭函数
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出', "是否要退出程序？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # 如果存在标签文件被打开，则询问是否保存修改
        if self.btFormat:
            if reply == QMessageBox.Yes:
                reply = QMessageBox.question(self, '标签文件', "对标签文件是否要保存修改？", QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.btFormat.Close(SaveOptions.SaveChanges)
                else:
                    self.btFormat.Close(SaveOptions.DoNotSaveChanges)
        self.txtLogFile.close()

        if self.btEngine.IsAlive:
            # 停止引擎
            self.btEngine.Stop()
            # 释放资源
            self.btEngine.Dispose()

        else:
            event.ignore()


"""if __name__ == '__main__'的意思是：
当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；
当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。"""
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)  # 实例化一个应用对象，sys.argv是一组命令行参数的列表。Python可以在shell里运行，这是一种通过参数来选择启动脚本的方式。
        myshow = myAutoPrintAppication()
        myshow.show()

        sys.exit(app.exec_())  # 确保主循环安全退出
    except Exception as e:
        print(e)
        if myshow.btEngine.IsAlive:
            # 停止引擎
            myshow.btEngine.Stop()
            # 释放资源
            myshow.btEngine.Dispose()

