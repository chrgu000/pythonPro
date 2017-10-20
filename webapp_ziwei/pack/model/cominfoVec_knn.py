#! -*- coding:utf-8 -*-

import os
import logging
import pandas as pd
import numpy as np
import json
from sklearn.neighbors import NearestNeighbors

from ..util.NLP_tool import *
from ..util.sql_interface import getCompanysFromBearCustomer
from ..util.es_interface import getPortalUserByIDES
from webapp_ziwei import loadRes
from ..__init__ import logger

word_idf_dict=loadRes(os.path.join('lib','word_idf_dict'))
word2vec_model=loadRes(os.path.join('lib','word2vecModel'))
def normalize(vec):
    norm=np.linalg.norm(vec)
    return vec/(norm+0.000001)

def calc_distance(vec1,vec2):
    vec1=normalize(vec1)
    vec2=normalize(vec2)
    return np.linalg.norm(vec1 - vec2)

def analyze_cominfo(cominfoList):
    cominfoSSSList = passage2SSS_1(cominfoList)
    for item in cominfoSSSList:
        arr_s=np.zeros((100,))
        wordList=item.split(' ')
        for i in range(len(wordList)):
            word=wordList[i]
            if word in word_idf_dict:
                idf=word_idf_dict[word]
                if idf<5:continue
                try:
                    arr_w = word2vec_model[word]
                    arr_s=arr_s+arr_w*float(idf)
                except Exception as e:
                    # logger.info("%s not exist in word2vec_model"%word)
                    pass
        yield normalize(arr_s)

def getRecommendClueList(all_cid_source,userID,maxCompanyNum=100):
    try:
        portalUser = getPortalUserByIDES(userID)
        companyCode = portalUser["User_Company_Id"]
        
    except Exception as e:
        raise e
    df = getCompanysFromBearCustomer(companyCode,["info"])

    cominfoList = df['info'][:maxCompanyNum]
    cominfoList = cominfoList.dropna()
    if cominfoList.shape[0]==0:
        return [],0
    infoVectors = analyze_cominfo(cominfoList)

    cellList_called=[]

    ###############
    # cominfo
    ## candidate cid -> cid cominfo vector
    cid_vec_dict={}
    for cid,source in list(all_cid_source.items()):
        if "cominfo_vector" in source and source["cominfo_vector"] not in ["",None]:
            cid_vec_dict[cid]=source["cominfo_vector"]

    #####
    ret=cid_vec_dict
    cid_cand_list=[];arr_cand_list=[]
    #### filter
    for cid,r in list(ret.items())[:]:
        try:
            vec=eval(r) #str->list
            cid_cand_list.append(cid)
            arr_cand_list.append(vec)
        except:pass

    X=np.array(arr_cand_list)
    candidate_arr=X[:,:]

    ## adjust num_required by candidate num
    num_tt_candidate=X.shape[0]
    
    ## train
    nbrs=NearestNeighbors(num_tt_candidate,algorithm='ball_tree').fit(X)

    cidList=set()
    cleanNumTotal=0

    for query_arr in infoVectors:
        if np.sum(query_arr)==0:continue
        ###### predict
        distances,indices=nbrs.kneighbors(query_arr.reshape(1, -1))  #sorted by distance
        Idx=np.squeeze(indices);
        for ind in Idx:
            cid=cid_cand_list[ind]
            cidList.add(cid)

    return list(cidList)

