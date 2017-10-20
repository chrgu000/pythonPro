# -*- coding: utf-8 -*
'''
连接测试工商库
get_pos_trainset(): 获取客户正样本训练集，存入库，定时更新
'''
import pymysql
import time
from datetime import datetime
from datetime import timedelta

conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                            port=3306,
                            user='yunker',
                            passwd='yunker2016EP',
                            db='xddb',
                            charset='utf8'
                            )
cur = conn_only.cursor()
space = "&"

def get_pos_trainset(company_code):
    # 得到这个客户所有座席id
    sql_1 = "SELECT User_Id FROM crm_t_portaluser WHERE User_Company_Id=" + "'" + company_code + "'"
    cur.execute(sql_1)
    user_id = []
    for row in cur.fetchall():
        user_id.append(str(row[0]))

    # 这个公司打过的所有电话
    cus_info = []
    tic_limit = str(datetime.now() - timedelta(days=1))
    # print("更新的时间段："+tic_limit+"-"+str(time.time()))
    for user in user_id:
        sql_2 = "SELECT tip_type,Created_Time,Plan_Customer_Id FROM crm_t_call_action WHERE User_Id=" + "'" + user + "'"+"and Created_Time>"+"\""+tic_limit+"\""
        cur.execute(sql_2)
        for row in cur.fetchall():
            cus_info.append(str(row[0]) + space + str(row[1]) + space + str(row[2]))

    phone_info = []
    for cus in cus_info:
        tp = cus.split(space)[0]
        created_time = cus.split(space)[1]
        customer_id = cus.split(space)[2]
        sql_3 = "SELECT Cellphone FROM crm_t_plan_customer WHERE Plan_Customer_Id=" + "'" + customer_id + "'"
        cur.execute(sql_3)
        for row in cur.fetchall():
            phone_info.append(tp + space + created_time + space + str(row[0]))

    clue_info = []
    for phone in phone_info:
        tp = phone.split(space)[0]
        tim = phone.split(space)[1]
        cell = phone.split(space)[2]

        sql_4 = "SELECT CLue_Id FROM crm_t_clue WHERE Clue_Entry_Cellphone='" + cell + "';"
        cur.execute(sql_4)
        c_id=""
        for row in cur.fetchall():
            c_id = row[0]
        clue_info.append(company_code+ space +tim + space + tp + space + c_id)
    return clue_info

def update_record_clue():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    sql_0 = "select  Company_Code FROM crm_t_company "
    cur.execute(sql_0)
    companycode_list = []
    for r in cur.fetchall():
        companycode_list.append(r[0])

    for k in range(0,len(companycode_list)):
        company_code=companycode_list[k]
        clue_info=get_pos_trainset(company_code)
        for i in range(0,len(clue_info)):
            code=clue_info[i].split(space)[0]
            tim=clue_info[i].split(space)[1]
            typ=clue_info[i].split(space)[2]
            cid=clue_info[i].split(space)[3]
            if len(cid)>10:
                try:
                    sql_5 = "insert into call_record(clue_id,call_date,company_code,call_type) VALUES ("+"\""+cid+"\""+","+"\""+tim+"\""+","+"\""+code+"\""+","+"\""+typ+"\""+")"
                    cur_test.execute(sql_5)
                    conn_test.commit()
                except Exception as e:
                    print(str(code)+"*"+str(tim)+"*"+str(typ)+"*"+str(cid))
    cur_test.close()
    conn_test.close()
    cur.close()
    conn_only.close()

if __name__ == '__main__':
    update_record_clue()
    pass