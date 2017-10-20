# -*- coding: utf-8 -*
'''
连接测试工商库
get_pos_trainset(): 获取客户正样本训练集
get_neg_trainset(): 获取客户负样本训练集(从不感兴趣的表中获取)
get_neg_trainset_r(): 获取客户负样本训练集(随机从线索表抽取)
'''
import pymysql
import random
from datetime import datetime
from datetime import timedelta

def get_neg_trainset_r(pos_num,pos_sam_id):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    not_intersted_clueinfo = []
    while True:
        if len(not_intersted_clueinfo) < int(pos_num):
            rc = random.randint(0, 20000000)
            sql_1 = "select CLue_Id from crm_t_clue limit "+ str(rc) +",100"
            cur_only.execute(sql_1)
            for r in cur_only.fetchall():
                if str(r[0]) not in pos_sam_id:
                    not_intersted_clueinfo.append(str(r[0]))
        else:
            break
    cur_only.close()
    conn_only.close()
    return not_intersted_clueinfo
'''
正样本必须是近期打过的线索
'''
def get_pos_trainset_r(company_code):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    '''
    读取正样本，crm_t_plan_customer表，近7天打过的线索，如果超过500，取最近的500个线索作为正样本
    '''
    dead_time = str(datetime.now() - timedelta(days=7))
    sql_c = "select Clue_Key from crm_t_plan_customer where Company_Code="+"\""+company_code+"\"" +"and Created_Time >"+ "\""+dead_time+"\"" +"order by Created_Time DESC"
    clue_info = []
    cur_only.execute(sql_c)
    for row in cur_only.fetchall():
        if row[0] != None and len(str(row[0])) > 30:
            clue_info.append(row[0])
        if len(clue_info) > 500:
            break
    cur_only.close()
    conn_only.close()
    return clue_info

if __name__ == '__main__':
    pass