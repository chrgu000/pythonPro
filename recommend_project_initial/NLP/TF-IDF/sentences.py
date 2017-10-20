# -*- coding: utf-8 -*
import pymysql
def get_sentences():
    print("开始读取数据")
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur = conn_only.cursor()
    sql_4 = "SELECT CLue_Id,param8,Clue_Entry_Com_Name FROM crm_t_clue"
    cur.execute(sql_4)
    list_info=[]
    for row in cur.fetchall():
        list_info.append(str(row[1])+"%&"+str(row[2]))
    return list_info

if __name__=='__main__':
    list_info=get_sentences()
    print(list_info)
    pass