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

def get_buindings():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    sql_test = "select u_id,b_building_name from buildings_info"
    building_uid = []
    building_name=[]
    cur_test.execute(sql_test)

    for row in cur_test.fetchall():
        building_name.append(row[1])
        building_uid.append(row[0])

    for k in range(0,len(building_uid)):
        print(str(k))
        uid=building_uid[k]
        name=building_name[k]
        key0 = "79d9804060d5aa9457e139ab0efcbcd3"
        url1 = "http://restapi.amap.com/v3/geocode/geo?key=" + key0 + "&address=" + parse.quote(name)
        url="http://restapi.amap.com/v3/place/text?key="+key0+"&keywords="+ parse.quote(name)+"&types="+ parse.quote("商务住宅;住宅区;住宅区;商务住宅;楼宇;商务写字楼商务住宅;产业园区;产业园区;小区")+"&city="+parse.quote("北京")+"&children=1&offset=20&page=1&extensions=all"
        json_geo = get_builds(url)
        try:
            pois_num=json_geo["count"]
            if int(pois_num)>=1:
                name_j=json_geo["pois"][0]["name"]
                loc=json_geo["pois"][0]["location"]
                f = open("building_tel.csv", "a", encoding="utf-8", errors="ignore")
                tel=json_geo["pois"][0]["tel"]
                f.write(name + "*" + str(tel) + "\n")
                f.close()
                if name==name_j or name in name_j or name_j in name:
                    lon=loc.split(",")[0]
                    lat=loc.split(",")[1]
                    # update="update buildings_info SET b_lat="+"\""+lat+"\""+","+"b_lon="+"\""+lon+"\""+" where u_id="+"\""+uid+"\""
                    # cur_test.execute(update)
                    # conn_test.commit()
                else:
                    f1 = open("building_lon.csv", "a", encoding="utf-8", errors="ignore")
                    f1.write(name+"*"+name_j+"*"+loc+"\n")
                    f1.close()
        except Exception as e:
            print(json_geo)
    cur_test.close()
    conn_test.close()
    return building_uid

def get_builds(url):
    while True:
        try:
            record_req = req.urlopen(url, timeout=10)
            hjson = json.loads(record_req.read().decode("utf_8"))
            if hjson["status"]=="1":
                return(hjson)
                break
        except:
            print("data is null!")


# 更新buildings_info字段中b_property_tel字段，电话信息从高德地图获取
def update_tel():
    f=open("building_tel.csv",encoding="utf-8",errors="ignore")
    all_line=f.readlines()
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    for k in range(0,len(all_line)):
        b_name=all_line[k].split("*")[0]
        tel=all_line[k].split("*")[1]
        if "[" not in tel and len(tel)>5:
            update_tel_sql="update buildings_info set b_property_tel="+"\""+tel+"\""+" where b_building_name="+"\""+b_name+"\""
            cur_test.execute(update_tel_sql)
    conn_test.commit()
    cur_test.close()
    conn_test.close()

def update_loc():
    f = open("building_loc.txt", encoding="utf-8", errors="ignore")
    all_line = f.readlines()
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    for k in range(0, len(all_line)):
        b_name = all_line[k].split("*")[0]
        lon = all_line[k].split("*")[2].split(",")[0]
        lat= all_line[k].split("*")[2].split(",")[1]
        update_tel_sql = "update buildings_info set b_lat=" + "\"" + lat + "\","+"b_lon="+"\""+lon+"\"" + " where b_building_name=" + "\"" + b_name + "\""
        cur_test.execute(update_tel_sql)
    conn_test.commit()
    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    # get_buindings()
    # update_tel()
    # update_loc()
    ss = datetime.now() - timedelta(days=2)
    print(str(ss))
    pass