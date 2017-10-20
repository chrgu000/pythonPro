# -*- coding: utf-8 -*

'''
处理得到的数据：新增建筑物；新增的匹配线索
c_company_building（能匹配到建筑物的公司）
c_no_match_building（不能匹配到建筑物的公司），将公司id存入company_no_match表
'''

from company_building_match import get_match_building
import pymysql
import uuid

def result_to_sql(city, time):
    uid_dict=get_uuid()
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    c_building=get_match_building(city, time)
    c_company_building=c_building[0]
    print(c_company_building)
    c_no_match_building=c_building[1]
    print(c_no_match_building)
    insert_no_match_company(c_no_match_building)

    for i in range(0,len(c_company_building)):
        cid=c_company_building[i].split("%")[0].replace("\n","")
        m_name=c_company_building[i].split("%")[1].replace("\n","")
        m_dis=c_company_building[i].split("%")[2].replace("\n","")
        m_addr=c_company_building[i].split("%")[3].replace("\n","")
        uid = uuid.uuid3(uuid.NAMESPACE_DNS, m_name)
        u_id = str(uid).replace("-", "")

        if u_id not in uid_dict.keys():
            insert_test_b = "insert into buildings_info(u_id,b_building_name,b_building_adr) VALUES (" + "\"" + u_id + "\"," + "\"" + m_name + "\"," +"\""+ m_addr+"\""+ ")"
            insert_test_c="insert into company_connection_building(c_id,b_uid,b_distance) VALUES  (" + "\"" + cid + "\"," + "\"" + u_id + "\"," +"\""+ m_dis+"\""+ ")"
            try:
                cur_test.execute(insert_test_b)
                cur_test.execute(insert_test_c)
            except Exception as e:
                print(e)
        else:
            insert_test_c = "insert into company_connection_building(c_id,b_uid,b_distance) VALUES  (" + "\"" + cid + "\"," + "\"" + u_id + "\"," + "\"" + m_dis + "\"" + ")"
            try:
                cur_test.execute(insert_test_c)
            except Exception as e:
                print(e)

        conn_test.commit()
    cur_test.close()
    conn_test.close()

def get_uuid():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    sql_test = "select u_id from buildings_info"
    building_uid = {}
    cur_test.execute(sql_test)
    for row in cur_test.fetchall():
        building_uid[row[0]] = 1
    cur_test.close()
    conn_test.close()
    return building_uid


def insert_no_match_company(c_no_match_building):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    for i in range(0,len(c_no_match_building)):
        insert_test = "insert into company_no_match(c_id) VALUES  (" + "\"" + c_no_match_building[i] + "\""  + ")"
        try:
            cur_test.execute(insert_test)
        except Exception as e:
            print(e)
        conn_test.commit()
    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    result_to_sql("北京市","")
    pass
