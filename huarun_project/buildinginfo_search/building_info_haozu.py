# -*- coding: utf-8 -*
'''
haozu:html文件解析，补全建筑物信息表中相关字段
'''

import os
import pymysql
import re

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


def get_html_haozu():
    match_result=[]
    data_building_info=get_building_name()
    files=os.listdir("haozu")
    for i in range(0,len(files)):
        f=files[i]
        print(f)
        building=open("haozu/"+f, "r",encoding="utf8").read()
        count=len(building.split("\n"))
        name=""
        price=""
        total_floor=""
        area=""
        property_name=""
        room_rate=""
        standard_height=""
        elevator_num=""
        developer=""
        hangqing=""
        introuce = ""
        check_enterprise=""
        for c in range(0,count):
            attr=building.split("\n")[c]
            if "name" in attr:
                name=attr.split(":")[1]

            if "address" in attr:
                address=attr.split(":")[1].replace("	地址： ","").replace("[","").replace("]","").replace("地图","").replace(" -  ","").replace(" ","")
            if "basic" in attr:
                basic=attr.split(":")[1]
                if "总楼层" in basic:
                    total_floor=re.findall(r"总楼层： (.+?) ", basic)
                if "建筑面积" in basic:
                    area=re.findall(r"建筑面积：(.+?)m", basic)
                if "物业公司" in basic:
                    property_name=re.findall(r"物业公司：(.+?) ", basic)
                if "得房率" in basic :
                    room_rate=re.findall(r"得房率：(.+?) ", basic)
                if "层高" in basic:
                    standard_height=re.findall(r"层高：(.+?) ", basic)
                if "客梯数" in basic:
                    elevator_num=re.findall(r"客梯数：(.+?) ", basic)
                if "开发商" in basic:
                    developer=re.findall(r"开发商：(.+?) ", basic)
                union_name=get_child(name,basic)
                c = basic.split(union_name)
                for j in range(1, len(c)):
                    introuce += c[j]
                if "已入驻企业" in basic:
                    check_enterprise = re.findall(r"已入驻企业：(.+?)" + union_name, basic)

            if "priceDay" in attr:
                price=attr.split(":")[1].replace("\n","")
                price+="元/m²⋅天(租)"
            if "hangqing" in attr:
                hangqing=attr.split(":")[1].replace("市场行情","")
            if price=="" and hangqing!="":
                price=hangqing.split("元/m²⋅天")[0]
                price = re.findall(r'(\d+(\.\d+)?)', price)
                if len(price)>0:
                    price=price[0][0]+"元/m²⋅天"
                    print(price)
        for k,v in data_building_info.items():
            if name in str(k) or str(k) in name or str(k)==name:

                ss=data_building_info[k]+"#"+str(k)+"#"+str(price)+"#"+''.join(total_floor)+"#"+ ''.join(area) +"#"+ ''.join(property_name)+"#"+''.join(room_rate)+"#"+ ''.join(standard_height) +"#"+''.join(elevator_num)+"#"+''.join(developer)+"#"+''.join(hangqing)+"#"+ name+''.join(introuce)+"#"+''.join(check_enterprise)
                # print(ss)
                match_result.append(ss)
                break
    return match_result


