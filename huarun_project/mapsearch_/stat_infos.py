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
b_industry_distribution:行业分布
b_date_distribution:注册时间分布
b_capital_distribution 注册资本分布
'''
import pymysql
import re


def stat_info():
    # 对每一个建筑物统计所需要的字段信息
    buildings=get_buildings()
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    year_length=0
    hangye_length=0

    for i in range(0,len(buildings)):
        print(str(i)+":"+buildings[i])
        company_id = []
        sql="select c_id from company_connection_building where  b_uid="+"\""+buildings[i]+"\""
        cur_test.execute(sql)
        for row in cur_test.fetchall():
            company_id.append(row[0])

        #某个建筑物包含企业的行业，注册时间，注册资金
        stat = get_stat(company_id)

        #某个建筑物包含企业的天眼查概览信息
        # tyc_summery=get_tyc_summery(company_id)
        # all_enterprise_stat = len(company_id)

        # all_trademark=0
        # all_patent=0
        # all_copyright=0
        # all_recruit=0
        # has_trademark=0
        # has_patent=0
        # has_copyright=0
        #
        # for j in range(0,len(tyc_summery)):
        #     if len(tyc_summery[j])>4 and "{" in tyc_summery[j]:
        #         summery_dict=eval(tyc_summery[j])
        #         if "14" in summery_dict.keys():
        #             all_copyright+=int(summery_dict["14"])
        #             has_copyright+=1
        #         if "29" in summery_dict.keys():
        #             all_patent+=int(summery_dict["29"])
        #             has_patent+=1
        #         if "40" in summery_dict.keys():
        #             all_trademark+=int(summery_dict["40"])
        #             has_trademark+=1
        #         if "33" in summery_dict.keys():
        #             all_recruit+=int(summery_dict["33"])
        #
        # no_copyright=all_enterprise_stat-has_copyright
        # no_patent=all_enterprise_stat-has_patent
        # no_trademark=all_enterprise_stat-has_trademark

        # capital_distribution={}
        # capital_distribution["<100w"] =0
        # capital_distribution["100w-500w"] =0
        # capital_distribution["500w-1000w"] = 0
        # capital_distribution["1000w-3000w"] = 0
        # capital_distribution["3000w-5000w"] = 0
        # capital_distribution[">5000w"] = 0
        #
        # capital_list=stat[0]
        # has_capital=0
        # for j in range(0,len(capital_list)):
        #     if capital_list[j]!=None and capital_list[j]!="":
        #         capital= re.findall(r'(\w*[0-9]+)\w*', capital_list[j])
        #         if len(capital)>0:
        #             capital_num=capital[0]
        #             if int(capital_num)<100:
        #                 capital_distribution["<100w"]+=1
        #                 has_capital+=1
        #             if int(capital_num)>=100 and int(capital_num)<500:
        #                 capital_distribution["100w-500w"]+=1
        #                 has_capital += 1
        #             if int(capital_num)>=500 and int(capital_num)<1000:
        #                 capital_distribution["500w-1000w"]+=1
        #                 has_capital += 1
        #             if int(capital_num)>=1000 and int(capital_num)<3000:
        #                 capital_distribution["1000w-3000w"]+=1
        #                 has_capital += 1
        #             if int(capital_num)>=3000 and int(capital_num)<5000:
        #                 capital_distribution["3000w-5000w"]+=1
        #                 has_capital += 1
        #             if int(capital_num)>=5000 :
        #                 capital_distribution[">5000w"]+=1
        #                 has_capital += 1
        # capital_distribution["无"]=len(capital_list)-has_capital

        date_distribution = {}
        date_distribution["无"] = 0
        date_distribution["2016-2017"] = 0
        date_distribution["2014-2015"] = 0
        date_distribution["2012-2013"] = 0
        date_distribution["2010-2011"] = 0
        date_distribution["2008-2009"] = 0
        date_distribution["2006-2007"] = 0
        date_distribution["2004-2005"] = 0
        date_distribution["2002-2003"] = 0
        date_distribution["2000-2001"] = 0
        date_distribution["1998-1999"] = 0
        date_distribution["1996-1997"] = 0
        date_distribution["1994-1995"] = 0
        date_distribution["1992-1993"] = 0
        date_distribution["1990-1991"] = 0
        date_distribution["1988-1989"] = 0
        date_distribution["1986-1987"] = 0
        date_distribution["1984-1985"] = 0
        date_distribution["1982-1983"] = 0
        date_distribution["<1982"] = 0

        date_list = stat[1]
        for j in range(0, len(date_list)):
            if date_list[j] != None:
                year = int(str(date_list[j]).split("-")[0])
                if 2017<=year and year<=2016 :
                    date_distribution["2016-2017"] += 1
                if 2014<=year and year<=2015 :
                    date_distribution["2014-2015"] += 1
                if 2012<=year and year<=2013 :
                    date_distribution["2012-2013"] += 1
                if 2010<=year and year<=2011:
                    date_distribution["2010-2011"] += 1
                if 2008<=year and year<=2009 :
                    date_distribution["2008-2009"] += 1
                if 2006<=year and year<=2007 :
                    date_distribution["2006-2007"] += 1
                if 2004<=year and year<=2005 :
                    date_distribution["2004-2005"] += 1
                if 2002<=year and year<=2003 :
                    date_distribution["2002-2003"] += 1
                if 2000<=year and year<=2001 :
                    date_distribution["2000-2001"] += 1
                if 1998<=year and year<=1999 :
                    date_distribution["1998-1999"] += 1
                if 1996<=year and year<=1997:
                    date_distribution["1996-1997"] += 1
                if 1994<=year and year<=1995 :
                    date_distribution["1994-1995"] += 1
                if 1992<=year and year<=1993 :
                    date_distribution["1992-1993"] += 1
                if 1990<=year and year<=1991 :
                    date_distribution["1990-1991"] += 1
                if 1988 <= year and year <= 1989:
                    date_distribution["1988-1989"] += 1
                if 1986 <= year and year <= 1987:
                    date_distribution["1986-1987"] += 1
                if 1984 <= year and year <= 1985:
                    date_distribution["1984-1985"] += 1
                if 1982 <= year and year <= 1983:
                    date_distribution["1982-1983"] += 1
                if year <= 1982:
                    date_distribution["<1982"] += 1
            else:
                date_distribution["无"] += 1

        # industry_distribution = {}
        # industry_distribution["无"]=0
        # industry_list=stat[2]
        # for j in range(0,len(industry_list)):
        #     if industry_list[j]!=None and industry_list[j]!="NULL" and industry_list[j]!="":
        #         if industry_list[j] not in industry_distribution:industry_distribution[industry_list[j]]=1
        #         else:industry_distribution[industry_list[j]]+=1
        #     else:
        #         industry_distribution["无"]+=1

        n_capital_dis={}
        n_date_dis={}
        n_industry_dis={}

        # for k,v in capital_distribution.items():
        #     if v!=0:n_capital_dis[k]=v

        for k, v in date_distribution.items():
            if v!=0: n_date_dis[k] =v

        # for k, v in industry_distribution.items():
        #     if v!=0: n_industry_dis[k] =v

        # if len(n_capital_dis)==0:n_capital_dis=""
        if len(n_date_dis)==0:n_date_dis=""
        # if len(n_industry_dis)==0:n_industry_dis=""

        if len(n_date_dis)>year_length:
            year_length=len(n_date_dis)
        # if len(n_industry_dis)>hangye_length:
        #     hangye_length=len(n_industry_dis)

        #print(n_capital_dis)
        print(n_date_dis)
        # print(n_industry_dis)

        # update_sql="update buildings_info set b_all_enterprise_stat="+"\""+str(all_enterprise_stat)+"\"," \
        #                 + "b_all_trademark_stat="+"\""+str(all_trademark) +"\","\
        #                 +"b_all_patent_stat="+"\""+ str(all_patent)+"\"," \
        #                 + "b_all_copyright_stat=" + "\"" + str(all_copyright) + "\"," \
        #                 +"b_all_recruit_stat=" + "\"" + str(all_recruit) + "\"," \
        #                 + "b_no_trademark_stat=" + "\"" + str(no_trademark) + "\"," \
        #                 +"b_no_patent_stat=" + "\"" + str(no_patent) + "\"," \
        #                 +"b_no_copyright_stat=" + "\"" + str(no_copyright) + "\"," \
        #                 +"b_has_trademark_stat=" + "\"" + str(has_trademark) + "\"," \
        #                 +"b_has_patent_stat=" + "\"" + str(has_patent) + "\"," \
        #                 +"b_has_copyright_stat=" + "\"" + str(has_copyright) + "\"," \
        #                 +"b_industry_distribution=" + "\"" + str(industry_distribution) + "\"," \
        #                 +"b_date_distribution=" + "\"" + str(date_distribution) + "\"," \
        #                 +"b_capital_distribution=" + "\"" + str(capital_distribution) + "\""+" where u_id="+ "\""+str(buildings[i])+"\""
        # upsql="update buildings_info set b_all_enterprise_stat="+"\""+str(all_enterprise_stat)+"\""+" where u_id="+ "\""+str(buildings[i])+"\""

        try:
            # update_sql="update buildings_info set b_industry_distribution=" + "\"" + str(n_industry_dis) + "\"," \
            #                 +"b_date_distribution=" + "\"" + str(n_date_dis) + "\"," \
            #                 +"b_capital_distribution=" + "\"" + str(n_capital_dis) + "\""+" where u_id="+ "\""+str(buildings[i])+"\""
            update_sql = "update buildings_info set b_date_distribution=" + "\"" + str(n_date_dis) + "\"" + " where u_id=" + "\"" + str(buildings[i]) + "\""
            cur_test.execute(update_sql)
            conn_test.commit()
        except Exception as e:
            print(e)
        print("**************************")

    cur_test.close()
    conn_test.close()


# 获取所有建筑uuid
def get_buildings():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    sql_test = "select u_id from buildings_info limit 1"
    building_uid = []
    cur_test.execute(sql_test)
    for row in cur_test.fetchall():
        building_uid.append(row[0])
    return building_uid

#获取到所有compnay_id
def get_stat(company_id):
    conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunkedata',
                                passwd='XingDongJia@2016',
                                db='dataprocess',
                                charset='utf8'
                                )
    cur = conn_gs.cursor()
    stat=[]
    capital=[]
    redate=[]
    hangye=[]
    for i in range(0, len(company_id)):
        sql="select capital,registrationdate,hangye from company_yunke where id="+"\""+str(company_id[i])+"\""
        cur.execute(sql)
        for row in cur.fetchall():
            capital.append(row[0])
            redate.append(row[1])
            hangye.append(row[2])
    stat.append(capital)
    stat.append(redate)
    stat.append(hangye)

    cur.close()
    conn_gs.close()
    return stat


# def get_tyc_summery(company_id):
#     conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
#                                 port=3306,
#                                 user='yunker',
#                                 passwd='yunker2016EP',
#                                 db='xddb',
#                                 charset='utf8'
#                                 )
#     cur_only = conn_only.cursor()
#     clueid=[]
#     for k in range(0,len(company_id)):
#         cur_only.execute("select CLue_Id from crm_t_clue where commercialDB_id="+"\""+str(company_id[k])+"\"" )
#         for r in cur_only.fetchall():
#             clueid.append(r[0])
#             break
#     cur_only.close()
#     conn_only.close()
#
#     conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
#                                 port=3306,
#                                 user='yunker',
#                                 passwd='yunke2016',
#                                 db='alg',
#                                 charset='utf8'
#                                 )
#     cur_test = conn_test.cursor()
#     summary=[]
#     for i in range(0,len(clueid)):
#         sql = "select c_tyc_summary from clue_feature where Clue_Id=" + "\"" +clueid[i]+ "\""
#         cur_test.execute(sql)
#         for row in cur_test.fetchall():
#             summary.append(row[0])
#             break
#     return summary


if __name__=='__main__':
    stat_info()
    # dd="{'批发和零售业': 2, '房地产业': 3, '无': 0, '文化、体育和娱乐业': 4, '科学研究和技术服务业': 1, '住宿和餐饮业': 2, '租赁和商务服务业': 6}"
    # dict_dd=eval(dd)
    # for k,v in dict_dd.items():
    #     if v!=0:
    #         print(k)
    pass