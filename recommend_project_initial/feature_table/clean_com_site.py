# -*- coding: utf-8 -*
'''
抽象出可计算向量，存入特征表，其中原始字段：com_site
'''

import pymysql

def clean_comsite(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql_only = "SELECT CLue_Id,com_site FROM crm_t_clue limit "+str(start)+","+str(banchsize)+";"
    cur_only.execute(sql_only)

    data=[]
    for row in cur_only.fetchall():
        clueid = str(row[0])

        #**********com_site(网址)**************
        #有网址，值=1；无网址=0
        comsite = '0'
        if row[1] != "" and row[1] != 'None':
            comsite = '1'

        data.append(clueid+"#"+comsite)
    cur_only.close()
    conn_only.close()
    return data

if __name__ == '__main__':

    pass
