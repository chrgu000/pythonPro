# -*- coding: utf-8 -*
#Clue_entry_Major 抽象出数值特征，存入sql

import pymysql
import time
import datetime
import math

major = open("major.txt", 'r', encoding='utf8', errors='ignore')
all_lines = major.readlines()
all_major=[]

for line in all_lines:
    all_major.append(line.replace("\n",""))

def clue_clean(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql_only = "SELECT CLue_Id,Clue_Entry_Major,registrationdate FROM crm_t_clue limit "+str(start)+","+str(banchsize)+";"
    cur_only.execute(sql_only)

    data=[]
    for row in cur_only.fetchall():
        cid = str(row[0])
        #************Clue_Entry_Major（联系人职位）************
        #如果无，值=“-1”
        major=str(row[1])
        major_show="-1"
        if major in all_major: major_show=str(all_major.index(major)+1)

        # ************registrationdate（注册时间）***************
        #存储unix时间戳，如果无，值=“-1”
        date_re = "-1"
        if len(str(row[2]).split("-")) == 3:
            timeArray = time.strptime(str(row[2]), "%Y-%m-%d")
            date_re = str(int(time.mktime(timeArray)))
            if date_re<0:date_re=0
        data.append(cid+"#"+major_show+ "#" + date_re)

    cur_only.close()
    conn_only.close()
    return data

def updata(data):
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
        major_show=data[i].split("#")[1]
        date_regi = data[i].split("#")[2]
        #update_test="UPDATE clue_feature SET "+"contact_major="+ major_show+","+"registration_date_timestamp="+ date_regi +" where Clue_Id="+"\""+clueid+"\""
        update_test="UPDATE clue_feature SET "+"c_reg_date="+date_regi +" where Clue_Id="+"\""+clueid+"\""
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()


if __name__ == '__main__':
    start=0
    banchsize=100000
    while(True):
        data = clue_clean(start,banchsize)
        if len(data)==0:break
        updata(data)
        start+=banchsize
        print("第"+str(start)+"完成")
    pass
