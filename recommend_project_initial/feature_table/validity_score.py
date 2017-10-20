# -*- coding: utf-8 -*
'''
线索有效性分数评价，通过被打线索次数和被打线索时间
get_validity():计算有效性评分
get_cid_time():获取被打线索的次数，被打时间时间
updata_validity（）：更新特征表clue_feature，更新有效性字段validity_score
'''

import pymysql
from time import time
from time import localtime
from datetime import datetime
import math

space = "%*"
def get_cid_time():
    clue_info=[]
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    sql="select call_date,call_type,clue_id from call_record"
    cur_test.execute(sql)
    for row in cur_test.fetchall():
        clue_info.append(str(row[0]) +space+ str(row[1])+ space + row[2])
    cur_test.close()
    conn_test.close()
    return clue_info

def get_validity():
    availability_dict_int={}
    clue_dict={}
    clue_info=get_cid_time()
    for i in range(0,len(clue_info)):
        cid=clue_info[i].split(space)[2]
        if cid in clue_dict:clue_dict[cid]+=("#"+clue_info[i])
        else: clue_dict[cid]=clue_info[i]

    for key, value in clue_dict.items():
        clue_count = value.split("#")
        x_score = 0
        has_error = False

        for i in range(0,len(clue_count)):
            tm = clue_count[i].split(space)[0]
            typ = clue_count[i].split(space)[1]
            if typ == "None" or typ == "":
                typ = 1
            if typ == 3:
                has_error = True

            cur_time = str(localtime(time()))
            c_year = int(cur_time.split("(")[1].split(",")[0].split("=")[1])
            c_month = int(cur_time.split("(")[1].split(",")[1].split("=")[1])
            l_year = int(tm.split("-")[0])
            l_month = int(tm.split("-")[1])
            if c_year == l_year:
                t_diff = c_month
            else:
                t_diff = (c_year - l_year - 1) * 12 + (12 - l_month) + c_month
            x_score += float(1 / (t_diff + 1))

        if has_error == False:
            score=math.pi/2 - math.atan(x_score)
        else:
            score=math.pi/2 - math.atan(100)
        availability_dict_int[key] = int((score/(math.pi/2))*100)
    updata_validity(availability_dict_int)

def updata_validity(availability_dict_int):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    for k,v in availability_dict_int.items():
        clueid = k
        validity=v
        dt = datetime.now()
        curtime = str(dt.strftime('%Y-%m-%d %H:%M:%S'))
        update_test = "UPDATE clue_feature SET validity_score=" + str(validity)+","+"update_time="+"\""+curtime+"\"" + " where Clue_Id=" + "\"" + clueid + "\""
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()

if __name__=='__main__':
    get_validity()
    pass