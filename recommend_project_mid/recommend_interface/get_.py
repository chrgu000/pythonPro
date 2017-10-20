# -*- coding: utf-8 -*

import pymysql
import numpy as np
import os

import sys
sys.path.append("../")
from fea_process import sql,feature_pro
from sklearn.externals import joblib
from generate_model.logistic_model_ import logistic_recommend
from filter_ import filter_recommend_result
from sort_ import sort_recommend_result

'''
模型评估模块
   输入:company_code,返回推荐结果
   如果用户首次使用推荐引擎，获取不到模型，则调用logistic_model_
   
'''

conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                            port=3306,
                            user='yunker',
                            passwd='yunke2016',
                            db='alg',
                            charset='utf8'
                            )
cur_test = conn_test.cursor()


def get_recommend_result(companyCode):
    has_model = True
    try:
        gbdt = joblib.load("../model/gbdt/"+companyCode+"_gbdt.m")
        gbdt_enc = joblib.load("../model/onehot/" + companyCode + "_onehot.m")
        lr = joblib.load("../model/lr/" + companyCode + "_lr.m")
        has_model_dump = True
    except Exception as e:
        has_model = False
        has_model_dump = logistic_recommend(companyCode)

    return_result = []
    if has_model is True and has_model_dump is True or has_model is False and has_model_dump is True:
        while len(return_result) < 20:
            start = get_start_loc(companyCode)
            banchsize = 5
            predict_result = model_predict(companyCode, start, banchsize)
            if type(predict_result) != str:
                result_filter = filter_recommend_result(predict_result, companyCode)

            for i in range(0, len(result_filter)):
                return_result.append(result_filter[i])
            file = open("../read_record/" + companyCode + ".txt", 'a')
            file.write(str(start+banchsize) + "\n")
            file.close()
    else:
        return_result = "-1"

    if return_result != "-1":
        result_sort = sort_recommend_result(return_result)
        result_intercept = []
        for i in range(0, 20):
            result_intercept.append(result_sort[i])
        return result_intercept
    else:
        return "-1"

def get_start_loc(companyCode):
    has_file = os.path.exists("../read_record/" + companyCode + ".txt")
    if has_file is False:
        file = open("../read_record/" + companyCode + ".txt", 'a')
        file.write("0"+"\n")
        file.close()

    file = open("../read_record/" + companyCode + ".txt")
    read_file = file.readlines()
    start = -1
    for i in range(0, len(read_file)):
        tp = int(str(read_file[i]).replace("\n", ""))
        if type(start) == int:
            start = tp
    if start + 10 > 26253697:
        os.remove("../read_record/" + companyCode + ".txt")
        return 0
    else:
        return start


def model_predict(companyCode, start, end):

    sql_ = sql() + " limit " + str(start) + "," + str(end)
    return_result = []
    gbdt = joblib.load("../model/gbdt/" + companyCode + "_gbdt.m")
    gbdt_enc = joblib.load("../model/onehot/" + companyCode + "_onehot.m")
    lr = joblib.load("../model/lr/" + companyCode + "_lr.m")
    cur_test.execute(sql_)
    predictsets = []
    cid_list = []
    for row in cur_test.fetchall():
        sample = feature_pro(row)
        if type(sample) != str:
            cid_list.append(row[14])
            predictsets.append(sample)
    predict_sets = np.array(predictsets)
    y_predict = lr.predict_proba(gbdt_enc.transform(gbdt.apply(predict_sets)[:, :, 0]))[:, 1]
    for i in range(0, len(cid_list)):
        return_result.append(cid_list[i] + ":" + str(y_predict[i]))
    return return_result

if __name__ == '__main__':

    pass