# -*- coding: utf-8 -*
'''
fangtianxia:html文件解析，补全建筑物信息表中相关字段
get_building_name():获取所有建筑物名称和id
get_html_fangtianxia():获取房天下html信息，解析,图片存入photo_ftx,解析到的建筑物信息存入buildings_ftx.csv
update_building():buildings_ftx.csv存入sql
'''

import os
import pymysql
import urllib.request as req
import socket
socket.setdefaulttimeout(10)

def get_building_name():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    sql_test = "SELECT b_id,b_building_name from buildings_info"
    cur_test.execute(sql_test)
    data_building_info = {}
    for row in cur_test.fetchall():
        data_building_info[str(row[1])]=str(row[0])
    cur_test.close()
    conn_test.close()
    return data_building_info


def get_html_fangtianxia():
    data_building_info=get_building_name()
    files=os.listdir("fangtianxia")
    for i in range(0,len(files)):
        print(i)
        f=files[i]
        building=open("fangtianxia/"+f, "r",encoding="utf-8",errors="ignore").read()
        count=len(building.split("\n"))
        name=""
        price=""
        construction_age=""
        building_type=""
        total_housing=""
        location=""
        total_number_buildings=""
        property=""
        developers=""
        activity=""
        plate_rate=""
        property_rate=""
        education_rate=""
        picture=""

        for c in range(0,count):
            attr=building.split("\n")[c]
            if "小区名称" in attr:
                name=attr.split(":")[1].replace("	","")
            if "价格" in attr:
                price=attr.split(":")[1].replace("	","")
            if "建筑年代" in attr:
                construction_age=attr.split(":")[1].replace("	","")
            if "建筑类型" in attr:
                building_type=attr.split(":")[1].replace("	","")
            if "房屋总数" in attr:
                total_housing=attr.split(":")[1].replace("	","")
            if "小区位置" in attr:
                location=attr.split(":")[1].replace("	","")
            if "楼栋总数" in attr:
                total_number_buildings=attr.split(":")[1].replace("	","")
            if "物业:" in attr:
                property=attr.split(":")[1].replace("	","")
            if "开发商" in attr:
                developers=attr.split(":")[1].replace("	","")
            if "活跃度评级" in attr:
                activity = attr.split(":")[1].replace("	","")
            if "板块评级" in attr:
                plate_rate = attr.split(":")[1].replace("	","")
            if "物业评级" in attr:
                property_rate = attr.split(":")[1].replace("	","")
            if "教育评级" in attr:
                education_rate = attr.split(":")[1].replace("	","")
            # if "图片" in attr:
            #     picture = attr.split(":	")[1]

        for k, v in data_building_info.items():
            match_result=""
            if name in str(k) or str(k) in name or str(k) == name:
                match_result=data_building_info[k] + "%" + k + "%" + price + "%" + construction_age + "%" + building_type + "%" + total_housing + "%" + location + "%" + total_number_buildings + "%" + property + "%" + developers + "%" + activity + "%" + plate_rate + "%" + property_rate + "%" + education_rate
                file = open("building_ftx.csv", 'a')
                file.write(match_result)
                file.write('\n')
                file.close()

                # pic_list = picture.split(",")
                # for j in range(0, len(pic_list)):
                #     for i in range(0,5):
                #         try:
                #             req.urlretrieve(pic_list[j], "./photo_ftx/" + str(data_building_info[k]) + "_" + str(j) + ".jpg")
                #             break
                #         except Exception as e:
                #             print(e)
                # break

    return match_result

if __name__=='__main__':
    match_result=get_html_fangtianxia()

    pass