#! -*- coding:utf-8 -*-

import pandas as pd
import pymysql
from pymysql import cursors
import logging
from ..__init__ import logger

DEFAULT_COMPANYS_NUM = 50
MAX_COMPANYS_NUM=100
def connectFormalMySQL():
    return pymysql.connect(host='rds5943721vp4so4j16r.mysql.rds.aliyuncs.com',
                     user='yunker',
                     passwd="yunker2016EP",
                     db="xddb",
                     use_unicode=True,
                     charset='utf8',
                     cursorclass=cursors.DictCursor)

def connectTestMySQL():
    return pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                     user='yunker',
                     passwd="yunke2016",
                     db="yunketest",
                     use_unicode=True,
                     charset='utf8',
                     cursorclass=cursors.DictCursor)

from tornado import gen
import tormysql

pool = tormysql.ConnectionPool(
    max_connections = 20, #max open connections
    idle_seconds = 0, #conntion idle timeout time, 0 is not timeout
    wait_connection_timeout = 3, #wait connection timeout
    host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
    user='yunker',
    passwd="yunke2016",
    db="yunketest",
    charset = "utf8"
)


def connectMySql():
    return connectTestMySQL()

db = connectMySql()

def excuteMySql(sql):
    try:
        global db
        return pd.read_sql(sql,db)
        
    except Exception as e:
        global db
        db = connectMySql()
        return pd.read_sql(sql,db)

@gen.coroutine
def excuteTorMySql(sql):
    ret=[]
    with (yield pool.Connection()) as conn:
        with conn.cursor() as cursor:
            yield cursor.execute(sql)
            datas = cursor.fetchall()
    return datas

def getCompanysFromBearCustomer(companyCode,fields=["name","business","info"],number = DEFAULT_COMPANYS_NUM):
    '''得到导入的用于得到搜索和推荐关键词的样本
    '''
    if number>MAX_COMPANYS_NUM:number=MAX_COMPANYS_NUM
    fieldSet=["Company_Name as name","Business_Scope as business","Company_Summary as info"]
    fieldList=[]
    if "name" in fields: fieldList.append(fieldSet[0])
    if "business" in fields: fieldList.append(fieldSet[1])
    if "info" in fields: fieldList.append(fieldSet[2])
    fieldStr = ','.join(fieldList)
    if fieldStr=='':
        return pd.DataFrame()

    sql = """   SELECT %s
                FROM   crm_t_bear_customer
                WHERE  Company_ID = '%s'
                LIMIT %s;
          """%(fieldStr,companyCode,number)

    companyDF = excuteMySql(sql)
    return companyDF

def getCompanysFromPlanCustomer(companyCode,number = DEFAULT_COMPANYS_NUM):
    '''得到用户导入的用来打电话的样本
    '''
    pass

def getCompanyCodeByUserID(userID):
    sql = """   SELECT User_Company_Id
                FROM crm_t_portaluser
                WHERE User_Id = '%s'
          """%userID
    companyCodeDF=excuteMySql(sql)

    if companyCodeDF.shape[0]==0:
        logger.error("The userID doesn't matchs any companyCode")
        return ""
    if companyCodeDF.shape[0]>1:
        logger.warning("The userID matchs multiple companyCode")

    companyCode = companyCodeDF.iat[0,0]
    return companyCode
    
@gen.coroutine
def query_synonym(word,exact=True):
    sql=""" SELECT synonym
            from synonym_cominfo 
            where word like '%s'
            limit 1
        """

    if exact==False:
        sql = sql % ('%'+word+'%')
    else:
        sql = sql % word
    
    data = yield excuteTorMySql(sql)
    try:
        return data[0][0]
    except:
        return ""
