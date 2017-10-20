# -*- coding: utf-8 -*
#Clue_entry_Major 抽象出数值特征，存入sql

import pymysql
import time

def clean_registedtate(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql_only = "SELECT CLue_Id,registrationdate FROM crm_t_clue limit "+str(start)+","+str(banchsize)+";"
    cur_only.execute(sql_only)

    data=[]
    for row in cur_only.fetchall():
        cid = str(row[0])

        # ************registrationdate（注册时间）***************
        #存储unix时间戳，如果无，值=“-1”
        date_re = "-1"
        if len(str(row[2]).split("-")) == 3:
            timeArray = time.strptime(str(row[2]), "%Y-%m-%d")
            date_re = str(int(time.mktime(timeArray)))
            if date_re<0:date_re=0
        data.append(cid+ "#" + date_re)

    cur_only.close()
    conn_only.close()
    return data


if __name__ == '__main__':

    pass
