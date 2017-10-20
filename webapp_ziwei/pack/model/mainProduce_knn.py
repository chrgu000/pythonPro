#! -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import re
import json
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from ..util.NLP_tool import *

def remove_cominfo(rowdict):
    rowdict1={}
    for feaname,v in list(rowdict.items()):
        if 'com_info_' not in feaname:
            rowdict1[feaname]=v
    return rowdict1

def get_attribute(clueIds): #
    sql ="""
    SELECT *
    from crm_t_clue
    where CLue_Id  IN ('%s')
    #and main_produce is not null
    """
    # cur = db.cursor()
    # cur.execute(sql % "','".join(clueIds))
    # ret = {}
    # for r in cur.fetchall():
    #     ret[r['CLue_Id']] = r #{id:{record},...}
    df=pd.read_sql(sql % "','".join(clueIds),db);
    return df

def yield_row(allclue_feaDict,feaName_to_fid):
    for clueid in sorted(allclue_feaDict.keys())[:]: # cid sorted in sequence
        obs={}
        for feaname,v in list(allclue_feaDict[clueid].items()):
            obs[ feaName_to_fid[feaname] ]=v
        yield obs

def getFeaname2Fid(allclue_feaDict):
    feaName_to_fid={} #{hospital:0,...}
    for clueid in sorted(allclue_feaDict.keys())[:]: # cid sorted in sequence
        for feaname,v in list(allclue_feaDict[clueid].items()):
            if feaname not in feaName_to_fid:#new word
                feaName_to_fid[feaname]=len(feaName_to_fid)
    return feaName_to_fid

def generate_svm(allclue_feaDict):
    feaName_to_fid = getFeaname2Fid(allclue_feaDict)
    item    =yield_row(allclue_feaDict,feaName_to_fid)
    indptr = np.array([0]);
    indices = np.array([]);
    for row_dict in item:
        idXXX = np.array([])
        for fid in sorted(row_dict.keys()):
            fval = row_dict[fid]
            if fval != 0.0:
                # f.write('%d:%f ' % (fid, fval))## write into  "modeling.svm"
                idXXX = np.append(idXXX,int(fid))
        indices = np.append(indices,idXXX)
        indptr = np.append(indptr,indptr[-1]+idXXX.shape[0])
    data = np.array(np.ones(indices.shape[0]))
    X = csr_matrix((data, indices, indptr))

    return X,feaName_to_fid

def remove_cominfo_comName(rowdict):
    rowdict1={}
    for feaname,v in list(rowdict.items()):
        if 'com_info_' not in feaname and 'com_name_' not in feaname:
            rowdict1[feaname]=v
    return rowdict1

def analyze_business(businessList,prior_n = 100):
    # 根据公司经营范围获取关键词(这里提供推荐的应该是关键词还是经营范围的短语)
    # businessList经营范围列表
    # prior_n，只分析前几条语句
    business_key_dict={}
    for business in businessList:
        if isinstance(business,str):
            if business in ['',None]:continue
            # yangrui version: 去掉括号中内容，将所有符号替换成空格，去掉数字和英文字母，用标点符号分句，去掉无效的断言句，未分词，
            #　　　　　　　　　　　使用特定或词汇切分句子
            
            business = remove_brace_content(business)
            sentences = [getChinese(sentence) for sentence in splitParagraph2Sentences(business)]
            
            '''
            # ziwei version:  去掉括号中内容，用有效的标点符号分句，获取句子中的汉字，用jieba模块分词
            wordListRaw = []
            #　用jieba模块分词
            [wordListRaw.extend(wordParsingCut(sentence,False)) for sentence in sentences]
            # 去掉所有地名，以及”股份“，”有限“，”公司“等词语          
            wordList=[w for w in wordListRaw if w not in noiseList and len(w)>1]
            # 将分词结果加入字典中
            for word in wordList:
                if word not in business_key_dict:business_key_dict[word]=1
                else:business_key_dict[word]+=1
            '''
            ll=remove_allegedNotParticipate(sentences);
            if len(ll)==0:continue

            ll=[w.strip() for w in ll if len(w.strip())>1]
            ### choose first 3
            ll=ll[:prior_n] if len(ll)>=prior_n else ll
            for word in ll:
                word=strip_word(word)
                word=word.split(' ')##stri->list
                for w in word:
                    if len(w.strip())==0:continue
                    if w not in business_key_dict:business_key_dict[w]=1
                    else:business_key_dict[w]+=1
    return business_key_dict

def prepare_wholeDB_svm_clue(cid_produce):
    #######
    cid_rawdict={}
    for cid,raw_str in list(cid_produce.items())[:]:

        words_dict=analyze_business([raw_str],10)
        words=list(words_dict.keys());
        cid_rawdict[cid]=dict(list(zip(words,[1]*len(words)))) #{cid:{str_word:1,,,,}
    return generate_svm(cid_rawdict)

def prepare_result(X,feaName_to_fid,business_keywords,cid_produce):

    ## adjust num_required by candidate num
    num_tt_candidate=X.shape[0]
    sample_number = num_tt_candidate #if sample_number > num_tt_candidate else sample_number 

    query_list=business_keywords

    query_ind=[]#[feaName_to_fid[w] for w in query_list if w in feaName_to_fid];
    query_ind_far=[]
    for feaname,fid in list(feaName_to_fid.items()):
        for word in query_list:
            if word !=feaname and word in feaname:
                query_ind_far.append(fid)

            if word ==feaname:query_ind.append(fid)
    query_arr=np.zeros((X.shape[1]))
    query_ind=list(set(query_ind));
    query_ind_far=list(set(query_ind_far));
    query_arr[query_ind]=2
    query_arr[query_ind_far]=1

    #### choose x has common fid with query_arr
    nonzero_clue_ind=np.arange(X.shape[0])
    n_arr=X*query_arr
    nonzero_clue_ind=np.nonzero(n_arr)[0]
    query_arr=csr_matrix(query_arr)

    # cidlist match svm
    cidlist_match_svm=sorted(cid_produce.keys())     # when generate svm, cid is in this sequence

    #############3
    # knn  when fit knn,only use cluetable,not querylist
    ## train
    nbrs=NearestNeighbors(sample_number,algorithm='ball_tree').fit(X)

    test=0
    # distances,indices=nbrs.kneighbors(x_query[test,:])
    distances,indices=nbrs.kneighbors(query_arr)  #sorted by distance
    clueTableIdx=np.squeeze(indices);

    #candidate_clueid_list=[cidlist_match_svm[i] for i in clueTableIdx if i in nonzero_clue_ind]  # in sequence
    candidate_clueid_list=[cidlist_match_svm[i] for i in clueTableIdx]

    return candidate_clueid_list

def getRecommendClueList(business_keywords,cid_produce,all_cid_source):
    X,feaName_to_fid = prepare_wholeDB_svm_clue(cid_produce)
    cidlist=prepare_result(X,feaName_to_fid,business_keywords,cid_produce)
    return cidlist
