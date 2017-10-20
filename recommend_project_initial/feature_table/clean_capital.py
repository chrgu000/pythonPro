# -*- coding: utf-8 -*

import pymysql

# registed_capital_num,
# registed_capital_currency

def clean_capital(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql_only = "SELECT CLue_Id,registed_capital_num,registed_capital_currency FROM crm_t_clue limit "+str(start)+","+str(banchsize)+";"
    cur_only.execute(sql_only)

    data=[]
    for row in cur_only.fetchall():
        cid = str(row[0])

        #*************registed_capital_num（注册资金）,registed_capital_currency******************
        # 如果无，值="-1"
        capital = "-1"
        if str.isdigit(str(row[1]))==True :
            if str(row[1])=="人民币":
                capital= str(row[5])
            if str(row[1])=="美元":
                capital=str(int(str(row[2])) * 6.5)#(美元兑人民币汇率：6.5)

        data.append(cid+"#"+str(capital))
    cur_only.close()
    conn_only.close()
    return data

if __name__ == '__main__':
    pass
