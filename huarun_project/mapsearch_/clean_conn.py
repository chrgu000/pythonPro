# -*- coding: utf-8 -*
'''
更新company_connection_building,将记录中b_uid不存在的删除
'''
import pymysql
def capital_unified():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    cur_test.execute("select u_id from buildings_info ")
    uid_list=[]
    for r in cur_test.fetchall():
        uid_list.append(r[0])
    print("%%%")
    cur_test.execute("select c_id,b_uid from company_connection_building ")
    print("***")
    for r in cur_test.fetchall():
        if r[1] not in uid_list:
            print(r[0])
            cur_test.execute("delete from company_connection_building where c_id="+"\""+str(r[0])+"\"")
            conn_test.commit()

    cur_test.close()
    conn_test.close()

if __name__ == "__main__":
    capital_unified()
    pass