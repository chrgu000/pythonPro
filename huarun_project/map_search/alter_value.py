# -*- coding: utf-8 -*
'''
字段内容修改
'''

import pymysql

# 将c_industry,c_rdate,c_capital字段中的“无”改为“保密”
def change_():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select c_id,c_industry,c_rdate,c_capital from company_connection_building")
    for row in cur_test.fetchall():
        if row[1] == "无":
            cur_test.execute("update company_connection_building set c_industry="+"\""+"保密"+"\""+" where c_id=" +"\""+row[0]+"\"")
        if row[2] == "无":
            cur_test.execute("update company_connection_building set c_rdate="+"\""+"保密"+"\""+" where c_id=" +"\""+row[0]+"\"")
        if row[3] == "无":
            cur_test.execute("update company_connection_building set c_capital="+"\""+"保密"+"\""+" where c_id=" +"\""+row[0]+"\"")
        conn_test.commit()

    conn_test.close()
    cur_test.close()

# 将value="0 万元" 修改为null
def change_capital():
    conn_test_yunketest()



def conn_test_yunketest():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    return conn_test

if __name__ == '__main__':
    change_()
    print()
    print("##")
    pass
