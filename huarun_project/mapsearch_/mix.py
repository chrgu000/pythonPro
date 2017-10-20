# -*- coding: utf-8 -*
'''
buildings_info_insert清洗建筑物，改建筑物在buildings_info则从buildings_info_insert中删除
'''

import pymysql
def delete_building():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    cur_test.execute("select b_building_name from buildings_info ")
    building_list=[]
    for r in cur_test.fetchall():
        building_list.append(r[0])
    cur_test.close()
    conn_test.close()

    conn_test_1 = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test_1 = conn_test_1.cursor()
    cur_test_1.execute("select b_building_name from buildings_info_insert")
    for r in cur_test_1.fetchall():
        if r[0] in building_list:
            cur_test_1.execute("delete from buildings_info_insert where b_building_name="+"\""+r[0]+"\"")
            print(r[0])
            conn_test_1.commit()

    cur_test_1.close()
    conn_test_1.close()

if __name__ == "__main__":
    delete_building()
    pass