# -*- coding: utf-8 -*
'''
定时任务：每天将新进入的电话记录更新
    crm_t_plan_customer表中添加Clue_Key字段，该字段是线索的id，将用户行为与线索联系起来
'''
import numpy as np

from elasticsearch import Elasticsearch
es = Elasticsearch("123.57.62.29", timeout=200)


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
    print(clue_id)
    return clue_id


if __name__ == '__main__':
    # get_cid("15312695108")
    cols = 2
    rows = 3

    # This works
    matrix_a = np.zeros(3)
    print(matrix_a)

    pass
