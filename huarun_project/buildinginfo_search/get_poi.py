# -*- coding: utf-8 -*
import pymysql
import urllib.request as req
import urllib.parse as parse
import json

def get_allpoi():
    key0 = "nPPBW9xruVM07MG5B3QLqjpwoPCLtP6E"
    lat_s = 39.8000
    lat_e = 39.8100
    for i in range(0,100):
        lon_s = 116.2000
        lon_e = 116.2100
        for j in range(0,100):
            print(lat_s)
            print(lon_s)
            print(lat_e)
            print(lon_e)
            url = "http://api.map.baidu.com/place/v2/search?query="+parse.quote("房地产")+"&bounds="+str(lat_s)+","+str(lon_s)+","+str(lat_e)+","+str(lon_e)+"&output=json&ak="+key0
            print(url)
            json_geo = get_builds(url)
            print(json_geo)

            file = open("poi.csv", 'a')
            file.write(str(json_geo))
            file.write('\n')
            file.close()
            lon_s = lon_e
            lon_e = lon_e+0.01
        lat_s = lat_e
        lat_e = lat_e+0.01

def get_builds(url1):
    try:
        record_req = req.urlopen(url1, timeout=5)
        result=record_req.read().decode("utf_8").replace("renderOption&&renderOption","").replace("(","").replace(")","")
        hjson = json.loads(result)
        return(hjson)
    except Exception as e:
        print("")

def analysis_poi():
    file = open("poi.csv", encoding="utf-8",errors='ignore')
    lines = file.readlines()
    for i in range(155,len(lines)):
        print(i)
        if len(lines[i])>10:
            ss=lines[i].replace("\n","")
            hjson = json.loads(ss)
            for j in range(0,len(hjson["results"])):
                ss="uid:"+hjson["results"][j]["uid"]+";"+"name:"+hjson["results"][j]["name"]+";"+"address:"+hjson["results"][j]["address"]+";"+"lat:"+str(hjson["results"][j]["location"]["lat"])+";"+"lng:"+str(hjson["results"][j]["location"]["lng"])
                print(ss)
                file = open("poic.csv", 'a')
                file.write(ss)
                file.write('\n')
                file.close()
def insert_poi():
    file = open("poic.csv",  errors='ignore')
    lines = file.readlines()
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    for i in range(912,len(lines)):
        print(i)
        l=lines[i]
        uid_bd=l.split(";")[0].split(":")[1]
        name=l.split(";")[1].split(":")[1]
        addr=l.split(";")[2].split(":")[1]
        lat=l.split(";")[3].split(":")[1]
        lng=l.split(";")[4].split(":")[1]
        try:
            cur_test.execute("insert into buildings_info_insert(b_building_name,b_building_adr,b_lat,b_lon) VALUES ("+"\""+name+"\","+"\""+addr+"\","+"\""+lat+"\","+"\""+lng+"\"" +")")
            conn_test.commit()
        except Exception as e:
            print(e)

if __name__=='__main__':
    # get_allpoi()
    # analysis_poi()
    insert_poi()
    pass