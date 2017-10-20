#!user/bin/env python3
# -*- coding: utf-8 -*


# 提取公司简介中的关键词
import pymysql
import re
import jieba.posseg as pseg
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# from sentences_process import get_sentences_process
from sentences_process import get_local_sentences

def tf_idf_alg():
    #读取sql数据，分词
    # name_info_fenci_list=get_sentences_process()
    #直接读取本地数据，已有过一遍关键词的抽取，留下10个重要关键词
    name_info_fenci_list=get_local_sentences()
    print("分词 结束！")
    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    # 获取词袋模型中的所有词语
    # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    print(len(name_info_fenci_list))
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(name_info_fenci_list))

    print(type(tfidf))

    file=open("feature_text_local.csv",'a')
    for i in range(0,len(name_info_fenci_list)):
        file.write(str(i)+":"+"\n")
        file.write(str(tfidf[i])+"\n")
    file.close()

def text_vec_to_sql(start,end,line_list):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    weight = ""
    for i in range(start,end):
        print(line_list[i])

    for i in range(start, end):
        if ":" in line_list[i]:
            weight += ("%" + str(int(line_list[i].split(":")[0]) + 1) + ":")
        if "," in line_list[i]:
            weight += (line_list[i].split("	")[0].split(",")[1].replace(")", "") + "," + str(round(float(line_list[i].split("	")[1].replace("\n", "")), 5)) + ";")
    list_vec = weight.split("%")
    print("*************")
    print(list_vec)

    for i in range(4,len(list_vec)-1):
        companyid=list_vec[i].split(":")[0]
        c_vector = list_vec[i].split(":")[1]
        list_id=get_clueid(companyid)
        if len(list_id)>0:
            for j in range(0,len(list_id)):
                    print(companyid)
                    print(c_vector)
                    print(list_id[j])
                    update_test = "UPDATE clue_feature SET c_tfidf_vec=" + "\""+c_vector +"\""+ " where Clue_Id=" + "\"" + list_id[j] + "\""
                    try:
                        cur_test.execute(update_test)
                    except Exception as e:
                        print(e)
                    conn_test.commit()
            print("*******************")
    cur_test.close()
    conn_test.close()

def get_clueid(companyid):
    clue_list=[]
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur = conn_only.cursor()
    sql_4 = "SELECT CLue_Id FROM crm_t_clue WHERE commercialDB_id='" + companyid + "';"
    cur.execute(sql_4)
    for row in cur.fetchall():
        clue_list.append(row[0])
    cur.close()
    conn_only.close()
    return clue_list

if __name__ == '__main__':
    # tf_idf_alg()
    f = open("feature_text_local.csv", encoding='utf-8', errors='ignore')
    line_list = f.readlines()
    count=len(line_list)
    print(count)
    start=28497500
    end=28497900
    while(True):
        if start > count: break
        text_vec_to_sql(start,end,line_list)
        break
        start=(end-100)
        end=(start+1000000)
        print(str(start)+":"+str(end))

    pass


