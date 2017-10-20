#!user/bin/env python3
# -*- coding: utf-8 -*


# 提取公司简介中的关键词
import pymysql
import re
import jieba.posseg as pseg
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import os
import pickle

def dump_dict(all_keywords_dict):
    idf_dic = open("all_keywords_dict.pkl", 'wb')
    pickle.dump(all_keywords_dict, idf_dic)

def get_local_sentences():
    count=1
    all_keywords_dict={}
    path_dir=os.listdir("../filter_keywords")
    for file in path_dir:
        f = open("../filter_keywords/"+file,errors='ignore')
        line_list = f.readlines()
        for line in line_list:
            keyword_list=line.split(":")[1].split(" ")
            for k in keyword_list:
                if k not in all_keywords_dict:
                    all_keywords_dict[k]=count
                    count+=1
        print("../filter_keywords/"+file+" read finish!")

    print(count)
    dump_dict(all_keywords_dict)


def conver_to_vec():
    pkl_file = open("all_keywords_dict.pkl", 'rb')
    all_keywords_dict = pickle.load(pkl_file)
    path_dir = os.listdir("../filter_keywords")
    for file in path_dir:
        company_vec_list = []
        f = open("../filter_keywords/"+file, errors='ignore')
        line_list = f.readlines()
        for k in range(0,len(line_list)):
            company_vec=line_list[k].split(":")[0]+":"
            keyword_list = line_list[k].split(":")[1].split(" ")
            for i in range(0,len(keyword_list)):
                if keyword_list[i]!=" " and keyword_list[i]!=""  and keyword_list[i]!="\n":
                    if keyword_list[i] in all_keywords_dict.keys():
                        company_vec+=(str(all_keywords_dict[keyword_list[i]])+",")
            company_vec_list.append(company_vec)
        write_to("../vector/vector_"+file,company_vec_list)
        print("../filter_keywords/keyword"+file)

# List 写入文件
def write_to(path,list_file):
    file = open(path, 'a',encoding='utf-8',errors='ignore')
    for i in range(0,len(list_file)):
        file.write(str(list_file[i]))
        file.write('\n')
    file.close()

if __name__ == '__main__':
    # get_local_sentences()
    # conver_to_vec()
    pkl_file = open("all_keywords_dict.pkl", 'rb')
    all_keywords_dict = pickle.load(pkl_file)
    print(len(all_keywords_dict))
    pass


