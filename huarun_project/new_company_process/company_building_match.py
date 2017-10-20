# -*- coding: utf-8 -*

'''
匹配线索-建筑物过程
返回的数据 c_building是list类型，list[0] 表示能匹配到建筑物的所有公司及对应建筑物名称地址，list[1]表示未能匹配到的公司Id
'''

key0 = "79d9804060d5aa9457e139ab0efcbcd3"

import sys
sys.path.append("./")
import urllib.request as req
import urllib.parse as parse
import json
from  new_company import get_company

def get_match_building(city,time):
    company_list = get_company(city,time)
    c_match_buinding = []
    c_no_match_building = []
    c_building = []
    for i in range(0,len(company_list)):
        c_id = company_list[i].split("#")[0]
        c_addr = company_list[i].split("#")[1].replace("\n","")
        url1 = "http://restapi.amap.com/v3/geocode/geo?key="+key0+"&address="+parse.quote(c_addr)
        json_geo = get_builds(url1)
        try:
            if len(json_geo["geocodes"])>0 and len(json_geo)>0:
                location=json_geo["geocodes"][0]["location"]
        except Exception as e:
            print("location error!"+str(company_list[i]))

        url2="http://restapi.amap.com/v3/geocode/regeo?key="+key0+"&location="+location+"&poitype="+parse.quote("写字楼|大厦|饭店|科技园|商务园|小区|开发区|产业园")+"&radius=1000&extensions=all&batch=false&roadlevel=0"
        json_nearpoi = get_builds(url2)
        m_name=""
        min_dis=10000
        m_addr=""
        if len(json_nearpoi["regeocode"]["pois"]) > 0:
            for i in range(0,len(json_nearpoi["regeocode"]["pois"])):
                b_dis=json_nearpoi["regeocode"]["pois"][i]["distance"]
                b_type=json_nearpoi["regeocode"]["pois"][i]["type"]
                b_name=json_nearpoi["regeocode"]["pois"][i]["name"]
                b_addr=json_nearpoi["regeocode"]["pois"][i]["address"]
                b_pname=json_nearpoi["regeocode"]["addressComponent"]["province"]
                if str(json_nearpoi["regeocode"]["addressComponent"]["district"]) != "[]":
                    b_cityname=json_nearpoi["regeocode"]["addressComponent"]["district"]
                if str(json_nearpoi["regeocode"]["addressComponent"]["district"])!="[]":
                    b_adname=json_nearpoi["regeocode"]["addressComponent"]["district"]

                if ("写字楼" in b_type or "楼宇" in b_type or "商务住宅" in b_type or "大厦" in b_type or "产业园" in b_type or "饭店" in b_type or "小区" in b_type \
                    or "科技园" in b_type or "商务园" in b_type or "住宅区" in b_type or "大学" in b_type or "工业园" in b_type or "商业中心" in b_type) and float(b_dis) < min_dis:
                    m_name=b_name
                    min_dis=float(b_dis)
                    m_addr=str(b_pname)+str(b_cityname)+str(b_adname)+str(b_addr)

        if m_name!="":
            c_match_buinding.append(c_id+"%"+str(m_name)+"%"+str(min_dis)+"%"+str(m_addr))
        else:
            c_no_match_building.append(c_id)

    c_building.append(c_match_buinding)
    c_building.append(c_no_match_building)
    return c_building


def get_builds(url):
    while True:
        try:
            record_req = req.urlopen(url, timeout=10)
            hjson = json.loads(record_req.read().decode("utf_8"))
            return(hjson)
            break
        except:
            print("data is null!")

if __name__=='__main__':
    c_match_buinding=get_match_building("北京市","20170901")
    pass