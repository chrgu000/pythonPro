# -*- coding: utf-8 -*

#每一个线索的描述定义成一个文档，使用LDA算法，对每一个文档分类

import time
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import jieba
import pymysql
import numpy as np

def get_oridoc():
    doc_list=[]
    conn_test = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunkedata',
                                passwd='XingDongJia@2016',
                                db='dataprocess',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    # sql_test = "SELECT id,business,product,content FROM company_yunke limit 100"
    sql_test = "SELECT id,product FROM company_yunke"
    cur_test.execute(sql_test)
    for row in cur_test.fetchall():
        doc_list.append(str(row[0])+"%"+str(row[1]))
    cur_test.close()
    conn_test.close()
    return doc_list

def get_stopwords():
    lines = open("stop_words.txt", 'r', encoding='utf8', errors='ignore')
    all_lines= lines.readlines()
    stop_list=[]
    for i in all_lines:
        stop_list.append(i.replace("\n",""))
    return stop_list

def lda_model():
    doc_list=get_oridoc()
    print(doc_list)
    doc_fenci_list = []
    doc_cid=[]
    for i in range(0,len(doc_list)):
        cid=doc_list[i].split("%")[0]
        doc=doc_list[i].split("%")[1]
        doc_cut=jieba.cut(doc)
        result=' '.join(doc_cut)
        doc_fenci_list.append(result)
        doc_cid.append(cid)

    stop_words_list=get_stopwords()

    cntVector = CountVectorizer(stop_words=stop_words_list)
    cntTf = cntVector.fit_transform(doc_fenci_list)
    lda = LatentDirichletAllocation(n_topics=500,
                                    learning_offset=50,
                                    learning_method='online',#(一般样本较多时，使用online)
                                    random_state=0)
    docres = lda.fit_transform(cntTf)
    docres.astype(np.float16)
    print(docres)
    np.save("docres",docres)

if __name__ == '__main__':
    print(time.time())
    lda_model()
    print(time.time())

    # list_file=get_oridoc()
    # List 写入文件
    # for i in range(0, len(list_file)):
    #     file = open("./infos/"+str(i)+".csv", 'a')
    #     file.write(str(list_file[i]))
    #     file.write('\n')
    # file.close()
    pass