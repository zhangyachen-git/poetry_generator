# -*- encoding: utf-8 -*-
'''
@File : main.py
@Time : 2019/01/24 14:24:53
@Author : zhangyachen
@Version : 1.0
@Contact : aachen@163.com
@License : (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc : None
'''

# here put the import lib
import train
import test
import application
import sys
sys.path.append('program/tool')
if __name__ == "__main__":
    if Config.run_flag == "0":
        train.train(Config)
    elif Config.run_flag == "1":
        test.test(Config)
    else:
        application.application(Config)
