# -*- coding: utf-8 -*

import pymysql


def get_cid(start,end):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    file = open("no_match_1.csv", encoding='utf8', errors='ignore')
    building = file.readlines()
    for i in range(start,end):
        cid=building[i].split(",")[0]
        print(cid)
        sql_test = "delete from company_connection_building where c_id="+"\""+cid+"\""
        cur_test.execute(sql_test)
        conn_test.commit()

    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    start=0
    end=80
    for i in range(0,1):
        cid_list=get_cid(start,end)
        start=end
        end=end+100
        print(str(start)+":"+str(end))
    pass
