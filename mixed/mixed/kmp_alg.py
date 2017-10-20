# -*- coding: utf-8 -*

import pymysql
import logging
import re
import jieba
import math
import jieba.posseg as pseg


def get_classes_library():
    fenci_list=[]
    text = open("classes.txt", 'r', encoding='utf8', errors='ignore')
    all_lines = text.readlines()
    all_str=""
    for line in all_lines:
        line_filter = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\(\)\=\|\{\}\'\:\、\;\'\[\]\.\ \<\>\/\?\~\��\※\@\#\\\&\%\--\_\��\:\）\（\《\》]", "", line)
        all_str+=(line_filter.replace("\t",""))
    all_list=all_str.split("*")
    for lists in all_list:
        dicts={}
        fenci=pseg.cut(lists, HMM=True)
        for fc in fenci:
            if fc.word not in dicts:dicts[fc.word]=1
            else: dicts[fc.word]+=1
        fenci_list.append(dicts)
    return fenci_list

def get_fields(fenci_list):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur = conn_only.cursor()

    sql ="SELECT com_info,param8,main_produce FROM crm_t_clue limit 10"
    cur.execute(sql)
    for row in cur.fetchall():
        content=(str(row[0])+str(row[1])+str(row[2]))
        keywords_list=[]
        fenci = pseg.cut(content, HMM=True)
        clue_list=[]
        for f in fenci:
            clue_list.append(f.word)
        for i in range(0,len(fenci_list)):
            fenci_dict=fenci_list[i]
            #print(fenci_dict)
            keywords = ""
            unuse=""
            for c in clue_list:
                if c in fenci_dict.keys(): keywords += (c+"")
                else:unuse+=(c+",")
            print(str(i)+":"+keywords.replace(" ，","").replace("，",""))
            #print(unuse)

            #keywords_list.append(keywords)
        print("**********************************")



# # 对子串加以预处理，找到匹配失败时子串回退的位置
# def preprocess(patter):
#     length = len(patter)
#     p = handlerList(length)
#     j = -1
#     p[0] = j
#     for i in range(1, length):
#         j = p[i - 1]
#         while j >= 0 and patter[i] != patter[j + 1]:
#             j = p[j]
#
#         if patter[i] == patter[j + 1]:  # 含有重复字符时，回退的位置+1
#             p[i] = j + 1
#         else:
#             p[i] = -1
#     return p
#
#
# # 初始化一个元组
# def handlerList(len, default=0):
#     if len <= 0:
#         return
#     p = []
#     for i in range(len):
#         p.append(default)
#     return p
#
#
# def kmp(value, pattern):
#     srcSize = len(value)
#     subSize = len(pattern)
#     p = preprocess(pattern)
#     tIndex, pIndex, total = 0, 0, 0
#     while tIndex < srcSize and pIndex < subSize:  # 找到合适的回退位置
#         if (value[tIndex] == pattern[pIndex]):
#             tIndex += 1
#             pIndex += 1
#         elif pIndex == 0:
#             tIndex += 1
#         else:
#             pIndex = p[pIndex - 1] + 1
#
#         if pIndex == subSize:  # 输出匹配结果，并且让比较继续下去
#             pIndex = 0
#             total += 1
#             print('find', pattern, 'at', (tIndex - subSize))
#     print('find times ', total)

if __name__=='__main__':
    fenci_list =get_classes_library()
    # for dic in fenci_list:
    #     print(dic)
    get_fields(fenci_list)

    pass