# -*- coding: utf-8 -*
'''
对于company_no_match表中的公司，重新与楼宇建立连接
'''

import pymysql
def get_no_match_company():
    no_match_company=[]
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    sql_no_match="select c_id from company_no_match"
    cur_test.execute(sql_no_match)
    for row in cur_test.fetchall():
        no_match_company.append(row[0])
    return no_match_company

def get_no_match_company_info():
    conn_test_business = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                         port=3306,
                                         user='yunkedata',
                                         passwd='XingDongJia@2016',
                                         db='dataprocess',
                                         charset='utf8'
                                         )
    cur_test_business = conn_test_business.cursor()
    no_match_company=get_no_match_company()
    no_match_company_info=[]
    for i in range(0,len(no_match_company)):
        sql_no_match = "select address from company_yunke WHERE id="+"\""+no_match_company[i]+"\""
        cur_test_business.execute(sql_no_match)
        for row in cur_test_business.fetchall():
            no_match_company_info.append(no_match_company[i]+"%"+row[0])
    return no_match_company_info


if __name__=='__main__':
    get_no_match_company_info()
    pass