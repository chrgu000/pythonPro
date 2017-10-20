# -*- coding: utf-8 -*
'''
company_connection_building表c_id(工商id)修改成mongodb中的ObjectId
依据公司名称匹配
'''

import pymysql
from pymongo import MongoClient

client = MongoClient("10.31.149.111", 27017)
db = client.TYCHtml
db.authenticate("tychtml", "2zeg4uei0364h21thw9m6")
collections = db.companys

def change_cid_to_mongoid():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    sql = "select c_id,c_company_name from company_connection_building"
    cur_test.execute(sql)
    for row in cur_test.fetchall():
        cid = row[0]
        company_name = row[1]
        result = collections.find({"companyPortray.comName": company_name}, {"_id": 1})
        mongoid=""
        for i in result:
            mongoid = str(i.values()).split("(")[2].replace("\'", "").replace(")", "").replace("]", "")
        if mongoid != "":
            print(str(cid)+":"+company_name+":"+mongoid)
            cur_test.execute("update company_connection_building set c_id="+"\""+str(mongoid)+"\"" +" where c_id="+"\""+ str(cid)+"\"")
            conn_test.commit()

    cur_test.close()
    conn_test.close()

if __name__ == '__main__':
    change_cid_to_mongoid()
    pass