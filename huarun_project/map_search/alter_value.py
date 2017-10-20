# -*- coding: utf-8 -*
'''
字段内容修改
'''

import pymysql
import time
from pymongo import MongoClient

# 连接mongodb

client = MongoClient("103.234.21.72", 27017)
db = client.TYCHtml
db.authenticate("tychtml", "2zeg4uei0364h21thw9m6")
collections = db.companys

# 将c_industry,c_rdate,c_capital字段中的“无”改为“保密”
def change_():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select c_id,c_industry,c_rdate,c_capital from company_connection_building ")
    for row in cur_test.fetchall():
        if row[1] == "无":
            cur_test.execute("update company_connection_building set c_industry="+"\""+"保密"+"\""+" where c_id=" +"\""+row[0]+"\"")
        if row[2] == "无":
            cur_test.execute("update company_connection_building set c_rdate="+"\""+"保密"+"\""+" where c_id=" +"\""+row[0]+"\"")
        if row[3] == "无":
            cur_test.execute("update company_connection_building set c_capital="+"\""+"保密"+"\""+" where c_id=" +"\""+row[0]+"\"")
        conn_test.commit()

    conn_test.close()
    cur_test.close()

# 将value="0 万元" 修改为null
def change_capital():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select c_id,c_company_name from company_connection_building")
    count = 0
    for r in cur_test.fetchall():
        print(count)
        c_name = r[1]
        print(c_name)
        cdate = ""
        capital = ""
        cstatus = ""
        company_portray = read_mongoid(c_name)
        if company_portray != "-1":
            try:
                if "regDate" in company_portray.keys():
                    rdate = company_portray["regDate"]
                    vdate = timestamp_datetime(rdate)
                    cdate = str(vdate).split(" ")[0]
                if "regCapital" in company_portray.keys():
                    capital = company_portray["regCapital"]
                if "status" in company_portray.keys():
                    cstatus = company_portray["status"]
                cur_test.execute("update company_connection_building set c_capital_detail="+"\""+capital+"\""+", c_cstatus="+"\""+cstatus+"\""+",c_rdate_detail="+"\""+cdate+"\"" +" where c_id="+"\""+r[0]+"\"" )
                conn_test.commit()
            except Exception as e:
                print(e)
        else:
            print("error!")
        count += 1

    conn_test.close()
    cur_test.close()


def read_mongoid(name):
    company_portray={}
    result = collections.find({"companyPortray.comName": name}, {"companyPortray": 1})
    try:
        for i in result:
            company_portray = i["companyPortray"]
    except Exception as e:
        print(e)

    if company_portray == {}:
        return "-1"
    else:
        return company_portray

def conn_test_yunketest():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    return conn_test


def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
     ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

if __name__ == '__main__':
    # change_()
    change_capital()

    # company_portray = read_mongoid("北京市至成电子公司")
    # print(company_portray)
    # rdate = company_portray["regDate"]
    # datee = timestamp_datetime(rdate)
    # print(str(datee).split(" ")[0])
    # print(company_portray["regCapital"])
    # print(company_portray["status"])
    pass
