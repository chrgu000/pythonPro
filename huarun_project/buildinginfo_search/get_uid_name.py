# -*- coding: utf-8 -*

import pymysql

def get_cid():

    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    file = open("b_uid.csv", encoding='utf8', errors='ignore')
    building = file.readlines()
    file_save = open("uic_name_count.csv", 'a')
    for i in range(0,len(building)):
        uid=building[i].split(",")[0]
        c_count=building[i].split(",")[1].replace("\n","")
        sql_test = "select b_building_name from buildings_info where u_id="+"\""+uid+"\""
        cur_test.execute(sql_test)
        for r in cur_test.fetchall():
            ss=uid+"%"+str(c_count)+"%"+r[0]
            print(ss)
            file_save.write(ss)
            file_save.write('\n')
    file_save.close()

    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    get_cid()
    pass
