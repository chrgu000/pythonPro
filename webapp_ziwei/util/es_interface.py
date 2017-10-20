#! -*- coding:utf-8 -*-

import json
import math
import time
import logging
import pandas as pd

from tornado import gen
from tornado import web

from .es.es_util_generatePart import *
from ..__init__ import logger

from elasticsearch import Elasticsearch
from .es.tornado_elasticsearch import AsyncElasticsearch

# es = Elasticsearch("123.57.62.29",timeout=200)

clueIP = "123.57.62.29"
actionIP = "47.93.78.47"
clueES = AsyncElasticsearch(clueIP,timeout=200)
# clueESSync = Elasticsearch(clueIP,timeout=200)
actionES = AsyncElasticsearch(actionIP,timeout=200)
DEFAULT_WEBINDEX_NUM = 50
MAX_WEBINDEX_NUM = 100

@gen.coroutine
def query_clueDB_aggregation(searchFilter,keyword_field="Clue_Entry_Com_Name"):
    '''用聚合操作查询     
    
    Arguments:
        searchFilter {dict} -- 搜索条件
        keyword_field {string} -- 查询的字段 Clue_Entry_Com_Name 或 main_produce
    
    Returns:
        dict -- 每个关键词对应的线索数量
    '''
    keyword_list=[]
    if keyword_field == "Clue_Entry_Com_Name":
        keyword_list=searchFilter['comname_list']
    if keyword_field == "main_produce":
        keyword_list=searchFilter['business_list']

    #### aggs dict
    aggs_dict={}
    shd_list=[]
    for keyword in keyword_list:
        aggs_dict[keyword_field+' = '+keyword]={"filter": {"match_phrase": {keyword_field: keyword}}} 
        shd_list.append({"match_phrase": {keyword_field: keyword}})

    # #### 2-gram
    # for i in range(len(keyword_list))[:]:
    #     for j in range(len(keyword_list)):
    #         if i==j:continue
    #         pair=keyword_list[i]+' '+keyword_list[j]
    #         aggs_dict[pair+'_'+keyword_field]={"filter": {"match":{keyword_field:{"query":pair, "operator":"and"}}}} 

    query={
        "query": generateQuery(searchFilter,shd_list),
        "aggs":aggs_dict
    }
    logger.info('ES query string:\n%s',json.dumps(query,indent = 2,ensure_ascii=False))

    startTime = time.time()
    try:
        rs = yield clueES.search(index='clue_*filtered',doc_type="clue",scroll='80s',size=500,body=query)
    except Exception as e:
        raise e #elasticsearch exception
    query_total = rs['hits']['total']
    key_count={}

    if len(aggs_dict)!=0:
        agg=rs['aggregations']
        for agg_name,v in list(agg.items()):
            key_count[agg_name]=v['doc_count']        

    keywords={"total":query_total,"keywords":key_count}
    return keywords

def prepareQuery(searchFilter,clueNum,from_=0):
    shd_comname=[];shd_product=[];

    ### should query
    comName_list=[w for w in searchFilter["comname_list"] if len(w)>1 and len(w)<9]
    product_list=[w for w in searchFilter["business_list"] if len(w)>1 and len(w)<9]

    for name in comName_list:
        shd_comname.append({"match_phrase":{"Clue_Entry_Com_Name": name }})
    for product in product_list:
        shd_product.append({"match_phrase":{"main_produce": product }})
        shd_product.append({"match_phrase":{"param8": product }})


    # clue_filtered 和clue_not_filtered 一共有8个分片，一次最多可以拿到8 * clueNum条数据
    query={
            "query": generateQuery(searchFilter,shd_product+shd_comname), 

            "from":from_,
            "size":clueNum,
            # "sort": [{ "_doc":"asc"}]         # 加上这个之后优先从clue_filtered里面获取

        }
    return query

@gen.coroutine
def query_clueDB(query,cominfo_mode,company_source={}):
    logger.info('ES query string:\n%s',json.dumps(query,indent = 2,ensure_ascii = False))

    startTime = time.time()
    try:
        rs = yield clueES.search(index='clue_*',doc_type="clue",body=query)
    except Exception as e:
        raise e #elasticsearch exception
    #whether cominfo is must included
    cominfo_flag="com_info" if cominfo_mode==True else "CLue_Id"

    scroll_size = rs['hits']['total']
    logger.info("scroll_size:%d",scroll_size)
    hit_list=rs['hits']['hits']
    for hit in hit_list:
        cid=hit['_id'];
        if cid not in company_source:
            if cominfo_flag in hit['_source'] and hit['_source'][cominfo_flag] not in ['',None,'null']:
                company_source[cid]=hit['_source']#{field:v}

    return company_source

