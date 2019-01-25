# -*- encoding: utf-8 -*-
'''
@File : utils.py
@Time : 2019/01/24 15:54:20
@Author : zhangyachen
@Version : 1.0
@Contact : aachen@163.com
@License : (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc : None
'''

# here put the import lib
import matplotlib.pyplot as plt


# 数据写入文件
def text_save(filename, data):
    file = open(filename, 'a')
    file.write(str(data))
    file.close()
    print(filename + "文件保存成功")


def result_image(history):
    # acc
    plt.plot(history.history['acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train'], loc='upper left')
    plt.savefig('project_doumentation/train_log/acc.jpg')
    # loss
    plt.plot(history.history['loss'])
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train'], loc='upper left')
    plt.savefig('project_doumentation/train_log/loss.jpg')