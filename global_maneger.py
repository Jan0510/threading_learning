#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/11/7 10:38

'''全局变量表
'''
_global_dict = {}

def _init():  # 初始化
    global _global_dict


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