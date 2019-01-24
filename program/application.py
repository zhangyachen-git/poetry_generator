# -*- encoding: utf-8 -*-
'''
@File : application.py
@Time : 2019/01/24 14:41:27
@Author : zhangyachen
@Version : 1.0
@Contact : aachen@163.com
@License : (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc : None
'''

# here put the import lib
import os
import numpy as np
import random
import train
from keras.models import Input, Model, load_model
import sys
sys.path.append('program/tool')
from config import Config
import data_utils

# 文件预处理
word2numF, num2word, words, files_content = data_utils.preprocess_file(Config)


def sample(preds, temperature=1.0):
    '''
    当temperature=1.0时，模型输出正常
    当temperature=0.5时，模型输出比较open
    当temperature=1.5时，模型输出比较保守
    在训练的过程中可以看到temperature不同，结果也不同
    '''
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def application(config):
    '''根据给出的文字，生成诗句'''
    # 判断模型是否存在
    if os.path.exists(config.weight_file):
        model = load_model(config.weight_file)
        model.summary()
    else:
        train.train(Config)

    text = input("请输入:")
    with open(config.poetry_file, 'r', encoding='utf-8') as f:
        file_list = f.readlines()
    random_line = random.choice(file_list)
    # 如果给的text不到四个字，则随机补全
    if not text or len(text) != 4:
        for _ in range(4 - len(text)):
            random_str_index = random.randrange(0, len(words))
            text += num2word.get(
                random_str_index) if num2word.get(random_str_index) not in [
                    ',', '。', '，'
                ] else num2word.get(random_str_index + 1)
    seed = random_line[-(config.max_len):-1]

    res = ''

    seed = 'c' + seed

    for c in text:
        seed = seed[1:] + c
        for j in range(5):
            x_pred = np.zeros((1, config.max_len))
            for t, char in enumerate(seed):
                x_pred[0, t] = word2numF(char)

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, 1.0)
            next_char = num2word[next_index]
            seed = seed[1:] + next_char
        res += seed
    print(res)
