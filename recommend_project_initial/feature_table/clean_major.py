# -*- coding: utf-8 -*
#Clue_entry_Major 抽象出数值特征，存入sql

import pymysql
import time
import datetime
import math

major = open("./convert_standard/major.txt", 'r', encoding='utf8', errors='ignore')
all_lines = major.readlines()
all_major=[]

for line in all_lines:
    all_major.append(line.replace("\n",""))

def clean_major(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql_only = "SELECT CLue_Id,Clue_Entry_Major FROM crm_t_clue limit "+str(start)+","+str(banchsize)+";"
    cur_only.execute(sql_only)

    data=[]
    for row in cur_only.fetchall():
        cid = str(row[0])
        #************Clue_Entry_Major（联系人职位）************
        #如果无，值=“-1”
        major=str(row[1])
        major_show="-1"
        if major in all_major:
            major_show=str(all_major.index(major)+1)

        data.append(cid+"#"+major_show)

    cur_only.close()
    conn_only.close()
    return data

if __name__ == '__main__':

    pass
