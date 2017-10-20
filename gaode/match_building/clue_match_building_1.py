# -*- coding: utf-8 -*

#匹配工商库company_yunke的地址与buildings_infos表中的大厦名称
#匹配方式：1）通过大厦名称与线索表公司注册地址匹配

import pymysql

#从工商库取id，注册地址
# def get_addr():
#     conn_only = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
#                                 port=3306,
#                                 user='yunkedata',
#                                 passwd='XingDongJia@2016',
#                                 db='dataprocess',
#                                 charset='utf8'
#                                 )
#     cur_only = conn_only.cursor()
#     #sql_only = "SELECT id,address FROM company_yunke where province="+"\""+"北京市"+"\""+ " limit " + str(start) + "," + str(banchsize) + ";"
#     sql_only="SELECT id,address,province,registeredaddr FROM company_yunke WHERE id IN (SELECT id FROM company_yunke) AND  province LIKE '北京%'"
#     cur_only.execute(sql_only)
#     data_addr=[]
#     for row in cur_only.fetchall():
#         if len(row[1])>0 or row[1]!="":
#             data_addr.append(str(row[0])+"%"+row[1])
#         else:
#             if row[3]!="" and len(row[3])>0:
#                 data_addr.append(str(row[0])+"%"+row[3])
#             else:
#                 data_addr.append(str(row[0]) + "%" + "null")
#     cur_only.close()
#     conn_only.close()
#     return data_addr


def get_addr1(start,banchsize):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    sql_test = "SELECT Clue_Id,clue_addr from company_connection_building limit "+str(start)+","+str(banchsize)
    cur_test.execute(sql_test)
    data_addr=[]
    for row in cur_test.fetchall():
        data_addr.append(str(row[0])+"%"+row[1])
    cur_test.close()
    conn_test.close()
    return data_addr
#获取特殊建筑表buildings_info
def get_building_info():
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
    data_building_info = []
    for row in cur_test.fetchall():
        data_building_info.append(str(row[0]) + "%" + str(row[1]))
    cur_test.close()
    conn_test.close()
    return data_building_info



#匹配buildings
#第一遍清洗匹配：方式，在线索表中出现的地址完全匹配特殊建筑物名称
def match_buildings(data_addr,data_building_info):
    match_result=[]
    for i in range(0,len(data_addr)):
        clueid=data_addr[i].split("%")[0]
        clue_addr=data_addr[i].split("%")[1]
        for j in range(0,len(data_building_info)):
            bid=data_building_info[j].split("%")[0]
            building_name=data_building_info[j].split("%")[1]
            if str(building_name) in clue_addr:
                match_result.append(clueid + "#" + bid)
                break

    # for i in range(0,len(match_result)):
    #     print(match_result[i])
    return match_result

#将匹配到的线索存入测试库
# def buildings_conn_to_sql(match_result):
#
#     conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
#                                 port=3306,
#                                 user='yunker',
#                                 passwd='yunke2016',
#                                 db='alg',
#                                 charset='utf8'
#                                 )
#     cur_test = conn_test.cursor()
#     for i in range(0,len(match_result)):
#         clueid =match_result[i].split("#")[0]
#         clue_adr =match_result[i].split("#")[1]
#         bid =match_result[i].split("#")[2]
#         b_name =match_result[i].split("#")[3]
#         update_test = "insert into company_connection_building (Clue_Id,clue_addr,b_id,b_name) values("+"\""+str(clueid)+"\""+","+"\""+str(clue_adr)+"\""+","+"\""+bid+"\""+","+"\""+b_name+"\""+" );"
#         try:
#             cur_test.execute(update_test)
#         except Exception as e:
#             print(e)
#     cur_test.close()
#     conn_test.commit()
#     conn_test.close()

#将匹配到的线索存入测试库
def buildings_conn_updateto_sql(match_result):

    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    for i in range(0,len(match_result)):
        clueid =match_result[i].split("#")[0]
        bid =match_result[i].split("#")[1]
        update_test = "update company_connection_building set b_n_id="+bid+"," +"b_name_match=1 where Clue_Id="+clueid
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()

if __name__ == '__main__':
    data_building_info=get_building_info()
    start=546100
    banchsize=10000
    while(True):
        data_addr=get_addr1(start,banchsize)
        if len(data_addr)==0:break
        match_result=match_buildings(data_addr,data_building_info)
        # buildings_conn_to_sql(match_result)
        buildings_conn_updateto_sql(match_result)
        start+=banchsize
        print(start)
    pass