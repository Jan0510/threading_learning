#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/11/7 10:38

'''全局变量表
'''
_global_dict = {}

def global_maneger_init():  # 初始化
    global _global_dict
    # 全局变量表
    # 1 与下位机通信相关变量
    _global_dict['status_print'] = 0
    _global_dict['status_recheck'] = 0
    _global_dict['cmd_mode'] = 0
    _global_dict['x_1'] = 0
    _global_dict['y_1'] = 0
    _global_dict['print_res_1'] = 0
    _global_dict['x_2'] = 0
    _global_dict['y_2'] = 0
    _global_dict['print_res_2'] = 0
    _global_dict['recheck_res_1'] = 0
    _global_dict['recheck_res_2'] = 0
    _global_dict['serial_connect'] = False
    # 2 与mes系统通信相关变量
    _global_dict['mes_login'] = False
    _global_dict['mes_doing_push_work_order'] = False
    _global_dict['FUNCTION_NAME']=0
    _global_dict['SERIAL_NUMBER']=0
    _global_dict['PARAME_VALUE']=0
    _global_dict['TARGET_QTY']=0
    _global_dict['SN_QTY'] = 0
    # 3 自动运行时的计数器
    _global_dict['current_SN'] = ''
    _global_dict['print_num'] = 0
    _global_dict['print_check_OK_num'] = 0
    _global_dict['print_check_NG_num'] = 0
    _global_dict['recheck_OK_num'] = 0
    _global_dict['recheck_NG_num'] = 0
def set_global_value(key, value):
    """ 定义一个全局变量 """
    global _global_dict
    _global_dict[key] = value

def get_global_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    global _global_dict
    try:
        return _global_dict[key]
    except KeyError:
        return defValue