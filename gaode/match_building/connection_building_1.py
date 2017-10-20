# -*- coding:utf-8 -*-
import os
import pymysql
import sys
import pickle
import urllib.request as req
import json
import urllib.parse

#找寻特殊建筑物与公司之间关系

def get_all_buildings():
    buildings_dict={}
    buildings_list=[]
    for file_name in os.listdir(sys.path[0]+"/buildings"):
        lines = open(sys.path[0]+"/buildings/" + file_name, 'r',encoding='utf8')
        all_buildings=lines.readlines()
        for building in all_buildings:
            b=building.replace("\n","")
            if b not in buildings_dict:
                buildings_dict[b]=1
            else:
                buildings_dict[b]+=1
    idf_dic = open("special_buildings.pkl", 'wb')
    pickle.dump(buildings_dict, idf_dic)
    print(buildings_dict)
    for k,v in buildings_dict.items():
        buildings_list.append(k)
    file = open("buildings_list.csv", 'a')
    for a in buildings_list:
        try:
            file.write(str(a) + "\n")
        except Exception as e:
            print(a)
            print(e)
    file.close()
    #return buildings_list

def get_connection_between_building(buildings):
    conn_build=[]
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur = conn_only.cursor()
    sql = "SELECT Clue_Entry_Com_Name,Com_Address FROM crm_t_clue WHERE param5='北京市'"
    cur.execute(sql)
    has_count=0
    all_count=0
    for row in cur.fetchall():
        all_count+=1
        min=0
        bulidf=''
        for key,value in buildings.items():
            set1 = set(key)
            set2 = set(row[1])
            if len(set1 & set2)>min :
                min=len(set1&set2)
                bulidf=str(key)

        if min>=len(bulidf)-1:
            conn_build.append(row[0]+":"+row[1]+":"+bulidf)
            has_count+=1

    print(has_count)
    print(all_count)
    return conn_build

# 调取百度接口，找到建筑物的地理位置，可能有多个
#比如五岳大厦分A座，b座，所以有两个地址

def  special_building_addr():
    key0 = "79d9804060d5aa9457e139ab0efcbcd3"
    # key1 = "fd6329856b21b17154b1839e51c12529"
    # key2 = "90b1575ae74dbe9a24d07f7a730c04c8"
    # key3 = "dd664c44f86f1f0b8355b377d5899f5f"

    lines = open("buildings_list.csv", 'r', encoding='utf8')
    all_buildings = lines.readlines()

    strr_list=[]
    for build in all_buildings:
        strr=str(build).replace("\n","")+":"
        k_quote=urllib.parse.quote(build)
        urls="http://restapi.amap.com/v3/place/text?key=fd6329856b21b17154b1839e51c12529&keywords="+k_quote+"&types=&city="+urllib.parse.quote("北京")+"&children=1&offset=20&page=1&extensions=all"
        while True:
            try:
                record_req = req.urlopen(urls,timeout=10)
                hjson = json.loads(record_req.read().decode("utf_8"))
                print(hjson)
                count=hjson['count']
                #解析json数据
                for i in range(0,min(int(count),5)):
                    strr += (hjson['pois'][i]['cityname'] + hjson['pois'][i]['adname'] + hjson['pois'][i]['address']+":#")
                print(strr)
                strr_list.append(strr)
                break
            except:
                print("data is null!")
                break
    file = open("conn_build_addr.csv", 'a')
    for s in strr_list:
        file.write(s+"\n")
    file.close()

def buildings_adrinfo_to_sql():
    #古北水镇温馨家园农家别墅: 北京市密云区古北水镇蔡家窝铺村244号(近古北水镇旅游区):  #
    lines = open("conn_build_addr.csv", 'r', encoding='utf8')
    all_buildings = lines.readlines()
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    for i in range(0,len(all_buildings)):
        clueid =i
        name=all_buildings[i].split(":")[0]
        length=len(all_buildings[i].split(":#"))
        adr_1 = ""
        adr_2 = ""
        adr_3 = ""
        adr_4 = ""
        adr_5 = ""
        if length==2:
            adr_1 = all_buildings[i].split(":#")[0].split(":")[1]
        if length == 3:
            adr_1 = all_buildings[i].split(":#")[0].split(":")[1]
            adr_2 = all_buildings[i].split(":#")[1]
        if length == 4:
            adr_1 = all_buildings[i].split(":#")[0].split(":")[1]
            adr_2 = all_buildings[i].split(":#")[1]
            adr_3 = all_buildings[i].split(":#")[2]
        if length == 5:
            adr_1 = all_buildings[i].split(":#")[0].split(":")[1]
            adr_2 = all_buildings[i].split(":#")[1]
            adr_3 = all_buildings[i].split(":#")[2]
            adr_4 = all_buildings[i].split(":#")[3]
        if length == 6:
            adr_1 = all_buildings[i].split(":#")[0].split(":")[1]
            adr_2 = all_buildings[i].split(":#")[1]
            adr_3 = all_buildings[i].split(":#")[2]
            adr_4 = all_buildings[i].split(":#")[3]
            adr_5 = all_buildings[i].split(":#")[4]

        update_test = "insert into buildings_infos (b_id,b_buildings_name,b_building_adr,b_building_adr2,b_building_adr3,b_building_adr4,b_building_adr5) values("+"\""+str(clueid)+"\""+","+"\""+name+"\""+","+"\""+adr_1+"\""+","+"\""+adr_2+"\""+","+"\""+adr_3+"\""+","+"\""+adr_4+"\""+ ","+"\""+adr_5+"\""+" );"
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()



if __name__=='__main__':
    #获取特殊建筑物的字典
    #buildings=get_all_buildings()

    #读取字典，调用高德接口，返回每一个建筑物地址
    # pkl_file = open("special_buildings.pkl", 'rb')
    # lexicon_dic = pickle.load(pkl_file)
    # print(len(lexicon_dic))
    # print(lexicon_dic)
    #special_building_addr()
    #将建筑物及得到的地址存入buildings_info表中
    buildings_adrinfo_to_sql()


    # conn_build=get_connection_between_building(buildings)
    # file = open("conn_build.csv", 'a')
    # for build in conn_build:
    #     file.write(build)
    # file.close()

    pass
