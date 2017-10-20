# -*- coding: utf-8 -*
'''
data_to_sql_1.py  data_to_sql_2.py  data_to_sql_3.py 是对不同字段
抽象出可计算向量，存入特征表，其中原始字段如下：
Clue_Longitude
Clue_Latitude
Clue_Entry_Major
registrationdate,
registed_capital_num
registed_capital_currency
com_site
com_type
employees_num
'''

import pymysql
import logging

def clue_clean(start,banchsize):
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

        #**********com_site(网址)**************
        #有网址，值=1；无网址=0
        comsite = '0'
        if row[1] != "" and row[1] != 'None':
            comsite = '1'

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

        #**********employees_num（员工人数）************
        #如果没有记录员工数，最大值=最小值=均值="-1"
        employees_min=employees_max=employees_mean=-1
        if str.isdigit(row[3])==True:
            employees_min = employees_max = employees_mean = row[3]
        else:
            if str(row[3])!='None' and str(row[3]!='null'):
                if len(row[3].split("-"))==2:
                    employees_min = row[3].split("-")[0]
                    employees_max =row[3].split("-")[1].replace("人","")
                    employees_mean =(int(employees_min)+int(employees_max))/2
                if len(row[3].split("-")) == 1:
                    if "下" in row[3]:
                        employees_min = 0
                        employees_max = str(row[3]).replace("人以下","")
                        employees_mean =(int(employees_min)+int(employees_max))/2
                    if "上" in row[3]:
                        employees_min =str(row[3]).replace("人以上", "").replace("以上","")
                        employees_max = int(employees_min)*2
                        employees_mean = (int(employees_min) + int(employees_max)) / 2
                    if row[3]=="少于50人":
                        employees_min = 0
                        employees_max = 50
                        employees_mean = 25
                    if "人" in row[3] and "以" not in row[3]:
                        employees_min = row[3].replace("人","")
                        employees_max = row[3].replace("人","")
                        employees_mean = row[3].replace("人","")


        data.append(clueid+"#"+comtype+"#"+comsite+"#"+str(employees_max)+"#"+str(employees_min)+"#"+str(employees_mean))
    cur_only.close()
    conn_only.close()
    return data

def insert_data(data):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    for i in range(0,len(data)):
        clueid=data[i].split("#")[0]
        comtype=data[i].split("#")[1]
        comsite=data[i].split("#")[2]
        employees_max=data[i].split("#")[3]
        employees_min=data[i].split("#")[4]
        employees_mean=data[i].split("#")[5]

        insert_test = "insert into clue_feature (Clue_Id,com_type,com_site,employees_num_max,employees_num_min,employees_num_mean) values("+"\""+clueid+"\""+","+"\""+comtype+"\""+","+"\""+comsite+"\""+","+"\""+employees_max+"\""+","+"\""+employees_min+"\""+","+"\""+employees_mean+"\""+");"
        try:
            cur_test.execute(insert_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()

if __name__ == '__main__':
    # log_file = "clue_feature.log"
    # logging.basicConfig(filename=log_file, level=logging.DEBUG)
    start=0
    banchsize=100000
    while(True):
        data = clue_clean(start,banchsize)
        if len(data)==0:break
        insert_data(data)
        start+=banchsize
        print("第"+str(start)+"完成")


    pass
