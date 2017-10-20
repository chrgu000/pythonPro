#!user/bin/env python3  
#-*- coding: utf-8 -*

import json
import re
import sys
import time

import jieba
import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

sys.path.append("../webapp")
sys.path.append("../updateClues")
from pack.util.NLP_tool import (remove_allegedNotParticipate,
                                remove_brace_content, splitParagraph2Sentences)
from clean_mysql.process_name_comname_birthday import leads_name

es = Elasticsearch("123.57.62.29", timeout=200)
# 1. 统计包含行业的公司数目(3816294)
# 2. 同时包含行业和公司简介的公司数目
# hangye            3816294
# content           17828290
# hangye  content   3223228
# product           15103592
# business          16065718
# product business  12739093


def getCompanyContainsX():
    query = {
        "query": {
            "bool": {
                "filter": [
                    {"exists": {
                        "field": "hangye"
                    }},
                    {"exists": {
                        "field": "content"
                    }}
                ]
            }
        }
    }

    rs = es.search(index="company_1", doc_type="company",
                   search_type="scan", scroll="10s", body=query)
    docNum = rs["hits"]["total"]
    print(docNum)

# 3. 把所有行业字段获取到本地存入字典，应该避免相同的词语


def getAllFields(field, dataType="list"):
    '''提取线索/公司某个字段所有值'''
    query = {
        "query": {
            "bool": {
                "filter": [{
                    "exists": {
                        "field": field
                    }
                }]
            }
        },
        "_source": [field]
    }
    # rs = es.search(index = "company_1", doc_type = "company", search_type = "scan", size = 10000, scroll = "500s", body = query)
    rs = es.search(index="clue_*filtered", doc_type="clue",search_type="scan", size=10000, scroll="500s", body=query)
    docNum = rs["hits"]["total"]
    print(docNum)
    data = None
    if "set" == dataType:
        data = set()
    elif "list" == dataType:
        data = list()
    else:
        return

    while docNum != 0:
        rs = es.scroll(scroll='200s', scroll_id=rs["_scroll_id"])
        docNum = len(rs["hits"]["hits"])
        hits = [hit["_source"][field].strip() for hit in rs["hits"]["hits"]]
        hits = [hit for hit in hits if hit != ""]
        if "set" == dataType:
            data |= set(hits)
        elif "list" == dataType:
            data.extend(hits)
        print(len(data))
        pd.to_pickle(data, "./temp/" + field + dataType)

def getAggsFromES(field):
    query = {
        "size": 0,
        "aggs": {
            "major": {
                "terms": {
                    "field": field,
                    "size": 10000
                }
            }
        }
    }

    rs = es.search(index = "clue_*",doc_type = "clue", body = query)
    buckets = rs["aggregations"]["major"]["buckets"]
    wordSet = set([bucket["key"] for bucket in buckets if len(bucket["key"])>1 and bucket["doc_count"]>100])
    pd.to_pickle(wordSet, "temp/" + field + "WordSet")

def processField2Dict(field):
    '''提取职位和行业分类的字典'''
    data = pd.read_pickle("./temp/"+field+"list")
    fieldDict = {}
    for industry in data:
      if industry not in fieldDict:
          fieldDict[industry] = 1
      else: fieldDict[industry] += 1
    pd.to_pickle(fieldDict,"./temp/"+field+"Dict")

def processField2Dict1(field):
    fieldDict = pd.read_pickle("./temp/" + field + "Dict")
    print(json.dumps(fieldDict, indent=2, ensure_ascii=False))
    arr = np.array(list(fieldDict.values()))
    print(np.sum(arr))

def processField2Dict2(field):
    '''提取职位和行业分类的字典'''
    fieldDict = pd.read_pickle("./temp/" + field + "Dict")

    countDict = {}
    for k,v in fieldDict.items():
        if field == "param1":       # 职位里面包含不必要的逗号
            k = k.replace(',','|')
        positions = k.split("|")
        for pos in positions:
            if pos in countDict: countDict[pos] += v
            else: countDict[pos] = v

    print(json.dumps(countDict, indent=2, ensure_ascii=False))
    arr = np.array(list(fieldDict.values()))
    print(np.sum(arr))

def getNum():
    '''查询满足条件的线索/公司的数量'''
    query = {
        "query": {
            "bool": {
                "must": [
                    {"script": {
                        "script": "doc['main_industry'].size() < 2"
                    }},
                ],
                "must_not": [
                    {"exists": {"field": "cominfo_vector"}},
                    {"script": {
                        "script": "doc['main_produce'].size() > 2"
                    }},
                    {"script": {
                        "script": "doc['param8'].size() > 2"
                    }},
                ],
                "minimum_should_match": 1,
                "boost": 1.0
            }
        }
    }
    # rs = es.search(index = "company_1", doc_type = "company", search_type = "scan", size = 10, scroll = "10s", body = query)
    rs = es.search(index="clue_*filtered", doc_type="clue", search_type="scan", size=10, scroll="10s", body=query)
    docNum = rs["hits"]["total"]
    print(docNum)
    return


def statClueField():
    pass


def statCompanyField():
    pass

