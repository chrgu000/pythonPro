#!user/bin/env python3
# -*- coding: utf-8 -*

# 公司名称关键词提取
# 2017/5/26
import re
import jieba.posseg as pseg
import pymysql
import sys
sys.path.append("../")
from company_intoduce import get_company_introduce

conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                          port=3306,
                          user='yunkedata',
                          passwd='XingDongJia@2016',
                          db='dataprocess',
                          charset='utf8'
                          )
cur_gs = conn_gs.cursor()

# 连接数据库，获取数据
def getdata_from_sql():
    lexicon_dict = {}
    lexicon_dict = get_company_introduce(0, 100, lexicon_dict)
    print(lexicon_dict)
    cur_gs.execute("SELECT title,business,product,content FROM company_yunke limit 1")
    for r in cur_gs.fetchall():
        # jieba分词，并给出词性
        useful_words = []
        company_introduce = ""
        for i in range(0, 4):
            if r[i] != None:
                company_introduce += r[i]
        introduce_words = pseg.cut(company_introduce, HMM=True)
        for iw in introduce_words:
            if iw.flag == "n" or iw.flag == "nz":
                useful_words.append(iw.word)
        words_sort = sort_dict(useful_words)
        print(words_sort)
        for i in range(0, len(words_sort)):
            print(words_sort[i][0]+":" + str(words_sort[i][1]/lexicon_dict[words_sort[i][0]]))

    cur_gs.close()
    conn_gs.close()


def sort_dict(useful_words):
    words_dict = {}
    for i in range(0, len(useful_words)):
        if useful_words[i] not in words_dict:
            words_dict[useful_words[i]] = 1
        else:
            words_dict[useful_words[i]] += 1
    words_sort = sorted(iter(words_dict.items()), key=lambda s: s[1], reverse=True)
    return words_sort


if __name__ == '__main__':
    getdata_from_sql()
    pass