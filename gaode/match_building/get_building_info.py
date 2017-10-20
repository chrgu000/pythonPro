# -*- coding: utf-8 -*
'''
建筑物地址补齐：通过高德地图接口，获取建筑物地址和图片信息
get_building_addr(),给出建筑物名称，找到对应的地址信息
adr_supply()：将名称update到buildings_info b_building_adr字段
'''


key0 = "79d9804060d5aa9457e139ab0efcbcd3"
key1 = "fd6329856b21b17154b1839e51c12529"

import urllib
import urllib.request as req
import urllib.parse as parse
import json
import pymysql

def get_building_addr():
    b_adr=[]
    building_list= open("b_addr_list_2.txt", encoding='utf8', errors='ignore')
    lines = building_list.readlines()
    for i in range(0,len(lines)):
        c_id=lines[i].split(",")[1]
        keyword=lines[i].split(",")[2]
        url="http://restapi.amap.com/v3/place/text?&keywords="+parse.quote(keyword)+"&city=beijing&output=json&offset=20&page=1&key="+key0+"&extensions=all"
        while True:
            try:
                record_req = req.urlopen(url, timeout=10)
                hjson = json.loads(record_req.read().decode("utf_8"))
                addr=hjson["pois"][0]["cityname"]+hjson["pois"][0]["adname"]+hjson["pois"][0]["address"]
                print(str(c_id)+"%%"+addr)
                b_adr.append(str(c_id)+"%%"+addr)
                # 图片获取
                # if len(hjson["pois"][0]["photos"])!=0:
                #     count=len(hjson["pois"][0]["photos"])
                #     for j in range(0,count):
                #         photo_url=hjson["pois"][0]["photos"][j]["url"]
                #         photo_title=hjson["pois"][0]["photos"][j]["title"]
                #         req.urlretrieve(photo_url,"./photo/"+ str(b_id)+"_"+str(j)+".jpg")
                break
            except:
                break
                print("data is null!")
    return b_adr

def adr_supply(lines):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    for i in range(0, len(lines)):
        cid = lines[i].split("%%")[0].replace("\n", "")
        badr = lines[i].split("%%")[1].replace("\n", "")
        update_test = "update buildings_info set b_building_adr=" + "\"" + badr + "\"" + " where u_id=" + "\"" + cid + "\""
        print(update_test)
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
        conn_test.commit()

    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    b_adr=get_building_addr()
    adr_supply(b_adr)

    pass