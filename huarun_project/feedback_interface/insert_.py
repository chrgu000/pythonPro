# -*- coding: utf-8 -*

import uuid
import pymysql
import time
import sys
sys.path.append("../")
from process_ import process_building
from search_ import get_fields_infos



def insert_new_building_a(bname,info):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    uid =get_uuid(bname)
    utime = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    addr_loc=process_building(bname)
    addr=addr_loc[0]
    lng=addr_loc[1].split(",")[0]
    lat=addr_loc[1].split(",")[1]
    insert_sql="insert into buildings_info_insert(u_id,b_building_name,b_building_adr,b_lat,b_lon,b_building_introduce,update_time) VALUES ("+"\""+uid+"\""+","+"\""+bname+"\""+","+"\""+addr+"\","+"\""+lat+"\","+"\""+lng+"\","+"\""+info+"\","+"\""+utime+"\""+")"
    try:
        cur_test.execute(insert_sql)
    except Exception as e:
        print(e)
    conn_test.commit()
    cur_test.close()
    conn_test.close()

def insert_new_building_b(bname):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    uid =get_uuid(bname)
    utime = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    addr_loc=process_building(bname)
    addr=addr_loc[0]
    lng = addr_loc[1].split(",")[0]
    lat = addr_loc[1].split(",")[1]
    info=""
    insert_sql="insert into buildings_info_insert(u_id,b_building_name,b_building_adr,b_lat,b_lon,b_building_introduce,update_time) VALUES ("+"\""+uid+"\""+","+"\""+bname+"\""+","+"\""+addr+"\","+"\""+lat+"\","+"\""+lng+"\","+"\""+info+"\","+"\""+utime+"\""+")"
    try:
        cur_test.execute(insert_sql)
    except Exception as e:
        print(e)
    conn_test.commit()
    cur_test.close()
    conn_test.close()

def insert_new_conn(belong_building_name,company_name):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    uid = get_uuid(belong_building_name)
    print(uid)
    utime=str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    result=get_fields_infos(company_name).split("%")
    print(result)
    state=result[0]
    cid=result[1]
    capital=result[2]
    rdate=result[3]
    hangye=result[4]
    score=result[5]
    dis=0
    print("&&&&&&&&&&&&")
    insert_sql= "INSERT INTO company_conn_building_insert(c_id,b_uid,b_distance,c_industry,c_rdate,c_capital,score,state,update_time) VALUES("+"\""+cid+"\""+","+"\""+uid+"\""+","+"\""+dis+"\""+","+"\""+hangye+"\""+","+"\""+rdate+"\""+","+"\""+capital+"\""+","+"\""+score+"\""+","+"\""+state+"\""+","+"\""+utime+"\""+")"
    print(insert_sql)
    try:
        cur_test.execute(insert_sql)
    except Exception as e:
        print(e)
    # 大厦名称插入到 buildings_info_insert
    insert_new_building_b(belong_building_name)
    conn_test.commit()
    cur_test.close()
    conn_test.close()

def get_uuid(name):
    uid_ = uuid.uuid3(uuid.NAMESPACE_DNS, name)
    uid = str(uid_).replace("-", "")
    return uid

if __name__=='__main__':
    print(get_uuid("百度大厦员工食堂"))
    pass