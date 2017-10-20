# -*- coding: utf-8 -*
'''
第二批房天下数据，补齐楼宇信息
'''

import os
import pymysql
import socket
import re

socket.setdefaulttimeout(10)
conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                            port=3306,
                            user='yunker',
                            passwd='yunke2016',
                            db='alg',
                            charset='utf8'
                            )

cur_test = conn_test.cursor()

def get_building_name():

    sql_test = "SELECT u_id,b_building_name from buildings_info"
    cur_test.execute(sql_test)
    data_building_info = {}
    for row in cur_test.fetchall():
        data_building_info[str(row[1])]=str(row[0])
    return data_building_info

def get_html_fangtianxia():
    data_building_info=get_building_name()
    files=os.listdir("esf.fang.com")
    for i in range(0,len(files)):
        f=files[i]
        building=open("esf.fang.com/"+f, "r",encoding="utf-8",errors="ignore").read()
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
        elevator_num=""
        area=""
        total_floor=""
        room_rate=""
        standard_height=""
        hangqing=""

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

            if "name" in attr:
                name = attr.split(":")[1]

            if "basic" in attr:
                basic = attr.split(":")[1]
                if "总楼层" in basic:
                    total_floor = re.findall(r"总楼层： (.+?) ", basic)
                if "建筑面积" in basic:
                    area = re.findall(r"建筑面积：(.+?)m", basic)
                if "物业公司" in basic:
                    property = re.findall(r"物业公司：(.+?) ", basic)
                if "得房率" in basic:
                    room_rate = re.findall(r"得房率：(.+?) ", basic)
                if "层高" in basic:
                    standard_height = re.findall(r"层高：(.+?) ", basic)
                if "客梯数" in basic:
                    elevator_num = re.findall(r"客梯数：(.+?) ", basic)
                if "开发商" in basic:
                    developers = re.findall(r"开发商：(.+?) ", basic)


            if "priceDay" in attr:
                price = attr.split(":")[1].replace("\n", "").replace("\t","")
                if len(price) >0 and price != "	" and price!="null" :
                    price += "元/m²⋅天(租)"

            if "hangqing" in attr:
                hangqing = attr.split(":")[1].replace("市场行情", "")
            if price == "" and hangqing != "":
                price = hangqing.split("元/m²⋅天")[0]
                price = re.findall(r'(\d+(\.\d+)?)', price)
                if len(price) >0 and price!="	" and price!="null":
                    price = price[0][0] + "元/m²⋅天"
                else:
                    price=""
        for k, v in data_building_info.items():
            if name in str(k) or str(k) in name or str(k) == name:
                print(name)
                match_result=data_building_info[k] + "%" + k + "%" + price
                update_building(match_result)
                break
    conn_test.commit()
    cur_test.close()
    conn_test.close()

def update_building(match_result):
    info_list=match_result.split("%")
    bid=info_list[0]
    name=info_list[1]
    price=info_list[2]
    # construction_age = info_list[3]
    # building_type = info_list[4]
    # total_housing = info_list[5]
    # location = info_list[6]
    # total_number_buildings = info_list[7]
    # property = info_list[8]
    # developers = info_list[9]
    # activity = info_list[10]
    # plate_rate = info_list[11]
    # property_rate = info_list[12]
    # education_rate = info_list[13]
    # hangqing = info_list[14]

    sql_updata_price=""
    sql_updata_property=""
    sql_updata_developers=""
    if info_list[2]!="null" and info_list[2]!="" and len(info_list[2])>4:
        sql_updata_price = "update buildings_info set  b_price_range="+ "\"" +price+ "\""+ " where u_id=" + "\"" + bid + "\""
        print(sql_updata_price)
        cur_test.execute(sql_updata_price)
    # if info_list[8]!="null" and info_list[8]!="":
    #     sql_updata_property = "update buildings_info set   b_property_name="+ "\"" +property+ "\""+ " where u_id=" + "\"" + bid + "\""
    #     print(sql_updata_property)
    #     cur_test.execute(sql_updata_property)
    #
    # if info_list[9]!="null" and info_list[9]!="":
    #     sql_updata_developers = "update buildings_info set   b_building_developer="+ "\"" +developers+ "\""+ " where u_id=" + "\"" + bid + "\""
    #     print(sql_updata_developers)
    #     cur_test.execute(sql_updata_developers)


if __name__=='__main__':
    get_html_fangtianxia()
    pass