def processField2WordSet(field):
    '''提取公司名称、主营产品和经营范围中出现过的词语'''
    fieldlist = pd.read_pickle("temp/"+ field + "list")
    fieldWordSet = set()
    print(len(fieldlist))
    for i in range(len(fieldlist)):
        if i%10000 == 0: print(i)
        if field == "product":
            fieldWordSet |= set(jieba.cut(fieldlist[i]))
        elif field == "business":
            string = remove_brace_content(fieldlist[i])
            sentences = [sentence for sentence in splitParagraph2Sentences(string)]
            ll=remove_allegedNotParticipate(sentences);
            ls = []
            for phrase in ll:
                ls.extend(jieba.cut(phrase))
            fieldWordSet |= set(ls)
        elif field == "companyName":
            fieldWordSet |= set(jieba.cut(fieldlist[i]))
    pd.to_pickle(fieldWordSet,"temp/" + field + "WordSet")

def filterNonChinese(field):
    '''词语集合中去掉英文数字标点符号'''
    wordSet = pd.read_pickle("temp/" + field + "WordSet")
    words=[]
    for word in wordSet:
        if re.sub(r'[^\u4e00-\u9fbf]+','',word) == '':
            words.append(word)
    wordSet -= set(words)
    pd.to_pickle(wordSet,"temp/" + field + "WordSet_chinese")

def mixProductAndBusiness():
    '''混合主营产品和经营范围所有词语'''

    wordset1 = pd.read_pickle('temp/productWordSet_chinese')
    wordset2 = pd.read_pickle('temp/businessWordSet_chinese')
    wordset3 = wordset1 | wordset2
    pd.to_pickle(wordset3,'temp/productBusinessWordSet_chinese')
    print(len(wordset1))
    print(len(wordset2))
    print(len(wordset3))
    print(len(wordset1) + len(wordset2) - len(wordset3))
    
    
def processNameSet():
    file1 = open("temp/name.txt",'r')
    file2 = open("temp/name2.txt",'r')
    name1 = file1.readlines()
    name2 = file1.readlines()
    file1.close()
    file2.close()

    name1set = set([leads_name(name) for name in name1])
    name2set = set([leads_name(name) for name in name2])
    wordSet = name1set | name2set
    pd.to_pickle(wordSet,"temp/nameSet")


def denoiseKeyword(field):
    ''''''
    wordSet = pd.read_pickle("temp/" + field + "WordSet_chinese")
    # 以地名为主
    noiseList = pd.read_pickle("../webapp/pack/model/lib/noise_extend")
    wordSet -= set(noiseList)

    # 人名
    nameSet = pd.read_pickle("temp/nameSet")
    wordSet -= nameSet
    
    pd.to_pickle(wordSet,"temp/" + field + "WordSet_ch_clean")

def generateDict(field,num):
    model = pd.read_pickle("../webapp/pack/model/lib/word2vecModel")
    fieldWordSet = pd.read_pickle("temp/" + field + "WordSet_ch_clean")
    print(len(fieldWordSet))
    fieldDict = {}
    count = 0
    for word in fieldWordSet:
        if word in model.wv:            
            l = model.similar_by_word(word,num)
            fieldDict[word] = [w for w,d in l if w in fieldWordSet]
            count += len(fieldDict[word])

    print("average synonym word %f"%(count/len(fieldDict)))
    print(len(fieldDict))
    pd.to_pickle(fieldDict,'../webapp/pack/model/lib/synonym' + field)

def testSynonym(field):

    fieldDict = pd.read_pickle('../webapp/pack/model/lib/synonym' + field)

    while True:
        try:            
            word = input()
            print(fieldDict[word])
        except Exception as e:
            # print(str(type(e))+": "+str(e))
            pass



if __name__ == '__main__':
    '''
    getAllFields("main_industry","list")          # 行业 8024015
    getAllFields("param1","list")                 # 职位 12352169
    getAllFields("product","list")                # 主营产品
    getAllFields("business","list")               # 经营范围

    processField2Dict("param1")
    processField2Dict("main_industry")
    processField2Dict1("param1")
    processField2Dict1("main_industry")
    processField2Dict2("param1")
    processField2Dict2("main_industry")
    # {行业字段，主营产品，经营范围}

    # 公司名称近义词提示
    # 获取所有公司名称中出现的词语
    processField2WordSet("product")
    processField2WordSet("business")
    processField2WordSet("companyName")
    getAggsFromES("Clue_Entry_Major")
    
    filterNonChinese("product")
    filterNonChinese("business")
    filterNonChinese("companyName")
    mixProductAndBusiness()

    filterNonChinese("Clue_Entry_Major")

    processNameSet()

    print("noiseproduct")
    denoiseKeyword("productBusiness")
    print("noisecomname")
    denoiseKeyword("companyName")
    print("noisemajor")
    denoiseKeyword("Clue_Entry_Major")

    print("genproductdict")
    generateDict("productBusiness",5)
    print("gencomnamedict")
    generateDict("companyName",5)
    print("genmajordict")
    generateDict("Clue_Entry_Major",30)
    '''
    


    # testSynonym("productBusiness")
    # testSynonym("companyName")
    # testSynonym("Clue_Entry_Major")

