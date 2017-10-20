# -*- coding: utf-8 -*

import pymysql
import logging
import re

# registed_capital_num,注册资金

log_file = "feature_table.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG)

def capital_clean(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql = "SELECT CLue_Id,registed_capital FROM crm_t_clue limit  "+str(start)+","+str(banchsize)
    data_list=[]
    cur_only.execute(sql)
    for row in cur_only.fetchall():
        clue_id =row[0]
        capital =row[1]
        num = re.findall("\d+", capital)
        capital_num="0"
        if len(num)>=1 and int(num[0])>0:
            capital_num=str(num[0])
        if len(num)>=1 and int(num[0])>0 and "美元" in capital:
            capital_num=str(int(num[0])*6.6)

        data_list.append(clue_id+"#"+capital_num)

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
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()


if __name__ == '__main__':
    start = 0
    banchsize = 10000
    while (True):
        data_list=capital_clean(start,banchsize)
        if len(data_list) == 0: break
        updata_capital(data_list)
        start += banchsize
        print("第" + str(start) + "完成")
    pass