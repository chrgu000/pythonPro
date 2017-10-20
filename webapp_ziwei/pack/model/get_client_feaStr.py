#! -*- coding:utf-8 -*-

import json
import os

import jieba
import numpy as np
import pandas as pd
from tornado import gen

from webapp_ziwei import loadRes
from webapp_ziwei import mainProduce_knn
from webapp_ziwei.pack.model import cominfoVec_knn
from .mainProduce_knn import analyze_business
from .modelHelper import postProcess
from ..__init__ import logger
from ..util.NLP_tool import *
from ..util.es_interface import getIntendedCompanys, getPortalUserByIDES, queryAllCompanySource
from ..util.sql_interface import query_synonym

word_idf_dict=loadRes(os.path.join('lib','word_idf_dict'))
noiseList=loadRes(os.path.join('lib','noise_extend'))

# synonymComNameDict=loadRes(os.path.join('lib','synonymcompanyName'))
# synonymProductBusinessDict=loadRes(os.path.join('lib','synonymproductBusiness'))
# synonymMajorDict=loadRes(os.path.join('lib','synonymClue_Entry_Major'))

companyNameWordSet = loadRes(os.path.join('lib','companyNameWordSet_chinese'))
productWordSet = loadRes(os.path.join('lib','productBusinessWordSet_chinese'))
majorWordSet = loadRes(os.path.join('lib','Clue_Entry_MajorWordSet_chinese'))

def calc_com_info_weight(cominfo_i): #cominfo_str -> {word:weight}
    # split
    ll=calculate_text(cominfo_i)
    wordList=[]
    # parsing + notParsing
    for w in ll:
        wordList+=wordParsingCut(w)
    wordList=[w for w in wordList if len(w)>1]
    word_weight_dict={}
    ## tfidf
    for word in wordList:
        if word in word_idf_dict:
            if word not in word_weight_dict:
                word_weight_dict[word]=word_idf_dict[word]
            else:word_weight_dict[word]+=word_idf_dict[word]
    return word_weight_dict

def idf_keyword(parse,n1):
    parseList=parse.split(' ')
    word_idf={}
    for word in parseList:
        if word in word_idf_dict:
            word_idf[word]=word_idf_dict[word]
    ###
    ll=sorted(iter(word_idf.items()),key=lambda s:s[1],reverse=True)
    n=n1 if len(ll)>=n1 else len(ll)
    return [p[0] for p in ll][:n]

    for x, w in jieba.analyse.textrank(sentence, topK=10,withWeight=True,allowPOS=('ns', 'n', 'vn', 'v')):
        if w>0.0:ll.append(x)
    return combine_parsed(ll)

def analyze_comname(comnameList):
    # 根据公司名称获取关键词
    # comnameList 公司名称列表
    comname_key_dict={}
    for comname in comnameList:
        if isinstance(comname,str):
            if comname in ['',None]:continue
            # yangrui version: 将括号等符号替换成空格，去掉数字和英文字母，对空格切分后的短语分词
            # ziwei version: 去掉括号中内容（无效信息），获取所有汉字，直接分词，结果一样
            comname=remove_brace_content(comname)
            comname=getChinese(comname)
            # 用jieba模块分词
            wordListRaw=wordParsingCut(comname,cut_all = False)#for search|False cut  |True cut all  
            # 去掉所有地名，以及”股份“，”有限“，”公司“等词语          
            wordList=[w for w in wordListRaw if w not in noiseList and len(w)>1]
            # 将分词结果加入字典中
            for word in wordList:
                if word not in comname_key_dict:comname_key_dict[word]=1
                else:comname_key_dict[word]+=1

            # 将连续两个词连接成一个词，加入字典中
            # 如           [ 古井   九方   制药   营销中心   ]
            # 连接结果为    [ 古井九方   九方制药   制药营销中心   ]
            if len(wordList)>=2:
                wordListCombined=combine_parsed(wordList)
                for word in wordListCombined:
                    if word not in comname_key_dict:comname_key_dict[word]=1
                    else:comname_key_dict[word]+=1

    return comname_key_dict

def sorted_dict(business_key_dict):
    business_pair=sorted(iter(business_key_dict.items()),key=lambda s:s[1],reverse=True)
    business_pair=[[s[0] for s in business_pair],[s[1]for s in business_pair]]
    return business_pair

