#! -*- coding:utf-8 -*-

'''推荐系统API模块

提供的API包括
    getSynonym          获取近义词
    getKeywordsByID     获取关键词
    getRecommend        获取推荐线索
'''

import json
import logging
import math
import os.path
import re
import sys

import pandas as pd
import tornado.concurrent
import tornado.ioloop
import tornado.options
import yaml
from tornado import gen, web
from tornado.options import define, options

from pack.model.get_client_feaStr import (getRecommend, getSynonym,
                                          prepareKeywords)
from pack.util.es_interface import query_clueDB_aggregation
from pack.util.NLP_tool import getChinese, getNumber, removeSpace



define("port", default=9300, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    '''Handler的基类

    Extends:
        tornado.web.RequestHandler
    '''

    def set_default_headers(self):
        '''设置响应头
        '''
        # 所有域可以获取数据
        self.set_header('Access-Control-Allow-Origin','*')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST,GET,PUT,DELETE,OPTIONS')
    def get(self):
        self.write("hello world")

    def requestEnd(self,data,retCode=0,infoStr = "成功"):
        ret={"retCode":retCode,"infoStr":infoStr,"data":data}
        self.write(json.dumps(ret,ensure_ascii=False))

class IndexHandler(BaseHandler):
    def get(self):
        self.write('该服务仅提供API，暂无可视化界面') # upload csv+ fill filter added_keywords

class SynonymHandler(BaseHandler):
    '''getSynonym的Handler
    '''
    @gen.coroutine
    def post(self):
        try:
            words = self.get_argument("words",default="")
            field = self.get_argument("field",default="comname")
            ret = yield getSynonym(words,field)
            self.requestEnd(ret)
        except Exception as e:
            infoStr = "获取近义词发生异常: "+str(type(e))+": "+str(e)
            logger.error(infoStr)
            self.requestEnd({},retCode = 1, infoStr = infoStr)

class KeywordsHandler(BaseHandler):
    '''getKeywordsByID的Handler
    '''
    @gen.coroutine
    def post(self):
        '''获取关键词
        '''
        try:
            userId = self.get_argument('ID',default = "")
            keywords=yield prepareKeywords(userId)
            self.requestEnd(keywords)

        except Exception as e:
            infoStr = "获取关键词发生异常: "+str(type(e))+": "+str(e)
            logger.error(infoStr)
            self.requestEnd({},retCode = 1, infoStr = infoStr)

class RecommendHandler(BaseHandler):
    '''getRecommend的Handler
    '''
    def parseInput(self):
        '''处理输入参数
        '''
        infoStr = ''
        clueNum = int(removeSpace(getNumber(self.get_argument('clueNum',default='100'))))
        clueNum = 8000 if clueNum > 8000 else clueNum
        
        searchFilter={}
        searchFilter["ID"]                  = self.get_argument('ID',default='')
        searchFilter["recoMode"]            = removeSpace(self.get_argument("recoMode", default='justSearch')).lower()
        searchFilter["province"]            = removeSpace(getChinese(self.get_argument('province', default='')))
        searchFilter["city"]                = removeSpace(getChinese(self.get_argument('city', default='')))
        searchFilter["comname"]             = removeSpace(getChinese(self.get_argument('comname', default='')))
        searchFilter["comname_mustnot"]     = list(set(getChinese(self.get_argument('comname_mustnot', default='')).split()))
        searchFilter["position"]            = removeSpace(getChinese(self.get_argument('position', default='')))
        searchFilter["employeeNum"]         = removeSpace(getNumber(self.get_argument('employeeNum', default='')))
        searchFilter["geo"]                 = getNumber(self.get_argument('geo', default='')).strip()
        searchFilter["registrationYear"]    = removeSpace(getNumber(self.get_argument('registrationYear', default='')))
        searchFilter["companyCode"]         = self.get_argument('companyCode', default='')
        searchFilter["comname_list"]        = list(set(getChinese(self.get_argument('comname_list', default='')).split()))
        searchFilter["business_list"]       = list(set(getChinese(self.get_argument('business_list', default='')).split()))
        searchFilter["cominfoRequired"]     = False
        
        if searchFilter["geo"] != '':
            geoMatch = re.match(r'([\-\+]?[\d\.]+)\s+([\-\+]?[\d\.]+)\s+([\-\+]?[\d\.]+)\s+([\-\+]?[\d\.]+)',searchFilter["geo"])
            if geoMatch:
                if  math.fabs(float(geoMatch.group(1)))<=90 and\
                    math.fabs(float(geoMatch.group(3)))<=90 and\
                    math.fabs(float(geoMatch.group(2)))<=180 and\
                    math.fabs(float(geoMatch.group(4)))<=180 :
                    searchFilter["geo"] = searchFilter["geo"].split()
                else:
                    searchFilter["geo"]=""
                    infoStr+="经纬度范围错误，已忽略。\n"
            else:
                searchFilter["geo"]=""
                infoStr+="经纬度格式错误，已忽略。\n"

        return searchFilter,clueNum,infoStr

    @gen.coroutine
    def post(self):
        '''根据给定的推荐方法获取推荐线索
        '''
        # cookie = self.get_cookie("_xsrf")
        try:
            searchFilter,clueNum,infoStr = self.parseInput()
            logger.info("SearchFilter:\n%s",json.dumps(searchFilter,indent=2,ensure_ascii=False))

            # 若获取推荐时business_list为空，则通过分析关键词得到
            try:
                if len(searchFilter["business_list"]) == 0 and searchFilter["recoMode"] != "justsearch":
                    keywords = yield prepareKeywords(searchFilter["ID"])
                    searchFilter["business_list"] = keywords["business"]["keywords"][:10]
            except Exception as e:
                infoStr = "参数中'主营产品'关键词为空，获取关键词发生异常: "+str(type(e))+": "+str(e)
                logger.error(infoStr)
                self.requestEnd({},retCode = 1, infoStr = infoStr)
                return

            key_count_comname=[]
            key_count_business=[]
            key_count_comname   = yield query_clueDB_aggregation(searchFilter,'Clue_Entry_Com_Name')
            key_count_business  = yield query_clueDB_aggregation(searchFilter,'main_produce')

            clueList,cleanRate=[],0
            clueList, cleanRate = yield getRecommend(searchFilter, clueNum)
            ret={"recommendClue":clueList,"cleanRate":cleanRate}#,"name":key_count_comname,"business":key_count_business}
            self.requestEnd(ret)

        except Exception as e:
            logger.error(e)
            infoStr = "获取推荐时发生异常: "+str(type(e))+": "+str(e)
            self.requestEnd({},retCode=1,infoStr = infoStr)

def make_app():
    '''创建web application
    '''
    settings = {
        "debug":True,
        "xsrf_cookies":False
    }
    return tornado.web.Application([
        (r'/index', IndexHandler),
        (r"/getSynonym",SynonymHandler),
        (r"/getKeywordsByID", KeywordsHandler),
        (r"/getRecommend", RecommendHandler)],
        **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    logging.config.dictConfig(yaml.load(open('logConfig.yaml', 'r')))
    logger = logging.getLogger("tornado.application")
    logger.info("Tornado started.")
    tornado.ioloop.IOLoop.current().start()
