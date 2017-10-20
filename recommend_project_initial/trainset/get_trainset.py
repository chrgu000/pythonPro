# -*- coding: utf-8 -*
'''
连接测试工商库
get_pos_trainset(): 获取客户正样本训练集
get_neg_trainset(): 获取客户负样本训练集(从不感兴趣的表中获取)
get_neg_trainset_r(): 获取客户负样本训练集(随机从线索表抽取)
'''
import pymysql
import random
conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                            port=3306,
                            user='yunker',
                            passwd='yunker2016EP',
                            db='xddb',
                            charset='utf8'
                            )
cur = conn_only.cursor()
space = "%*"

def get_neg_trainset(company_code):
    #得到这个客户所有座席id
    sql_1 = "SELECT User_Id FROM crm_t_portaluser WHERE User_Company_Id=" + "'" + company_code + "'"
    cur.execute(sql_1)
    user_id = []
    for row in cur.fetchall():
        user_id.append(str(row[0]))

    # 这个公司在推荐结果中删除的线索，即不感兴趣的线索
    not_intersted_clueinfo=[]
    for u in user_id:
        sql_2 = "SELECT clue_id,create_time FROM crm_t_usernotinterested_clue WHERE user_id=" +"'" +u+ "'"
        cur.execute(sql_2)
        for r in cur.fetchall():
            not_intersted_clueid=r[0]
            time = r[1]
            #not_intersted_clueinfo.append(str(time) + space + str(not_intersted_clueid))
            not_intersted_clueinfo.append(str(not_intersted_clueid))
    return not_intersted_clueinfo

def get_neg_trainset_r(pos_num):
    not_intersted_clueinfo = []
    for i in range(0,int(pos_num/100)):
        rc=random.randint(0, 20000000)
        sql_1="select CLue_Id from crm_t_clue limit "+ str(rc) +",100"
        cur.execute(sql_1)
        for r in cur.fetchall():
            not_intersted_clueinfo.append(str(r[0]))
    return not_intersted_clueinfo


def get_pos_trainset(company_code):
    # 得到这个客户所有座席id
    sql_1 = "SELECT User_Id FROM crm_t_portaluser WHERE User_Company_Id=" + "'" + company_code + "'"
    cur.execute(sql_1)
    user_id = []
    for row in cur.fetchall():
        user_id.append(str(row[0]))

    # 这个公司打过的所有电话
    cus_info = []
    for user in user_id:
        sql_2 = "SELECT tip_type,Created_Time,Plan_Customer_Id FROM crm_t_call_action WHERE User_Id=" + "'" + user + "'"
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
        time = phone.split(space)[1]
        cell = phone.split(space)[2]

        sql_4 = "SELECT CLue_Id FROM crm_t_clue WHERE Clue_Entry_Cellphone='" + cell + "';"
        cur.execute(sql_4)
        for row in cur.fetchall():
            c_id = row[0]
            # clue_info.append(time + space + tp + space + c_id)
            clue_info.append(c_id)
    return clue_info

def get_pos_trainset_r(company_code):
    conn_test = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    sql="select clue_id from call_record where company_code="+"\""+company_code+"\""
    clue_info = []
    cur_test.execute(sql)
    for row in cur_test.fetchall():
        c_id = row[0]
        clue_info.append(c_id)
    return clue_info

if __name__ == '__main__':
    sql_companyCode="SELECT Company_code FROM crm_t_Company"
    cur.execute(sql_companyCode)
    for row in cur.fetchall():
        code=row[0]
        print("开始公司:"+code+"的训练正样本搜集 ing")
        get_pos_trainset(code)
        print("开始公司:" + code + "的训练负样本搜集 ing")
        get_neg_trainset(code)
    pass