# -*- coding: utf-8 -*

import random
import urllib.request as req
import urllib.parse as parse
import json
import pymysql
import re

# 给出建筑物名称，调用百度地图api接口，返回地址信息，经纬度信息
key = "nPPBW9xruVM07MG5B3QLqjpwoPCLtP6E"
def process_building(building_name):
    addr_loc=[]
    url="http://api.map.baidu.com/geocoder/v2/?&callback=renderOption&output=json&address="+parse.quote(building_name)+"&city="+parse.quote("北京市")+"&ak="+key
    json_geo = get_builds(url)
    if json_geo["status"] == 0:
        lng = str(json_geo["result"]["location"]["lng"])
        lat = str(json_geo["result"]["location"]["lat"])
    else:
        lng = "-1"
        lat = "-1"

    location=str(lng)+","+str(lat)
    address="无"
    addr_loc.append(address)
    addr_loc.append(location)
    return addr_loc

def get_builds(url):
    for k in range(0,5):
        try:
            record_req = req.urlopen(url, timeout=10)
            hjson = json.loads(record_req.read().decode("utf_8"))
            return(hjson)
            break
        except:
            print("data is null!")


# 给出注册时间，注册资本，行业，返回清洗标准后的数据
def fields_process(stat):
    capital = stat.split("%")[0]
    capital_clean = "None"
    if capital != None and capital != "":
        capital = re.findall(r'(\w*[0-9]+)\w*', capital)
        if len(capital) > 0:
            capital_num = capital[0]
            if int(capital_num) < 100:
                capital_clean = "<100w"
            if int(capital_num) >= 100 and int(capital_num) < 500:
                capital_clean = "100w-500w"
            if int(capital_num) >= 500 and int(capital_num) < 1000:
                capital_clean = "500w-1000w"
            if int(capital_num) >= 1000 and int(capital_num) < 3000:
                capital_clean = "1000w-3000w"
            if int(capital_num) >= 3000 and int(capital_num) < 5000:
                capital_clean = "3000w-5000w"
            if int(capital_num) >= 5000:
                capital_clean = ">5000w"

    rdate = stat.split("%")[1]
    rdate_clean = "None"
    if rdate != None:
        rdate_clean = str(rdate).split("-")[0]
    hangye = stat.split("%")[2]
    hangye_clean = "None"
    if hangye != None and hangye != "NULL" and hangye != "":
        hangye_clean = hangye
    return capital_clean+"%"+rdate_clean+"%"+hangye_clean

if __name__=='__main__':
    process_building("国贸大厦")
    pass