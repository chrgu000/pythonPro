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


def update_building():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test_up = conn_test.cursor()
    file = open("building_ftx.csv", encoding='utf8', errors='ignore')
    match_result = file.readlines()

    for i in range(0, len(match_result)):
        info_list=match_result[i].split("%")
        bid=info_list[0]
        name=info_list[1]
        price=info_list[2]+"元/m²"
        construction_age = info_list[3]
        building_type = info_list[4]
        total_housing = info_list[5]
        location = info_list[6]
        total_number_buildings = info_list[7]
        property = info_list[8]
        developers = info_list[9]
        activity = info_list[10]
        plate_rate = info_list[11]
        property_rate = info_list[12]
        education_rate = info_list[13]


        sql_updata_price = "update buildings_info set   b_price_range="+ "\"" +price+ "\""+ " where b_building_name=" + "\"" + name + "\""
        print(sql_updata_price)
        # sql_updata_property = "update buildings_info set   b_property_name="+ "\"" +property+ "\""+ " where b_id=" + "\"" + bid + "\""
        # sql_updata_developers = "update buildings_info set   b_building_developer="+ "\"" +developers+ "\""+ " where b_id=" + "\"" + bid + "\""

        try:
            cur_test_up.execute(sql_updata_price)
            # cur_test_up.execute(sql_updata_property)
            # cur_test_up.execute(sql_updata_developers)

        except Exception as e:
            print(e)

    cur_test_up.close()
    conn_test.commit()
    conn_test.close()

# photo_ftx文件夹下，更新到sql，存储图片名称
#
# def update_picture():
#     conn_test = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
#                                 port=3306,
#                                 user='yunker',
#                                 passwd='yunke2016',
#                                 db='alg',
#                                 charset='utf8'
#                                 )
#     cur_test_up = conn_test.cursor()
#     all_files = os.listdir("photo_ftx")
#     bid_pic={}
#     for bid in range(1,14855):
#         pic = []
#         for i in range(0,len(all_files)):
#             if bid==int(all_files[i].split("_")[0]):
#                 pic.append(all_files[i])
#         bid_pic[bid]=pic
#
#     for k,v in bid_pic.items():
#         pic_count=len(v)
#         pic_path=""
#         bid =k
#         for j in range(0,pic_count):
#             pic_path+=(v[j]+",")
#
#         print(str(bid)+":"+pic_path)
#         sql_updata_degree = "update buildings_info set  b_building_picture_ftx=" + "\"" + str(pic_path) + "\"" + " where b_id=" + "\"" + str(bid) + "\""
#         try:
#             cur_test_up.execute(sql_updata_degree)
#         except Exception as e:
#              print(e)
#
#     cur_test_up.close()
#     conn_test.commit()
#     conn_test.close()


if __name__=='__main__':
    update_building()
    # update_picture()
    pass