#!user/bin/env python3
# -*- coding: utf-8 -*
# 访问mogo
# # uri = 'mongodb://' + user + ':' + pwd + '@' + server + ':' + port +'/'+ db_name
# uri = 'mongodb://' + "tychtml" + ':' + "2zeg4uei0364h21thw9m6" + '@' + "103.234.21.41" + ':' + "27017" + '/' + "TYCHtml"
# client = MongoClient(uri)
# mongodb = client.TYCHtml
# collection = mongodb.companys
# data = collection.find({"companyPortray.comName": {"$in": names}}, batch_size=len(names))
# uri = 'mongodb://' + user + ':' + pwd + '@' + server + ':' + port +'/'+ db_nameuri = 'mongodb://' + "tychtml" + ':' + "2zeg4uei0364h21thw9m6" + '@' + "103.234.21.41 " + ':' + "27017" +'/'+ "TYCHtml"client = MongoClient(uri)mongodb = client.TYCHtmlcollection = mongodb.companysdata = collection.find({"companyPortray.comName":{"$in":names}},batch_size=len(names))

# 爬取地图上所有poi，存储数据到mongodb中

import re
import json
import os
from pymongo import MongoClient
import logging

client = MongoClient("103.234.21.41", 27017)
db = client.GDSB
collection = db.gdbs

log_file = "sbuild1.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG)

def write2db(buildings):
    try:
        collection.insert_one(buildings)
    except Exception as e:
        print(buildings["_id"])

def main(json_dir):
    lines = open("sbuild1.log", 'r')
    name_lines = lines.readlines()
    finish_csv = []
    for finish in name_lines:
        finish_csv.append(finish.split(":")[2].replace("\n", ""))

    for file_name in os.listdir(json_dir):
        print(file_name)
        if file_name not in finish_csv:
            logging.info(file_name)
            try:
                lines = open(json_dir + "//" + file_name, 'r', encoding='utf8', errors='ignore')
                json_lines = lines.readlines()
                for json_line in json_lines:
                    building = json.loads(json_line)
                    if building["count"] != "0":
                        for i in range(0, len(building["pois"])):
                            building_Write = {}
                            building_Write["_id"] = building["pois"][i]["id"]
                            building_Write["name"] = building["pois"][i]["name"]
                            building_Write["tag"] = building["pois"][i]["tag"]
                            building_Write["type"] = building["pois"][i]["type"]
                            building_Write["typecode"] = building["pois"][i]["typecode"]
                            building_Write["biz_type"] = building["pois"][i]["biz_type"]
                            building_Write["address"] = building["pois"][i]["address"]
                            building_Write["location"] = building["pois"][i]["location"]
                            building_Write["tel"] = building["pois"][i]["tel"]
                            building_Write["postcode"] = building["pois"][i]["postcode"]
                            building_Write["website"] = building["pois"][i]["website"]
                            building_Write["email"] = building["pois"][i]["email"]
                            building_Write["pcode"] = building["pois"][i]["pcode"]
                            building_Write["pname"] = building["pois"][i]["pname"]
                            building_Write["citycode"] = building["pois"][i]["citycode"]
                            building_Write["cityname"] = building["pois"][i]["cityname"]
                            building_Write["adcode"] = building["pois"][i]["adcode"]
                            building_Write["adname"] = building["pois"][i]["adname"]
                            building_Write["importance"] = building["pois"][i]["importance"]
                            building_Write["shopid"] = building["pois"][i]["shopid"]
                            building_Write["shopinfo"] = building["pois"][i]["shopinfo"]
                            building_Write["poiweight"] = building["pois"][i]["poiweight"]
                            building_Write["gridcode"] = building["pois"][i]["gridcode"]
                            building_Write["distance"] = building["pois"][i]["distance"]
                            building_Write["navi_poiid"] = building["pois"][i]["navi_poiid"]
                            building_Write["entr_location"] = building["pois"][i]["entr_location"]
                            building_Write["business_area"] = building["pois"][i]["business_area"]
                            building_Write["exit_location"] = building["pois"][i]["exit_location"]
                            building_Write["match"] = building["pois"][i]["match"]
                            building_Write["recommend_project_mid"] = building["pois"][i]["recommend_project_mid"]
                            building_Write["timestamp"] = building["pois"][i]["timestamp"]
                            building_Write["alias"] = building["pois"][i]["alias"]
                            building_Write["indoor_map"] = building["pois"][i]["indoor_map"]
                            building_Write["indoor_data"] = building["pois"][i]["indoor_data"]
                            building_Write["groupbuy_num"] = building["pois"][i]["groupbuy_num"]
                            building_Write["discount_num"] = building["pois"][i]["discount_num"]
                            building_Write["biz_ext"] = building["pois"][i]["biz_ext"]
                            building_Write["event"] = building["pois"][i]["event"]
                            building_Write["children"] = building["pois"][i]["children"]
                            building_Write["photos"] = building["pois"][i]["photos"]

                            write2db(building_Write)
            except Exception as e:
                print(e)
        else:
            print("该文件上传完毕！")

