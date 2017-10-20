#!user/bin/env python3
#-*- coding: utf-8 -*

from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch("123.57.62.29", timeout=200)

# ****************从es上获取数据*******************
def get_data_from_es(start, size):
    clue_id = []
    quary = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match_all": {}
                    }
                ]
            }
        },
        "from": start,
        "size": size,
        "sort": [],
        "aggs": {}
    }

    result = es.search(index="clue_filtered", doc_type="clue", body=quary)

    for i in range(0, len(result["hits"]['hits'])):
        hit_data = result["hits"]['hits'][i]['_source']
        if type(hit_data['commercialDB_id']) == type(1) and type(hit_data['tfidf_keyword']) != type("1"):
            clue_id.append(hit_data['CLue_Id'] + ":" + str(hit_data['commercialDB_id']))

    return clue_id


# ****************连接es，将得到的数据插入es,批量插入数据*******************
def data_to_es(es, data):
    # 创建ACTIONS,每500条数据进行一次批量导入
    ACTIONS = []
    for line in data:
        clue_id = line.split(":")[0]
        clue_keyword = line.split(":")[1]

        action = {
            "_op_type": 'update',
            # "_index": "clue_not_filtered",
            "_index": "clue_filtered",
            "_type": "clue",
            "_id": clue_id,
            "_score": "1",
            "doc": {
                "tfidf_keyword": clue_keyword
            }
        }
        ACTIONS.append(action)
    helpers.bulk(es, ACTIONS, request_timeout=1000)

if __name__ == '__main__':
    pass