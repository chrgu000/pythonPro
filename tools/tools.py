# -*- coding: utf-8 -*
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from datetime import datetime
from datetime import timedelta
import uuid

def get_uuid(name):
    uid_ = uuid.uuid3(uuid.NAMESPACE_DNS, name)
    uid = str(uid_).replace("-", "")
    return uid
# 按行读取文件
def read_from(path):
    file = open(path, encoding='utf8', errors='ignore')
    lines = file.readlines()
    return lines

#对字典排序,返回结果是list
def sort_dict(dict):
    dict_sort=sorted(dict.items(),key=lambda item:item[1],reverse=True)
    #print(dict_pair)
    return dict_sort

def load_dict():
    pkl_file = open("idf_dic.pkl", 'rb')
    lexicon_dic = pickle.load(pkl_file)

def dump_dict(lexicon_dic):
    idf_dic = open("idf_dic.pkl", 'wb')
    pickle.dump(lexicon_dic, idf_dic)

# List 写入文件
def write_to(path,list_file):
    file = open(path, 'a')
    for i in range(0,len(list_file)):
        file.write(str(list_file[i]))
        file.write('\n')
    file.close()
#读取一个文件夹中所有问文件
def get_all_file():
    pathDir=os.listdir("")

# 翻转字典
all_keywords_dict={}
all_keywords_dict_new = {value: key for key, value in all_keywords_dict.items()}

#读存取模型
lr=LogisticRegression()
joblib.dump(lr, "model_lr.m")
joblib.load("model_lr.m")

# 获取前days=1(参数可修改)天日期（2017-10-09 11:47:39.583927）
tic_limit = str(datetime.now() - timedelta(days=1))