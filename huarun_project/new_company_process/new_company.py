# -*- coding: utf-8 -*
'''
获取未匹配到楼宇的公司或新加入的公司信息
输入参数：地区，日期；地区如果为null，表示寻找全国地区公司
输入参数样例：北京市,20170811
'''

import pymysql

def get_company(city,time):
    company=[]
    conn_test_business = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunkedata',
                                passwd='XingDongJia@2016',
                                db='dataprocess',
                                charset='utf8'
                                )
    cur_test_business = conn_test_business.cursor()
    sql_business=""
    if city!="" and time!="":
        sql_business = "SELECT id,address FROM company_yunke WHERE city="+"\""+city+"\""+ " and edit_date>"+"\""+time+"\""
    if city!="" and time=="":
        sql_business= "SELECT id,address FROM company_yunke WHERE city="+"\""+city+"\""
    if city=="" and time!="":
        sql_business= "SELECT id,address FROM company_yunke WHERE edit_date>" + "\"" + time + "\""
    if city=="" and time=="":
        sql_business = "SELECT id,address FROM company_yunke"

    print(sql_business)

    cur_test_business.execute(sql_business)
    for row in cur_test_business.fetchall():
        cid=row[0]
        c_addr=row[1]
        company.append(str(cid)+"#"+c_addr)

    return company


if __name__=='__main__':
    company=get_company("北京市","")
    print(company)
    pass