def select_attribute(cid_source):
    cid_produce={}

    for cid,source in list(cid_source.items()):

        obs={}
        for att in attList[:]:
            if att in hit['_source'] and hit['_source'][att]!=None:
                obs[att]=hit['_source'][att]
            else:
                obs[att]=''
        cid_produce[cid]=obs

def select_produce(cid_source,attList): #{cid:sourceDict...}
    cid_produce={}
    for cid,source in list(cid_source.items())[:]:
        cid_produce[cid]=''
        for att in attList:
            if att in source and source[att] not in ['',None]:
                cid_produce[cid]+=' '+source[att];
    return cid_produce

def select_produce_name(cid_source,attList): #{cid:sourceDict...}
    cid_produce={}
    for cid,source in list(cid_source.items())[:]:

        cid_produce[cid]={}
        for att in attList[:]:
            if att in source and source[att] not in ['',None]:

                cid_produce[cid][att]=source[att];
            else:cid_produce[cid][att]=''

    return cid_produce

@gen.coroutine   
def getPaginationFrom(userID):
    query = {"query":{"term":{"User_Id":userID}},"_source":"recommendation_page"}
    try:
        rs = yield clueES.search(index = "portaluser", doc_type = "user", size=1,body = query )
    except Exception as e:
        raise e #elasticsearch exception
    total = rs["hits"]["total"]
    if total == 0:
        raise LookupError(userID)
    if total > 1:
        logger.warning("The userID matchs multiple users")
    try:
        PaginationFrom = int(rs["hits"]["hits"][0]["_source"]["recommendation_page"])
        PaginationFrom = PaginationFrom>>24
        PaginationFrom &= 255
        return PaginationFrom
    except Exception as e:
        return 0

@gen.coroutine
def queryAllCompanySource(searchFilter,clueNum,bypage=False):

    keyword_business=searchFilter["business_list"]
    keyword_business = [w for w in keyword_business if len(w)>1]

    company_source={}
    searchFilter["business_list"]=keyword_business
    if bypage:
        from_ = yield getPaginationFrom(searchFilter["ID"])
        query = prepareQuery(searchFilter,clueNum,from_)
    else:
        query = prepareQuery(searchFilter,clueNum)
    company_source = yield query_clueDB(query,searchFilter["cominfoRequired"],company_source)

    searchFilter["business_list"] = keyword_business
    logger.info("len(company_source): %d",len(company_source))
    # 获取主营产品和经营范围(param8)
    attList_companyDB=['param8','main_produce']
    cid_produce=select_produce(company_source,attList_companyDB)
    return company_source,cid_produce

@gen.coroutine
def getPortalUserByIDES(userID):
    query = {"query":{"term":{"User_Id":userID}}}
    try:
        rs = yield clueES.search(index = "portaluser", doc_type = "user", size=1,body = query )
    except Exception as e:
        raise e #elasticsearch exception

    total = rs["hits"]["total"]
    if total == 0:
        raise Exception("用户不存在：",userID)

    if total > 1:
        logger.warning("该ID匹配多个用户")

    return rs["hits"]["hits"][0]["_source"]

@gen.coroutine
def getIntendedCompanys(companyCode,number=DEFAULT_WEBINDEX_NUM):
    '''获取最近有意向的客户信息
    '''
    if number>MAX_WEBINDEX_NUM: number = MAX_WEBINDEX_NUM
    fields = ["companyCode","actionType","company","mainProduce","createdTime"]
    names = ["code","intend","name","business","time"]
    renameDict = {key:value for (key,value) in zip(fields,names)}
    query=  \
        {"query":
            {"bool":
                {"filter":[
                    {"term": {"companyCode": companyCode}},
                    {"term": {"actionType": 1}}
                ]}
            },
            "sort":[{"createdTime":"desc"}],
            "_source":fields,
            "size":number
        }

    try:
        rs = yield actionES.search(index = "webindex", doc_type = "pc", scroll = "60s", body = query)
    except Exception as e:
        if e.status_code == 400:
            raise Exception("找不到最近有意向的客户")
        raise e #elasticsearch exception

    Companys = [hit["_source"] for hit in rs['hits']['hits']]
    df = pd.DataFrame(Companys)
    df.rename(columns = renameDict, inplace=True)

    return df


