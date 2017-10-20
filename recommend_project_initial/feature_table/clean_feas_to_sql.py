# -*- coding: utf-8 -*
'''
将处理过的标准的字段更新到clue_feature表
'''

import pymysql
import sys
sys.path.append("../")
from clean_capital import clean_capital
from clean_com_site import clean_comsite
from clean_com_type import clean_comtype
from clean_employees_num import clean_employees
from clean_registed_date import clean_registedtate
from clean_major import clean_major
from clean_location import clean_location

def update_data():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    for i in range(0,len(data)):
        clueid=data[i].split("#")[0]
        comtype=data[i].split("#")[1]
        comsite=data[i].split("#")[2]
        employees_max=data[i].split("#")[1]
        employees_min=data[i].split("#")[2]
        employees_mean=data[i].split("#")[3]

        update_test = "UPDATE clue_feature SET c_employees_max=" + employees_max + " where Clue_Id=" + "\"" + clueid + "\""
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()

if __name__ == '__main__':

    start = 0
    banchsize = 100000
    while (True):
        data = clean_employees(start, banchsize)
        if len(data) == 0: break
        update_data(data)
        start += banchsize
        print("第" + str(start) + "完成")

    pass