@gen.coroutine
def prepareKeywords(userID,companyNum=100,kNum = 100):
    '''从公司列表中获取公司名称和主营产品的关键字
        companyNum 为分析的公司数
        kNum 为最大关键字数
    '''
    try:
        portalUser = yield getPortalUserByIDES(userID)
        companyCode = portalUser["User_Company_Id"]

        # 用户导入的用来打电话的样本
        # df = getCompanysFromBearCustomer(companyCode,["name","business"],companyNum)

        # 获取最近有意向的客户信息
        df = yield getIntendedCompanys(companyCode,companyNum)
        comnameList=df['name'][:companyNum]
        businessList=df['business'][:companyNum]

        comname_key_dict = analyze_comname(comnameList);
        business_key_dict = analyze_business(businessList)

        comname_key,comname_weight=sorted_dict(comname_key_dict)
        business_key,business_weight=sorted_dict(business_key_dict)

        keyword_comname={'keywords':comname_key[:kNum],'w':comname_weight[:kNum]}
        keyword_business={'keywords':business_key[:kNum],'w':business_weight[:kNum]}

        keywords = {'name':keyword_comname,'business':keyword_business}

        ######################### 记录日志 #######################
        try:
            dirpath = "./debugdata/"+userID+"/"
            if not os.path.exists(dirpath): os.mkdir(dirpath)

            filename = "portalUser.txt"
            portalUser = {key:value for key,value in portalUser.items() if value != None and value != ""}
            with open(dirpath+filename,"w") as file:
                file.write(json.dumps(portalUser,indent=2,ensure_ascii=False))

            filename = "recentIntendedCompanys.xls"
            df.to_excel(dirpath+filename)

            filename = "keywords.xls"
            length = max(len(keyword_comname["w"]),len(keyword_comname["w"]))
            name            = keyword_comname["keywords"]   + [""]*(length-len(keyword_comname["w"]))
            nameCount       = keyword_comname["w"]          + [np.nan]*(length-len(keyword_comname["w"]))
            business        = keyword_business["keywords"]  + [""]*(length-len(keyword_business["w"]))
            businessCount   = keyword_business["w"]         + [np.nan]*(length-len(keyword_business["w"]))
            df = pd.DataFrame({ "name":name,"nameCount":nameCount,
                                "business":business,"businessCount":businessCount})
            df.to_excel(dirpath+filename)
        except Exception as e:
            logger.warning("记录日志发生异常: "+str(type(e))+": "+str(e))
        ###########################################################

        return keywords

    except Exception as e:
        raise e

@gen.coroutine
def getRecommend(searchFilter,clueNum):
    if searchFilter["recoMode"] == "recoByKeywords".lower() and len(searchFilter["business_list"]) != 0:
        searchFilter["cominfoRequired"] = False
        company_source,cid_produce = yield queryAllCompanySource(searchFilter,clueNum,bypage=True)
        cidList = mainProduce_knn.getRecommendClueList(searchFilter['business_list'],cid_produce,company_source)

    elif searchFilter["recoMode"] == "recoByInfovect".lower():
        searchFilter["cominfoRequired"] = True    
        company_source,cid_produce = yield queryAllCompanySource(searchFilter,clueNum,bypage=True)
        cidList = cominfoVec_knn.getRecommendClueList(company_source, searchFilter["ID"])
    
    elif searchFilter["recoMode"] == "justSearch".lower():
        searchFilter["cominfoRequired"] = False
        company_source,cid_produce = yield queryAllCompanySource(searchFilter,clueNum,bypage=True)
        cidList = list(company_source.keys())

    else :
        raise Exception("推荐模式错误")

    clueList = postProcess(cidList,company_source,clueNum);
    clean_num = len([1 for data in clueList if data["param2"]==1])
    clean_rate=clean_num/len(clueList)

    ############################ 记录日志 ###########################
    try:
        userID = searchFilter["ID"]
        dirpath = "./debugdata/"+ userID +"/"
        if not os.path.exists(dirpath): os.mkdir(dirpath)

        portalUser = yield getPortalUserByIDES(userID)
        filename = "portalUser.txt"
        portalUser = {key:value for key,value in portalUser.items() if value != None and value != ""}
        with open(dirpath+filename,"w") as file:
            file.write(json.dumps(portalUser,indent=2,ensure_ascii=False))

        filename = "searchFilter.txt"
        searchFilter = {key:value for key,value in searchFilter.items() if value != None and value != ""}
        with open(dirpath+filename,"w") as file:
            file.write(json.dumps(searchFilter,indent=2,ensure_ascii=False))

        filename = "originalClue.xls"
        df = pd.DataFrame(list(company_source.values()))
        df.to_excel(dirpath+filename)

        filename = "processedClue.xls"
        df = pd.DataFrame(clueList)
        df.to_excel(dirpath+filename)
    except Exception as e:
        logger.warning("记录日志发生异常: "+str(type(e))+": "+str(e))
    ################################################################

    return clueList,clean_rate

def getSynonymFromDict(wordList,synonymDict):
    ret={}
    for word in wordList:
        word = getChinese(word)
        if word in synonymDict:
            ret[word]=" ".join(synonymDict[word])
    return ret

def filterWordSet(ret,wordSet):
    for word,wordstr in ret.items():
        wordList = wordstr.split(' ')
        # 过滤效果并不好
        wordList = [w for w in wordList if w in wordSet]
        # wordList = [w for w in wordList]
        ret[word] = " ".join(wordList[0:5])
    return ret

@gen.coroutine
def getSynonym(words,field):
    wordList = words.split(' ')
    wordList=[word for word in wordList if word!=""]
    ret={}

    for word in wordList:
        ret[word]=yield query_synonym(getChinese(word))

    if field.lower() == 'comname':
        ret = filterWordSet(ret,companyNameWordSet)
    if field.lower() == 'mainproduct':
        ret = filterWordSet(ret,productWordSet)
    if field.lower() == 'position':
        ret = filterWordSet(ret,majorWordSet)

    # if field.lower() == 'comname':
    #     ret = getSynonymFromDict(wordList,synonymComNameDict)
    # if field.lower() == 'mainproduct':
    #     ret = getSynonymFromDict(wordList,synonymProductBusinessDict)
    # if field.lower() == 'position':
    #     ret = getSynonymFromDict(wordList,synonymMajorDict)
    
    return ret