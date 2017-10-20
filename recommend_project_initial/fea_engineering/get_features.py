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

def feature_trans(pos_sam_id,neg_sam_id):
    print("训练正样本个数：" + str(len(pos_sam_id)))
    print("训练负样本个数：" + str(len(neg_sam_id)))
    print("训练样本个数：" + str(len(pos_sam_id)+len(neg_sam_id)))

    trainset_id=[]
    for i in range(0,len(pos_sam_id)):
        trainset_id.append(pos_sam_id[i])
    for i in range(0,len(neg_sam_id)):
        trainset_id.append(neg_sam_id[i])

    #准备模型的训练样本输入数据
    train_sets=[]
    for i in range(0,len(trainset_id)):
        cid=trainset_id[i]
        sql_1=sql()+"where Clue_Id="+ "\""+str(cid)+"\""
        cur_test.execute(sql_1)
        sample=[]
        for row in cur_test.fetchall():
            sample=feature_pro(row)
        train_sets.append(sample)
    trainsets=np.array(train_sets)
    print("训练集数据样本数，特征数："+str(trainsets.shape))
    # cur_test.close()
    # conn_test.close()
    return trainsets


def samples_label(pos_sam_id, neg_sam_id):
    labels = np.zeros((len(pos_sam_id) + (len(neg_sam_id)), 1))
    for i in range(0, len(pos_sam_id)):
        labels[i,0] = 1
    print("labels数组长度："+ str(labels.shape))
    return labels

if __name__=='__main__':
    #code="yunkecn"
    code="13"
    print("开始公司:" + code + "的训练正样本搜集 ing")
    pos_sam_id=get_pos_trainset(code)
    print("训练正样本:"+str(len(pos_sam_id)))

    print("开始公司:" + code + "的训练负样本搜集 ing")
    neg_sam_id =get_neg_trainset(code)
    print("训练负样本:"+str(len(neg_sam_id)))

    print("模型输入的特征向量")
    feature_trans(pos_sam_id,neg_sam_id)
    print("对应特征向量的label")
    samples_label(pos_sam_id, neg_sam_id)
    pass