# -*- coding: utf-8 -*
'''
统计:
b_all_enterprise_stat: 统计企业总数总数
b_all_trademark_stat:统计商标信息总数
b_all_patent_stat :统计专利总数
b_all_copyright_start:统计著作权总数
b_all_recruit_stat:统计招聘信息总数
b_no_trademark_start:统计无商标的企业总数
b_no_patent_stat:统计无专利的企业总数
b_no_copyright_stat:统计无著作权的企业总数
b_has_trademark_stat:统计有商标的企业总数
b_has_patent_stat:统计有专利的企业总数
b_has_copyright_stat:统计有著作权的企业总数
'''

import pymysql
from pymongo import MongoClient

# 连接mongodb

client = MongoClient("103.234.21.72", 27017)
db = client.TYCHtml
db.authenticate("tychtml", "2zeg4uei0364h21thw9m6")
collections = db.companys

def stat_fields_digital():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    # 对每一个建筑物统计所需要的字段信息
    buildings = get_buildings()
    for i in range(0, len(buildings)):
        print("建筑物："+str(i))
        companys = get_companys(buildings[i])
        all_enterprise_stat = len(companys)
        all_trademark = 0
        all_patent = 0
        all_copyright = 0
        all_recruit = 0
        has_trademark = 0
        has_patent = 0
        has_copyright = 0
        for j in range(0, len(companys)):
            summary = read_mongoid(companys[j])
            if summary != "":
                if "recruitCount" in summary.keys():
                    all_recruit += int(summary["recruitCount"])
                if "copyrightCount" in summary.keys():
                    all_copyright += int(summary["copyrightCount"])
                    has_copyright += 1
                if "patentCount" in summary.keys():
                    all_patent += int(summary["patentCount"])
                    has_patent += 1
                if "tmCount" in summary.keys():
                    all_trademark += int(summary["tmCount"])
                    has_trademark += 1

        no_copyright = all_enterprise_stat - has_copyright
        no_patent = all_enterprise_stat - has_patent
        no_trademark = all_enterprise_stat - has_trademark


        update_sql = "update buildings_info set b_all_enterprise_stat="+"\""+str(all_enterprise_stat)+"\"," \
                        + "b_all_trademark_stat="+"\""+str(all_trademark) +"\","\
                        +"b_all_patent_stat="+"\""+ str(all_patent)+"\"," \
                        + "b_all_copyright_stat=" + "\"" + str(all_copyright) + "\"," \
                        +"b_all_recruit_stat=" + "\"" + str(all_recruit) + "\"," \
                        + "b_no_trademark_stat=" + "\"" + str(no_trademark) + "\"," \
                        +"b_no_patent_stat=" + "\"" + str(no_patent) + "\"," \
                        +"b_no_copyright_stat=" + "\"" + str(no_copyright) + "\"," \
                        +"b_has_trademark_stat=" + "\"" + str(has_trademark) + "\"," \
                        +"b_has_patent_stat=" + "\"" + str(has_patent) + "\"," \
                        +"b_has_copyright_stat=" + "\"" + str(has_copyright) + "\"" \
                        +" where u_id="+ "\""+str(buildings[i])+"\""

        cur_test.execute(update_sql)
        conn_test.commit()
        print(update_sql)
    conn_test.close()
    cur_test.close()

# 获取所有建筑uuid
def get_buildings():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()

    sql_test = "select u_id from buildings_info"
    building_uid = []
    cur_test.execute(sql_test)
    for row in cur_test.fetchall():
        building_uid.append(row[0])
    cur_test.close()
    conn_test.close()
    return building_uid

# 得到某个建筑里所有公司
def get_companys(b_uid):
    company_lists = []
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select c_company_name from company_connection_building where b_uid="+"\""+b_uid+"\"")
    for r in cur_test.fetchall():
        company_lists.append(r[0])
    cur_test.close()
    conn_test.close()
    return company_lists


def conn_test_yunketest():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    return conn_test

def read_mongoid(name):
    summary = {}
    result = collections.find({"companyPortray.comName": name}, {"summary": 1})
    try:
        for i in result:
            summary = i["summary"]
    except Exception as e:
        print(e)
    return summary


if __name__ == '__main__':
    stat_fields_digital()
    # name = "北京虾烤虾烤餐饮管理有限公司"
    # summary = read_mongoid(name)
    # if summary != "":
    #     if "changeCount" in summary.keys():
    #         print(summary["changeCount"])
    pass