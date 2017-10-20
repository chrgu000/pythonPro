# -*- coding: utf-8 -*
'''
抽象出可计算向量，存入特征表，其中原始字段：com_type
'''

import pymysql
import logging

def clean_comtype(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql_only = "SELECT CLue_Id,com_site,com_type,employees_num FROM crm_t_clue limit "+str(start)+","+str(banchsize)+";"
    cur_only.execute(sql_only)

    data=[]
    for row in cur_only.fetchall():
        clueid = str(row[0])

        #***********com_type（公司性质）*************
        #如果无，值="0"
        comtype = '0'
        if "国有" in row[2]:
            comtype='1'
        if "集体企业" in row[2]:
            comtype='2'
        if "联营企业" in row[2]:
            comtype='3'
        if "股份合作制企业" in row[2]:
            comtype='4'
        if "私营企业" in row[2]:
            comtype='5'
        if "个体户" in row[2] or "个体工商户" in row[2]:
            comtype='6'
        if "合伙企业" in row[2]:
            comtype='7'
        if "有限责任公司" in row[2]:
            comtype='8'
        if "股份有限公司" in row[2]:
            comtype='9'
        if "农民专业合作社" in row[2] or "农民专业合作经济组织" in row[2]:
            comtype='10'
        if "个人独资" in row[2]:
            comtype='11'

        data.append(clueid+"#"+comtype)
    cur_only.close()
    conn_only.close()
    return data

if __name__ == '__main__':
    pass
