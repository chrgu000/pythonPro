# -*- coding: utf-8 -*
#定时更新模型：维护每一个客户推荐模型，非实时生成，只有用户在当天使用时，模型会在当天凌晨更新

import time
from threading import Timer
import os
import sys
sys.path.append("../")
sys.path.append("../..")
from recommend_model.logistic_model_ import logistic_recommend

def function():
    print("start time:"+str(time.time()))
    file = open("../../model/cur_company.txt", encoding='utf8', errors='ignore')
    company_list = file.readlines()
    company_dict = {}
    for c in company_list:
        c = c.replace("\n", "")
        if c not in company_dict.keys():
            company_dict[c] = 1
        else:
            company_dict[c] += 1
    for k, v in company_dict.items():
        print(k)
        logistic_recommend(k)
    print("end time:" + str(time.time()))
    os.remove("../../model/cur_company.txt")
    t = Timer(24*3600, function)
    t.start()

if __name__ == "__main__":
    time.sleep(8*3600)
    function()

