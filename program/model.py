# -*- encoding: utf-8 -*-
'''
@File : model.py
@Time : 2019/01/24 15:02:07
@Author : zhangyachen
@Version : 1.0
@Contact : aachen@163.com
@License : (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc : None
'''

# here put the import lib
import keras
from keras.callbacks import LambdaCallback
from keras.models import Input, Model, load_model
from keras.layers import LSTM, Dropout, Dense, Flatten, Bidirectional, Embedding, GRU
from keras.optimizers import Adam


def build_model(config, num2word, words):
    '''建立模型'''

    # 输入的dimension
    input_tensor = Input(shape=(config.max_len,))
    embedd = Embedding(
        len(num2word) + 2, 300, input_length=config.max_len)(input_tensor)
    lstm = Bidirectional(GRU(128, return_sequences=True))(embedd)
    # dropout = Dropout(0.6)(lstm)
    # lstm = LSTM(256)(dropout)
    # dropout = Dropout(0.6)(lstm)
    flatten = Flatten()(lstm)
    dense = Dense(len(words), activation='softmax')(flatten)
    model = Model(inputs=input_tensor, outputs=dense)
    optimizer = Adam(lr=config.learning_rate)
    model.compile(
        loss='categorical_crossentropy',
        optimizer=optimizer,
        metrics=['accuracy'])
    return model
