# -*- coding: utf-8 -*

import pymysql

def delete_match_company(start,end):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    file = open("no_match.csv", encoding='utf8', errors='ignore')
    building = file.readlines()
    for i in range(start,end):
        cid = building[i].split(",")[0]
        insert_test = "insert into company_no_match(c_id) VALUES  (" + "\"" + cid + "\""  ")"
        try:
            cur_test.execute(insert_test)
        except Exception as e:
            print(e)
        conn_test.commit()
    cur_test.close()
    conn_test.close()


if __name__=='__main__':
    start=0
    end=82287
    delete_match_company(start, end)
    pass
