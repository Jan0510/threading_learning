#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/10/29 23:47
import configparser
import datetime
import os

# 集合了日志功能和开机初始化配置
class FileSystem():
    def __init__(self):
        folder_path = os.getcwd()  # 获取当前路径
        self.txtLogFile = None
        self.log_path = folder_path+"\\Log\\"
        # 判断目录是否存在
        if os.path.exists(self.log_path):
            pass
        else:
            os.mkdir(self.log_path)
        # 'a'表示可连续写入到文件，保留原内容，在原内容之后写入。'w'会自动清空文件内容。
        self.log_file_name = "%s_Log.txt" % datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.txtLogFile = open(self.log_path + self.log_file_name, "w")  # 设置文件对象，放在脚本文件夹下
        # 打印日志信息到文本
        self.logcat_into_file("Application Start...")

        self.conf_path = folder_path + "\\conf\\"
        if os.path.exists(self.conf_path):
            pass
        else:
            os.mkdir(self.conf_path)

    def get_conf_dict(self, filename):
        conf_dict = {}
        if len(filename) > 0:
            try:
                cf = configparser.ConfigParser()
                file = self.conf_path+filename
                cf.read(file, encoding='utf-8')
                for key, value in cf.items('config'):
                    conf_dict[key] = value
            except Exception as ex:
                print(ex)
        return conf_dict
    def save_defualt_configure(self, conf_dict, filename):
        try:
            cf = configparser.ConfigParser()
            file = self.conf_path+filename
            cf.read(file, encoding='utf-8')
            list = cf.sections()
            if 'config' not in list:# 如果分组type不存在则插入type分组
                cf.add_section("config")
            for key, value in conf_dict.items():
                cf.set("config", str(key), str(value))
            # 'w'读写模式,文件不存在会创建文件，但是如果文件存在会将其覆盖
            with open(file, "w", encoding='utf-8') as f:
                cf.write(f)
        except Exception as ex:
            print(ex)
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