# -*- coding: utf-8 -*

'''
处理company_no_match中未匹配到的公司
'''

from company_building_smatch import get_match_building
import pymysql
import uuid

def result_to_sql():
    uid_dict=get_uuid()
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    c_match_building=get_match_building()

    delete_match_company(c_match_building)

    for i in range(0,len(c_match_building)):
        cid=c_match_building[i].split("%")[0].replace("\n","")
        m_name=c_match_building[i].split("%")[1].replace("\n","")
        m_dis=c_match_building[i].split("%")[2].replace("\n","")
        m_addr=c_match_building[i].split("%")[3].replace("\n","")
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


def delete_match_company(c_match_building):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    for i in range(0,len(c_match_building)):
        cid = c_match_building[i].split("%")[0].replace("\n", "")
        delete_test = "delete from company_no_match where c_id="+"\""+cid+"\""
        try:
            cur_test.execute(delete_test)
        except Exception as e:
            print(e)
        conn_test.commit()
    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    result_to_sql()
    pass
