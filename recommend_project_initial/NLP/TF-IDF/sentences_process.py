# -*- coding: utf-8 -*

import jieba
from sentences import get_sentences
import os

def get_stopwords():
    lines = open("stop_words.txt", 'r')
    all_lines= lines.readlines()
    stop_list=[]
    for i in all_lines:
        stop_list.append(i.replace("\n",""))
    return stop_list

def get_sentences_process():
    stop_list= get_stopwords()
    name_info_list = get_sentences()
    print("read data end!")
    name_info_fenci_list = []
    for line in name_info_list:
        com_info=line.split("%&")[0]
        if com_info=="None" or com_info=="" or len(com_info)<=1:
            com_info = line.split("%&")[1]
        # 删除括号内的内容，待做
        fenci = jieba.cut(com_info, HMM=True)
        s = ""
        for fc in fenci:
            if fc not in stop_list:
                s += (fc+ " ")
        name_info_fenci_list.append(s)
    return name_info_fenci_list

def get_local_sentences():
    all=[]
    path_dir=os.listdir("../filter_keywords")
    for file in path_dir:
        f = open("../filter_keywords/"+file,encoding='utf-8',errors='ignore')
        line_list = f.readlines()
        for line in line_list:
            all.append(line.split(":")[1])
        print("../filter_keywords/"+file+" read finish!")

    return all

if __name__ == '__main__':
    # name_info_fenci_list=get_sentences_process()
    # print(name_info_fenci_list)
    get_local_sentences()
    pass


