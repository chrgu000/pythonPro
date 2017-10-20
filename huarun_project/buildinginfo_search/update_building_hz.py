# -*- coding: utf-8 -*
'''
haozu:html文件解析，补全建筑物信息表中相关字段
'''

import os
import pymysql

def update_building():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test_up = conn_test.cursor()
    file = open("building_hz.csv", encoding='utf8', errors='ignore')
    match_result = file.readlines()

    for i in range(0, len(match_result)):
    # for i in range(0, 10):

        bid = match_result[i].split("%")[0]
        name = match_result[i].split("%")[1]
        addr=match_result[i].split("%")[2]
        hangqing=match_result[i].split("%")[3]
        basic=match_result[i].split("%")[4]
        price=match_result[i].split("%")[5].replace("\n","")

        introduce=""
        if len(addr)>0:
            introduce+=name.replace("\\","")+"坐落于"+addr.replace("\\","")+","
        if len(hangqing)>0:
            introduce+="其售价及周边价格介绍："+hangqing.replace("\\","").replace("\"","")
        if len(basic)>0:
            introduce+=basic.replace("\\","").replace("\"","")
        if len(price)>0:
            introduce+=",租赁价格是"+price.replace("\n","")+"元/m²⋅天。"

        sql_updata_degree = "update buildings_info set  b_building_price=" + "\"" + price + "\"" + " where b_building_name=" + "\"" + name + "\""

        try:
            cur_test_up.execute(sql_updata_degree)
            print()
        except Exception as e:
            print(sql_updata_degree)

    cur_test_up.close()
    conn_test.commit()
    conn_test.close()

# photo文件夹下的图片，更新到sql中，存储图片名称

def update_picture():
    conn_test = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test_up = conn_test.cursor()
    all_files = os.listdir("photo")
    bid_pic = {}
    for bid in range(1, 14855):
        pic = []
        for i in range(0, len(all_files)):
            if bid == int(all_files[i].split("_")[0]):
                pic.append(all_files[i])
        bid_pic[bid] = pic

    for k, v in bid_pic.items():
        pic_count = len(v)
        pic_path = ""
        bid = k
        for j in range(0, pic_count):
            pic_path += (v[j] + ",")

        print(str(bid) + ":" + pic_path)
        sql_updata_degree = "update buildings_info set  b_building_picture_baidu=" + "\"" + str(pic_path) + "\"" + " where b_id=" + "\"" + str(bid) + "\""
        try:
            cur_test_up.execute(sql_updata_degree)
        except Exception as e:
            print(e)

    cur_test_up.close()
    conn_test.commit()
    conn_test.close()


if __name__ == '__main__':
    update_building()
    # update_picture()
    pass