# -*- encoding: utf-8 -*-
'''
@File : data_utils.py
@Time : 2019/01/24 10:41:50
@Author : zhangyachen
@Version : 1.0
@Contact : aachen@163.com
@License : (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc : None
'''

# here put the import lib
from tool.config import Config

# 标点符号集
puncs = [']', '[', '（', '）', '{', '}', '：', '《', '》']


# 预料文本处理
def preprocess_file(Config):
    # 预料文本内同
    files_content = ''
    with open(Config.poetry_file, "r", encoding='utf-8') as f:
        for line in f:
            # 每行的末尾加上"]"符号代表一首诗结束

            for char in puncs:
                line = line.replace(char, "")
            files_content += line.strip() + "]"
    words = sorted(list(files_content))
    words.remove(']')
    counted_works = {}
    for word in words:
        if word in counted_works:
            counted_works[word] += 1
        else:
            counted_works[word] = 1
    # 去掉低频字
    erase = []
    for key in counted_works:
        if counted_works[key] <= 2:
            erase.append(key)
        for key in erase:
            del counted_works[key]
        del counted_works[']']
        wordPairs = sorted(counted_works.items(), key=lambda x: -x[1])

        words, _ = zip(*wordPairs)
        # word到id的映射
        word2num = dict((c, i + 1) for i, c in enumerate(words))
        num2word = dict((i, c) for i, c in enumerate(words))
        word2numF = lambda x: word2num.get(x, 0)

        return word2numF, num2word, words, files_content


word2numF, num2word, words, files_content = preprocess_file(Config)
# utils.text_save("data/output/data_set/word2numF.txt", word2numF)
# utils.text_save("data/output/data_set/num2word.txt", num2word)
# utils.text_save("data/output/data_set/words.txt", words)
# utils.text_save("data/output/data_set/files_content.txt", files_content)