def update_building(match_result):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test_up = conn_test.cursor()
    # file = open("building_hz_1.csv", encoding='utf8', errors='ignore')
    # match_result = file.readlines()

    for i in range(0, len(match_result)):

        bid = match_result[i].split("#")[0]
        name = match_result[i].split("#")[1]
        price=re.sub('[\ ]', '', match_result[i].split("#")[2])
        # totalfloor = re.sub('[\ ]', '', match_result[i].split("#")[3])
        # area = re.sub('[\ ]', '', match_result[i].split("#")[4])
        # propertyname = re.sub('[\ ]', '', match_result[i].split("#")[5])
        # roomrate = re.sub('[\ \\n]', '', match_result[i].split("#")[6])
        # standardheight = re.sub('[\ ]', '', match_result[i].split("#")[7])
        # elenum = match_result[i].split("#")[8]
        # elenum = re.sub('[\ ]', '', elenum)
        # developer = match_result[i].split("#")[9]
        # developer = re.sub('[\ ]', '', developer)
        # hangqing = match_result[i].split("#")[10]
        # hangqing = re.sub('[\ ]', '', hangqing)
        # introuce = re.sub('[\ \	]', '', match_result[i].split("#")[11])
        # introuce=''.join(introuce)
        # enterprise = re.sub('[\ \	]', '', match_result[i].split("#")[12])
        # enterprise=''.join(enterprise)

        sql_updata_1 = "update buildings_info set  b_price_range=" + "\"" + price + "\"" + " where b_id=" + "\"" + bid + "\""
        print(sql_updata_1)
        # sql_updata_2 = "update buildings_info set  b_building_floor=" + "\"" + totalfloor + "\"" + " where b_id=" + "\"" + bid + "\""
        # sql_updata_3 = "update buildings_info set  b_building_area=" + "\"" + area + "\"" + " where b_id=" + "\"" + bid + "\""
        # sql_updata_4 = "update buildings_info set  b_property_name=" + "\"" + propertyname + "\"" + " where b_id=" + "\"" + bid + "\""
        # sql_updata_5 = "update buildings_info set  b_room_rate=" + "\"" + roomrate + "\"" + " where b_id=" + "\"" + bid + "\""
        # sql_updata_6 = "update buildings_info set  b_standard_height=" + "\"" + standardheight + "\"" + " where b_id=" + "\"" + bid + "\""
        # sql_updata_7 = "update buildings_info set  b_elevator_num=" + "\"" + elenum + "\"" + " where b_id=" + "\"" + bid + "\""
        # sql_updata_8 = "update buildings_info set  b_building_developer=" + "\"" + developer + "\"" + " where b_id=" + "\"" + bid + "\""
        # sql_updata_9 = "update buildings_info set  b_hangqing=" + "\"" + hangqing + "\"" + " where b_id=" + "\"" + bid + "\""
        # sql_updata_10 = "update buildings_info set  b_building_introduce=" + "\"" + introuce + "\"" + " where b_id=" + "\"" + bid + "\""
        # sql_updata_11 = "update buildings_info set  b_check_enterprise=" + "\"" + enterprise + "\"" + " where b_id=" + "\"" + bid + "\""

        try:
            cur_test_up.execute(sql_updata_1)
            # cur_test_up.execute(sql_updata_2)
            # cur_test_up.execute(sql_updata_3)
            # cur_test_up.execute(sql_updata_4)
            # cur_test_up.execute(sql_updata_5)
            # cur_test_up.execute(sql_updata_6)
            # cur_test_up.execute(sql_updata_7)
            # cur_test_up.execute(sql_updata_8)
            # cur_test_up.execute(sql_updata_9)
            # cur_test_up.execute(sql_updata_10)
            # cur_test_up.execute(sql_updata_11)

        except Exception as e:
            print(e)

    cur_test_up.close()
    conn_test.commit()
    conn_test.close()

#查找两个字符串的连续子串
def get_child(data1, data2):
    maxLength = end = tempLength = 0
    tempData = {}

    # 选择出比较长字符串
    largest = data1
    other = data2
    if len(data2) > len(data1):
        largest = data2
        other = data1

    # 将比较长的字符串每个字符及位置存在字典中，便于查找
    for i in range(len(largest)):
        if largest[i] not in tempData: tempData[largest[i]] = []
        tempData[largest[i]].append(i)

    # 遍历较短字符串准备找相同字符串
    for i in range(len(other)):
        # 如果较长字符串中没有就丢弃
        if other[i] not in tempData: continue
        # 字符重复出现，其下标存在字典中List中
        indexList = tempData[other[i]]
        # 对重复字符遍历比较，查找字串
        for index in indexList:
            firsti = i + 1
            tempLength = 1
            j = index + 1
            # 字串查找
            while firsti < len(other) and j < len(largest) and other[firsti] == largest[j]:
                tempLength += 1
                firsti += 1
                j += 1
            # 如果本次子串最长纪录下来
            if tempLength > maxLength:
                maxLength = tempLength
                end = j
    return largest[end - maxLength:end]


if __name__=='__main__':
    match_result=get_html_haozu()
    update_building(match_result)

    # name="德胜凯旋大厦"
    # strr="basic:	写字楼信息 总楼层： 18层 建筑面积： 40939m² 得房率： 75% 标准层高： 4米 客梯数： 7个(上海三菱) 开发商： 北京杰盛华物业管理有限责任公司 物业公司： 北京杰盛华物业管理有限公司 已入驻企业： 洁盛华有限公司、北京环球医疗救援有限责任公司、中原地产、安利，招商银行，北京地方志编纂委员会办公室，北京英福美软件开发有限公司 联合国际大厦位于朝阳区东三环南路39号，十里河桥西北角，大厦位于华威桥与十里河桥之间，东南三环内侧，坐西朝东，与三环零距离，左右傍京津塘、京沈高速公路，是北京的重要商务区。 展开 被收录到【地铁10分钟】专题中 [查看专题]"
    # if "标准层高：" in strr:
    #     check_enterprise = re.findall(r"层高：(.+?) ", strr)
    #     print(check_enterprise)
    pass