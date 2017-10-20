#!user/bin/env python3
# -*- coding: utf-8 -*

# 获取公司的介绍数据

import pymysql
import jieba.posseg as pseg

# 连接数据库，获取数据
def get_company_introduce(start, end, lexicon_dict):
    conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                              port=3306,
                              user='yunkedata',
                              passwd='XingDongJia@2016',
                              db='dataprocess',
                              charset='utf8'
                              )
    cur_gs = conn_gs.cursor()
    cur_gs.execute("SELECT title,business,product,content FROM company_yunke limit "+"\""+start+"\""+","+"\""+end+"\"")
    for r in cur_gs.fetchall():
        # jieba分词，并给出词性
        useful_words = {}
        company_introduce = ""
        for i in range(0, 4):
            if r[i] != None:
                company_introduce += r[i]
        introduce_words = pseg.cut(company_introduce, HMM=True)
        for iw in introduce_words:
            if iw.flag == "n" or iw.flag == "nz":
                if iw.word not in useful_words.keys():
                    useful_words[iw.word] = 1
        for k, v in useful_words.items():
            if k not in lexicon_dict:
                lexicon_dict[k] = 1
            else:
                lexicon_dict[k] += 1
    cur_gs.close()
    conn_gs.close()
    return lexicon_dict

if __name__ == '__main__':
    pass