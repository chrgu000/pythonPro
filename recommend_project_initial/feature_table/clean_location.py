# -*- coding: utf-8 -*

import pymysql

#Clue_Longitude,
# Clue_Latitude,

def clean_location(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql_only = "SELECT CLue_Id,Clue_Longitude,Clue_Latitude,Clue_entry_Major,registed_capital_num,registed_capital_currency FROM crm_t_clue limit "+str(start)+","+str(banchsize)+";"
    cur_only.execute(sql_only)

    data=[]
    for row in cur_only.fetchall():
        cid = str(row[0])

        #**********Clue_Longitude,Clue_Latitude（经纬度）********
        #如果经纬度为空，值="-1"
        clon="-1"
        clat="-1"
        if clon!="" or clon!="None" or clon!="null" and clat!="" or clat!="None" or clat!="null":
            clon = str(row[1])
            clat = str(row[2])
        data.append(cid+"#"+clon+"#"+clat)
    cur_only.close()
    conn_only.close()
    return data

if __name__ == '__main__':
    pass
