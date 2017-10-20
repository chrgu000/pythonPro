# -*- coding: utf-8 -*
'''
根据楼宇名称，关键词搜索api，返回经纬度，存储到clue_feature b_lon,b_lat
'''
import pymysql
import urllib.request as req
import urllib.parse as parse
import json
import time
from datetime import datetime
from datetime import timedelta

conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                            port=3306,
                            user='yunker',
                            passwd='yunke2016',
                            db='yunketest',
                            charset='utf8'
                            )
cur_test = conn_test.cursor()

def get_buindings():

    sql_test = "select u_id,b_building_name,b_building_adr from buildings_info where b_lat<39  limit 3"
    building_uid = []
    building_name=[]
    building_addr=[]
    cur_test.execute(sql_test)

    for row in cur_test.fetchall():
        building_name.append(row[1])
        building_uid.append(row[0])
        building_addr.append(row[2])

    for k in range(0,len(building_uid)):
        uid=building_uid[k]
        name=building_name[k]
        addr=building_addr[k]

        key0 = "nPPBW9xruVM07MG5B3QLqjpwoPCLtP6E"
        url1 ="http://api.map.baidu.com/geocoder/v2/?&callback=renderOption&output=json&address="+parse.quote(name)+"&city="+parse.quote("北京市")+"&ak="+key0
        print(url1)
        # url2 ="http://api.map.baidu.com/geocoder/v2/?&callback=renderOption&output=json&address="+parse.quote(addr)+"&city="+parse.quote("北京市")+"&ak="+key0

        json_geo = get_builds(url1)
        if json_geo["status"]==1:
            #json_geo = get_builds(url2)
            print("**************北京 " + name)
        else:
            lng=str(json_geo["result"]["location"]["lng"])
            lat=str(json_geo["result"]["location"]["lat"])
            print(str(k) + ":" + uid + ":" + name+":"+lng+":"+lat)
            update_loc(lng,lat,uid)

    cur_test.close()
    conn_test.close()


def get_builds(url1):
    try:
        record_req = req.urlopen(url1, timeout=5)
        result=record_req.read().decode("utf_8").replace("renderOption&&renderOption","").replace("(","").replace(")","")
        hjson = json.loads(result)
        return(hjson)
    except Exception as e:
        print("")


def update_loc(lon,lat,uid):
    #39.9058047754,116.1469652445
    # lon = "116.1469652445"
    # lat= "39.9058047754"
    update_tel_sql = "update buildings_info set b_lat=" + "\"" + lat + "\","+"b_lon="+"\""+lon+"\"" + " where u_id=" + "\"" + uid + "\""
    cur_test.execute(update_tel_sql)
    conn_test.commit()

def clean_data():
    uuid_dict={}
    cur_test.execute("SELECT u_id FROM buildings_info")
    for r in cur_test.fetchall():
        uuid_dict[r[0]]=1
    print("%%%%")
    cur_test.execute("select b_uid from company_connection_building")
    for r1 in cur_test.fetchall():

        if r1[0] not in uuid_dict.keys():
            cur_test.execute("delete from company_connection_building where b_uid="+"\""+r1[0]+"\"")
            print("**:"+r1[0])
            conn_test.commit()
        else:
            print(r1[0])
    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    # get_buindings()
    # clean_data()
    pass