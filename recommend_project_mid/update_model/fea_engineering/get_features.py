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

conn_test = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
cur_test = conn_test.cursor()

def feature_trans(pos_sam_id, neg_sam_id):
    labels = []
    trainset_id = []
    for i in range(0, len(pos_sam_id)):
        trainset_id.append(pos_sam_id[i])
    for i in range(0, len(neg_sam_id)):
        trainset_id.append(neg_sam_id[i])

    # 准备模型的训练样本输入数据
    train_sets = []
    for i in range(0, len(trainset_id)):
        cid = trainset_id[i]
        sql_1 = sql()+"where Clue_Id=" + "\""+str(cid)+"\""
        cur_test.execute(sql_1)
        for row in cur_test.fetchall():
            sample = feature_pro(row)
            # 判断sample的格式是否可转化成np.array
            if type(sample) != str:
                train_sets.append(sample)
                if i < len(pos_sam_id):
                    labels.append("1")
                else:
                    labels.append("0")
    trainsets = np.array(train_sets)
    labels = np.array(labels)

    results = []
    results.append(trainsets)
    results.append(labels)

    # cur_test.close()
    # conn_test.close()
    return results

if __name__ == '__main__':
    pass