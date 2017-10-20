# -*- coding: utf-8 -*
'''
company_connection_building表添加四个字段:行业(c_industry)、年份(c_rdate)、资金(c_capital)、天眼评分(score)
'''
import pymysql
import re

import sys
sys.path.append("../")

def add_filed():
    conn_gs = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur = conn_gs.cursor()
    cur.execute("select c_id from company_connection_building where c_industry is NULL ")

    for r in cur.fetchall():
        # 某个建筑物包含企业的行业，注册时间，注册资金
        stat = get_stat(r[0])
        capital=stat.split("%")[0]
        capital_clean="None"
        if capital != None and capital != "":
            capital = re.findall(r'(\w*[0-9]+)\w*', capital)
            if len(capital) > 0:
                capital_num = capital[0]
                if int(capital_num) < 100:
                    capital_clean="<100w"
                if int(capital_num) >= 100 and int(capital_num) < 500:
                    capital_clean="100w-500w"
                if int(capital_num) >= 500 and int(capital_num) < 1000:
                    capital_clean="500w-1000w"
                if int(capital_num) >= 1000 and int(capital_num) < 3000:
                    capital_clean="1000w-3000w"
                if int(capital_num) >= 3000 and int(capital_num) < 5000:
                    capital_clean="3000w-5000w"
                if int(capital_num) >= 5000:
                    capital_clean=">5000w"

        rdate=stat.split("%")[1]
        rdate_clean="None"
        if rdate != None:
            rdate_clean = str(rdate).split("-")[0]
        hangye=stat.split("%")[2]
        hangye_clean="None"
        if hangye != None and hangye != "NULL" and hangye != "":
            hangye_clean=hangye

        print(capital_clean)
        print(rdate_clean)
        print(hangye_clean)
        # 某个建筑物包含企业的天眼查概览信息
        tyc_score = get_tyc_score(r[0])
        if tyc_score=="-1" or tyc_score=="" or tyc_score==None:
            tyc_score="None"
        print(tyc_score)

        cur.execute("update company_connection_building set c_industry="+"\""+hangye_clean+"\""+","+"c_rdate="+"\""+rdate_clean+"\""+","+"c_capital="+"\""+capital_clean+"\""+","+"score="+"\""+tyc_score+"\""+" where c_id="+"\""+str(r[0])+"\"")
        conn_gs.commit()
    cur.close()
    conn_gs.close()

#获取到所有compnay_id
def get_stat(c_id):
    conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunkedata',
                                passwd='XingDongJia@2016',
                                db='dataprocess',
                                charset='utf8'
                                )
    cur = conn_gs.cursor()
    stat=""


    sql="select capital,registrationdate,hangye from company_yunke where id="+"\""+str(c_id)+"\""
    cur.execute(sql)
    for row in cur.fetchall():
        stat=str(row[0])+"%"+str(row[1])+"%"+str(row[2])

    cur.close()
    conn_gs.close()
    return stat


def get_tyc_score(company_id):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    clueid = ""
    cur_only.execute("select CLue_Id from crm_t_clue where commercialDB_id=" + "\"" + str(company_id) + "\"")
    for r in cur_only.fetchall():
            clueid=r[0]
    cur_only.close()
    conn_only.close()

    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    summary = ""
    sql = "select c_tyc_score from clue_feature where Clue_Id=" + "\"" + clueid + "\""
    cur_test.execute(sql)
    for row in cur_test.fetchall():
        summary = str(row[0])
    return summary

'''
company_connection_building表添加六个字段:公司名称(c_company_name)、企业法人(c_legalperson)、注册日期(c_rdate_detail)、地址(c_address)、注册资本(c_capital_detail)、状态(c_cstatus)
'''
def add_fields_six():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                              port=3306,
                              user='yunkedata',
                              passwd='XingDongJia@2016',
                              db='dataprocess',
                              charset='utf8'
                              )
    cur_gs = conn_gs.cursor()

    sql_cid="select c_id from company_connection_building"
    cid_list=[]
    cur_test.execute(sql_cid)
    for row in cur_test.fetchall():
        cid_list.append(row[0])

    for cid in cid_list:
        print(str(cid))
        sql_info="select title,legalperson,registrationdate,address,capital,cstatus from company_yunke where id="+"\""+str(cid)+"\""
        cur_gs.execute(sql_info)
        info_list=[]
        for r in cur_gs.fetchall():
            if r[0]!=None:
                info_list.append(r[0])
            else:
                info_list.append("")
            if r[1]!=None:
                info_list.append(r[1])
            else:
                info_list.append("")
            if r[2] != None:
                info_list.append(str(r[2]))
            else:
                info_list.append("")
            if r[3] != None:
                info_list.append(r[3])
            else:
                info_list.append("")
            if r[4] != None:
                info_list.append(r[4])
            else:
                info_list.append("")
            if r[5] != None:
                info_list.append(r[5])
            else:
                info_list.append("")

        sql_update="update company_connection_building set c_company_name="+"\""+info_list[0]+"\""+",c_legalperson="+"\""+info_list[1]+"\""+",c_rdate_detail="+"\""+info_list[2]+"\""+",c_address="+"\""+info_list[3]+"\""+",c_capital_detail="+"\""+info_list[4]+"\""+",c_cstatus="+"\""+info_list[5]+"\""+"where c_id="+"\""+str(cid)+"\""
        cur_test.execute(sql_update)
        conn_test.commit()

    cur_test.close()
    conn_test.close()
    cur_gs.close()
    conn_gs.close()

if __name__ == '__main__':
    # add_filed()
    add_fields_six()
    pass