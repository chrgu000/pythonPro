
# -*- coding: utf-8 -*
'''
连接测试alg库，读取正负样本对应的特征表
samples_label():给正负样本贴标签
feature_trans():特征转换
param：fea_len = 58

'''
import pymysql
import numpy as np
import sys
sys.path.append("../")
from fea_engineering.feature_process import sql,feature_pro


def features_engineering_test(start,num):
    conn_test = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    #准备模型的测试样本输入数据
    test_sets=[]
    sql_2=sql()+"limit "+ str(start)+","+str(num)
    cur_test.execute(sql_2)
    for row in cur_test.fetchall():
        sample = feature_pro(row)
        test_sets.append(sample)

    cid=[]
    sql_1 = "select Clue_Id from clue_feature " + "limit " + str(start) + "," + str(num)
    cur_test.execute(sql_1)
    for r in cur_test.fetchall():
       cid.append(r[0])
    cur_test.close()
    conn_test.close()
    tsets = np.array(test_sets)
    return tsets

def get_test_cid(start, num):
    conn_test = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    cid = []
    sql_1 = "select Clue_Id from clue_feature  limit " + str(start) + "," + str(num)
    cur_test.execute(sql_1)
    for r in cur_test.fetchall():
        cid.append(r[0])
    cur_test.close()
    conn_test.close()
    return cid

def get_samples(cid_list):
    row_list=[]
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur = conn_only.cursor()
    for i in range(0,len(cid_list)):
        sql = "SELECT * FROM crm_t_clue WHERE CLue_Id='" + cid_list[i] + "';"
        cur.execute(sql)
        for row in cur.fetchall():
            row_list.append(row)
    return row_list

if __name__ == '__main__':
    pass
