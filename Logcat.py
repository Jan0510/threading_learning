#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 23:47
import datetime
import os


class Logcat():
    def __init__(self, log_dir_path):
        self.txtLogFile = None
        # 判断目录是否存在
        if os.path.exists(log_dir_path):
            pass
        else:
            os.mkdir(log_dir_path)

        # 'a'表示可连续写入到文件，保留原内容，在原内容之后写入。'w'会自动清空文件内容。
        log_file_name = "%s_Log.txt" % datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.txtLogFile = open(log_dir_path + log_file_name, "w")  # 设置文件对象，放在脚本文件夹下
        # 打印日志信息到文本
        self.logcat_into_file("Application Start...")

    # 打印日志信息到文本
    def logcat_into_file(self, text):
        if self.txtLogFile:
            self.txtLogFile.writelines(text)  # 写入文件
            self.txtLogFile.flush()  # 强制刷新，使数据从缓冲区推入txt文件中
            return True
        else:
            return False
    # 析构函数
    def __del__(self):
        self.txtLogFile.flush()  # 强制刷新，使数据从缓冲区推入txt文件中
        self.txtLogFile.close()