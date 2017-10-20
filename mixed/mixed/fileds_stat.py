# -*- coding: utf-8 -*

import pymysql
import logging

#统计每一个字段包含的值，统计出每一个值占的比例

log_file = "feature_table.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG)

def get_fields_stat():
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur = conn_only.cursor()

    major_all={}
    sql ="SELECT Clue_Entry_Major FROM crm_t_clue"
    cur.execute(sql)
    for row in cur.fetchall():
        if str(row[0]) in major_all:
            major_all[str(row[0])]+=1
        else:
            major_all[str(row[0])]=1
    cur.close()
    conn_only.close()

    file = open("com_major_2.csv", 'a')
    for k,v in major_all.items():
        file.write(str(k) + "*#@&" + str(v))
        file.write('\n')
    file.close()


if __name__ == '__main__':
    get_fields_stat()
    pass