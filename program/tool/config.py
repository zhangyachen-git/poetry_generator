# -*- encoding: utf-8 -*-
'''
@File : config.py
@Time : 2019/01/24 10:43:56
@Author : zhangyachen
@Version : 1.0
@Contact : aachen@163.com
@License : (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc : None
'''


# here put the import lib
class Config(object):
    # 原始数据
    poetry_file = "../data/original_data/poetry.txt"
    # 权重
    weight_file = "../data/output/weight_file/poetry_model.h5"
    # 根据前六个字预测第七个字
    max_len = 6
    batch_size = 512
    learning_rate = 0.001
    # 配置启动步骤
    run_flag = "2"