def building_stat():
    lines = open('./place/010_北京市市辖区_商务住宅_别墅.csv', 'r', encoding='utf8', errors='ignore')
    json_lines = lines.readlines()
    all_data=[]
    for json_line in json_lines:
        building = json.loads(json_line)
        if building["count"] != "0":
            for i in range(0, len(building["pois"])):
                building_Write = {}
                #building_Write["_id"] = building["pois"][i]["id"]
                building_Write["name"] = building["pois"][i]["name"]
                # building_Write["tag"] = building["pois"][i]["tag"]
                # building_Write["type"] = building["pois"][i]["type"]
                # building_Write["typecode"] = building["pois"][i]["typecode"]
               # building_Write["biz_type"] = building["pois"][i]["biz_type"]
               #  building_Write["address"] = building["pois"][i]["address"]
               #  building_Write["location"] = building["pois"][i]["location"]
                # building_Write["tel"] = building["pois"][i]["tel"]
                # building_Write["postcode"] = building["pois"][i]["postcode"]
                # building_Write["website"] = building["pois"][i]["website"]
                # building_Write["email"] = building["pois"][i]["email"]
                # building_Write["pcode"] = building["pois"][i]["pcode"]
                # building_Write["pname"] = building["pois"][i]["pname"]
                # building_Write["citycode"] = building["pois"][i]["citycode"]
                #building_Write["cityname"] = building["pois"][i]["cityname"]
                # building_Write["adcode"] = building["pois"][i]["adcode"]
                # building_Write["adname"] = building["pois"][i]["adname"]
                # building_Write["importance"] = building["pois"][i]["importance"]
                # building_Write["shopid"] = building["pois"][i]["shopid"]
                # building_Write["shopinfo"] = building["pois"][i]["shopinfo"]
                # building_Write["poiweight"] = building["pois"][i]["poiweight"]
                # building_Write["gridcode"] = building["pois"][i]["gridcode"]
                # building_Write["distance"] = building["pois"][i]["distance"]
                # building_Write["navi_poiid"] = building["pois"][i]["navi_poiid"]
                # building_Write["entr_location"] = building["pois"][i]["entr_location"]
                # building_Write["business_area"] = building["pois"][i]["business_area"]
                # building_Write["exit_location"] = building["pois"][i]["exit_location"]
                # building_Write["match"] = building["pois"][i]["match"]
                # building_Write["recommend_project_mid"] = building["pois"][i]["recommend_project_mid"]
                # building_Write["timestamp"] = building["pois"][i]["timestamp"]
                # building_Write["alias"] = building["pois"][i]["alias"]
                # building_Write["indoor_map"] = building["pois"][i]["indoor_map"]
                # building_Write["indoor_data"] = building["pois"][i]["indoor_data"]
                # building_Write["groupbuy_num"] = building["pois"][i]["groupbuy_num"]
                # building_Write["discount_num"] = building["pois"][i]["discount_num"]
                # building_Write["biz_ext"] = building["pois"][i]["biz_ext"]
                # building_Write["event"] = building["pois"][i]["event"]
                # building_Write["children"] = building["pois"][i]["children"]
                # building_Write["photos"] = building["pois"][i]["photos"]
                all_data.append(building_Write)

    file = open("beijing_别墅.csv", 'a')
    for i in range(0, len(all_data)):
        file.write(str(all_data[i]))
        file.write('\n')
    file.close()

if __name__ == '__main__':
    main("D:\\placetext1\\")
    building_stat()
    pass