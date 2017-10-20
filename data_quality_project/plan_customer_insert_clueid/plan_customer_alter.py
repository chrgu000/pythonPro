# -*- coding: utf-8 -*
'''
定时任务：每天处理新进入的电话记录
    crm_t_plan_customer表中添加Clue_Key字段，该字段是线索的id，将用户行为与线索联系起来
    crm_t_clue_plan表中添加Clue_Key字段，该字段是线索的id
'''

import pymysql
from elasticsearch import Elasticsearch
es = Elasticsearch("123.57.62.29", timeout=200)

def add_clue_id(dead_time):
    conn_formal = pymysql.connect(host='rds5943721vp4so4j16r.mysql.rds.aliyuncs.com',
                                  port=3306,
                                  user='yunker',
                                  passwd='yunker2016EP',
                                  db='xddb',
                                  charset='utf8'
                                  )
    cur_formal = conn_formal.cursor()

    cur_formal.execute("SELECT Plan_Customer_Id,Cellphone FROM crm_t_plan_customer where Created_Time>"+"\""+dead_time+"\"")
    for r in cur_formal.fetchall():
        cid = get_cid(str(r[1]))
        if cid != "":
            cur_formal.execute("update crm_t_plan_customer set Clue_Key="+"\""+cid+"\""+" where Plan_Customer_Id="+"\"" + r[0]+"\"")
            conn_formal.commit()

    # cur_formal.execute("SELECT Clue_Downloaded_Id,Clue_Entry_Cellphone FROM crm_t_clue_plan where Created_Time>"+"\""+dead_time+"\"")
    # for r in cur_formal.fetchall():
    #     cid = get_cid(str(r[1]))
    #     if cid != "":
    #         cur_formal.execute("update crm_t_clue_plan set Clue_Key="+"\""+cid+"\""+" where Clue_Downloaded_Id="+"\"" + r[0]+"\"")
    #         conn_formal.commit()
    cur_formal.close()
    conn_formal.close()


def get_cid(cellphone):
    clue_id = ""
    quary = {
        "query": {
                "term": {
                        "Clue_Entry_Cellphone": cellphone
                    }
        },
    }
    result = es.search(index="clue_filtered", doc_type="clue", body=quary)
    count = int(result["hits"]["total"])
    if count != 0:
        clue_id = result["hits"]["hits"][0]["_source"]["CLue_Id"]
    else:
        result = es.search(index="clue_not_filtered", doc_type="clue", body=quary)
        count_ = int(result["hits"]["total"])
        if count_ != 0:
            clue_id = result["hits"]["hits"][0]["_source"]["CLue_Id"]

    return clue_id


if __name__ == '__main__':
    # add_clue_id("2016-01-01 00:00:00")
    pass
