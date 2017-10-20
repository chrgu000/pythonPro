# -*- coding:utf-8 -*-
import os
import pymysql
import sys
import pickle


def get_connection_between_building():
    pkl_file = open("special_buildings.pkl", 'rb')
    buildings = pickle.load(pkl_file)
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

if __name__=='__main__':

    conn_build=get_connection_between_building()
    file = open("conn_build_1.csv", 'a')
    for build in conn_build:
        file.write(build)
    file.close()

    pass
