#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  :   {Jan__}
# @Time    :   2020/11/5 13:48

import ConfigParser
if __name__ == '__main__':
    cf = ConfigParser.SafeConfigParser()

    file = cf.read("default.ini")
    print(file)
    sec = cf.sections()
    print(sec)
