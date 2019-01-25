# -*- encoding: utf-8 -*-
'''
@File : train.py
@Time : 2019/01/24 14:37:22
@Author : zhangyachen
@Version : 1.0
@Contact : aachen@163.com
@License : (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc : None
'''

# here put the import lib
import keras
import random
import numpy as np
from keras.callbacks import LambdaCallback
import model
import sys
sys.path.append('program/tool')
import utils
import data_utils


class train(object):
    def __init__(self, config):
        self.model = None
        self.do_train = True
        self.loaded_model = False
        self.config = config

        # 文件预处理
        self.word2numF, self.num2word, self.words, self.files_content = data_utils.preprocess_file(
            self.config)

        self.train()

    def sample(self, preds, temperature=1.0):
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

    def generate_sample_result(self, epoch, logs):
        '''训练过程中，每个epoch打印出当前的学习情况'''
        # if epoch % 5 != 0:
        #     return
        print(
            "\n==================Epoch {}=====================".format(epoch))
        #utils.text_save(epoch)
        for diversity in [0.5, 1.0, 1.5]:
            print("------------Diversity {}--------------".format(diversity))
            start_index = random.randint(
                0,
                len(self.files_content) - self.config.max_len - 1)
            generated = ''
            sentence = self.files_content[start_index:start_index +
                                          self.config.max_len]
            generated += sentence
            for i in range(20):
                x_pred = np.zeros((1, self.config.max_len))
                for t, char in enumerate(sentence[-6:]):
                    x_pred[0, t] = self.word2numF(char)

                preds = self.model.predict(x_pred, verbose=0)[0]
                next_index = self.sample(preds, diversity)
                next_char = self.num2word[next_index]

                generated += next_char
                sentence = sentence + next_char
            print(sentence)

    def data_generator(self):
        '''生成器生成数据'''
        i = 0
        while 1:
            x = self.files_content[i:i + self.config.max_len]
            y = self.files_content[i + self.config.max_len]

            puncs = [']', '[', '（', '）', '{', '}', '：', '《', '》', ':']
            if len([i for i in puncs if i in x]) != 0:
                i += 1
                continue
            if len([i for i in puncs if i in y]) != 0:
                i += 1
                continue

            y_vec = np.zeros(shape=(1, len(self.words)), dtype=np.bool)
            y_vec[0, self.word2numF(y)] = 1.0

            x_vec = np.zeros(shape=(1, self.config.max_len), dtype=np.int32)

            for t, char in enumerate(x):
                x_vec[0, t] = self.word2numF(char)
            yield x_vec, y_vec
            i += 1

    def train(self):
        '''训练模型'''
        # number_of_epoch = len(self.files_content) // self.config.batch_size
        number_of_epoch = 50
        builded_model = model.build_model(self.config, self.num2word,
                                          self.words)
        self.model = builded_model

        self.model.summary()

        history = self.model.fit_generator(
            generator=self.data_generator(),
            verbose=True,
            steps_per_epoch=self.config.batch_size,
            epochs=number_of_epoch,
            callbacks=[
                keras.callbacks.ModelCheckpoint(
                    self.config.weight_file, save_weights_only=False),
                LambdaCallback(on_epoch_end=self.generate_sample_result)
            ])
        utils.result_image(history)