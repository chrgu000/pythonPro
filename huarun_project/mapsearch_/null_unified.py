import pymysql
'''
字段中有些是null字符，将这些字段修改为空
'''
def get_buildings():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    sql_test = "select u_id from buildings_info where b_building_developer="+"\""+"null"+"\""
    building_uid = []
    cur_test.execute(sql_test)
    for row in cur_test.fetchall():
        print(row[0])
        cur_test.execute("UPDATE buildings_info SET b_building_developer="+"\""+"\""+" WHERE u_id="+"\""+row[0]+"\"")
        conn_test.commit()
    conn_test.close()
    cur_test.close()
    return building_uid

if __name__=='__main__':
    get_buildings()
    pass