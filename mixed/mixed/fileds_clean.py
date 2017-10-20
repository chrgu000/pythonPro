# -*- coding: utf-8 -*

import pymysql
import logging
import re

#清洗线索库的字段
# Clue_Entry_Major,
# registed_capital_num

log_file = "feature_table.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG)

def major_clean(old):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur = conn_only.cursor()
    sql = "SELECT CLue_Id FROM crm_t_clue where Clue_Entry_Major="+"\""+old+"\""
    cur.execute(sql)
    id_list=[]
    for row in cur.fetchall():
        id_list.append(row[0])
    cur.close()
    conn_only.close()
    return id_list

def major_up_clean(id_list,new):
    conn = pymysql.connect(host='rds5943721vp4so4j16r.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_o = conn.cursor()
    for i in range(0,len(id_list)):
        idd=id_list[i].replace("\n","")
        print(idd)
        sql_up = "UPDATE crm_t_clue SET Clue_Entry_Major=" + "\"" + new+ "\"" + " where CLue_Id=" + "\"" + idd + "\""
        cur_o.execute(sql_up)
    cur_o.close()
    conn.commit()
    conn.close()

def capital_clean(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    #sql = "SELECT CLue_Id,registed_capital FROM crm_t_clue limit  "+str(start)+","+str(banchsize)
    sql="SELECT CLue_Id,registed_capital FROM crm_t_clue WHERE CLue_Id IN (SELECT CLue_Id FROM crm_t_clue) limit " +str(start)+","+str(banchsize)
    data_list=[]
    cur_only.execute(sql)
    for row in cur_only.fetchall():
        clue_id =row[0]
        capital =row[1]
        num = re.findall("\d+", capital)
        capital_num="0"
        capital_currency="人民币"
        if len(num)>=1 and int(num[0])>0:
            capital_num=str(int(num[0])*10000)
        if "美元" in capital:
            capital_currency="美元"

        data_list.append(clue_id+"#"+capital_num+"#"+capital_currency)
        #print(clue_id+"#"+capital_num+"#"+capital_currency)

    cur_only.close()
    conn_only.close()
    return data_list

def updata_capital(data_list):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    for i in range(0, len(data_list)):
        clueid = data_list[i].split("#")[0]
        capital_num = data_list[i].split("#")[1]
        update_test = "UPDATE clue_feature SET c_reg_capital=" + capital_num + " where Clue_Id=" + "\"" + clueid + "\""
        print(update_test)
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()

def crm_updata_capital(data_list):
    conn_formal = pymysql.connect(host='rds5943721vp4so4j16r.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )

    cur_formal = conn_formal.cursor()
    for i in range(0, len(data_list)):
        clueid = data_list[i].split("#")[0]
        capital_num = data_list[i].split("#")[1]
        capital_curr= data_list[i].split("#")[2]
        update_test = "UPDATE crm_t_clue SET registed_capital_num=" + capital_num +","+"registed_capital_currency="+"\""+capital_curr+"\"" + " where Clue_Id=" + "\"" + clueid + "\""
        try:
            cur_formal.execute(update_test)
        except Exception as e:
            print(e)
    cur_formal.close()
    conn_formal.commit()
    conn_formal.close()

if __name__ == '__main__':
    # old="Manager"
    # new="经理"
    # id_list=major_clean(old)
    # major_up_clean(id_list,new)
    # 00006eb209bf11e7bde500163e006499检测？
    start = 3412000
    banchsize = 100000
    while (True):
        data_list=capital_clean(start,banchsize)
        if len(data_list) == 0: break
        crm_updata_capital(data_list)
        start += banchsize
        print("第" + str(start) + "完成")
    pass