#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/11/5 13:48
import configparser
import datetime as dt
import operator
import os

FolderPath = os.getcwd()  # 获取当前路径

class FileSystem:
    def __init__(self):
        self.logDirPath = FolderPath + "\\log\\"
        self.confDirPath = FolderPath + "\\conf\\"
        # 日志文件都存放在文件夹Log中
        if (os.path.exists(self.logDirPath)):
            pass
        else:
            os.mkdir(self.logDirPath)

        # 'a'表示可连续写入到文件，保留原内容，在原内容之后写入。'w'会自动清空文件内容。
        Logfilename = "%s_Log.txt" % dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.txtLogFile = open(self.logDirPath + Logfilename, "w")  # 设置文件对象，放在脚本文件夹下
        # 打印日志信息
        self.logcat_into_file("Application Start...")
    def logcat_into_file(self, msg):
        # 获取当前时间
        now_time = dt.datetime.now().strftime('%T') + " : "
        self.txtLogFile.writelines(now_time + msg)  # 写入列表
        self.txtLogFile.write('\n')
        self.txtLogFile.flush()  # 强制刷新，使数据从缓冲区推入txt文件中
    def get_conf_dict(self, file):
        filePath = self.confDirPath + file
        cf = configparser.ConfigParser()
        cf.read(filePath)
        self.conf_dict = {}
        sec = cf.sections()
        if len(sec) > 0:
            try:
                for key, value in cf.items("config"):
                    self.conf_dict[key] = value
            except Exception as ex:
                print(ex)
        return self.conf_dict
    def if_diff(self, new_dict):
        return operator.eq(self.conf_dict, new_dict)
    def save_defualt_configure(self, conf_dict, file):
        filePath = self.confDirPath + file
        cf = configparser.ConfigParser()
        cf.add_section("config")            # 添加一个新的section
        for key, value in conf_dict.items():
            cf.set("config", key, value)    # 对section中的option信息进行写入
        # 覆盖式写入config
        with open(filePath, "w+") as f:
            cf.write(f)