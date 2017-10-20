# -*- coding: utf-8 -*

import pymysql
def get_no_match_company():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    cid_list = []
    cur_test.execute("select c_id from company_connection_building")
    for r in cur_test.fetchall():
        cid_list.append(r[0])
    print("**********")

    # 测试库--工商库
    conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                              port=3306,
                              user='yunkedata',
                              passwd='XingDongJia@2016',
                              db='dataprocess',
                              charset='utf8'
                              )
    cur_gs = conn_gs.cursor()
    cur_gs.execute("select id,title,address from company_yunke where province="+"\""+"北京市"+"\"")
    for r in cur_gs.fetchall():
        if r[0] not in cid_list:
            try:
                sql="insert into no_match_company(c_id,c_name,c_addr) VALUES ("+ "\""+str(r[0])+"\","+"\""+r[1]+"\","+"\""+r[2]+"\""+")"
                print(sql)
                cur_test.execute(sql)
                conn_test.commit()
            except Exception as e:
                print(e)
    cur_gs.close()
    conn_gs.close()
    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    get_no_match_company()
    pass