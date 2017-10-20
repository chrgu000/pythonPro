# -*- coding: utf-8 -*
'''
对新插入的数据处理
'''
import pymysql
from process_ import fields_process

def get_fields_infos(company_name):
    state="0"
    conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                              port=3306,
                              user='yunkedata',
                              passwd='XingDongJia@2016',
                              db='dataprocess',
                              charset='utf8'
                              )
    cur_gs = conn_gs.cursor()
    cur_gs.execute("select id,capital,registrationdate,hangye from company_yunke where title="+"\""+company_name+"\"")
    cid="-1"
    capital = "None"
    rdate= "None"
    hangye = "None"
    for r in cur_gs.fetchall():
        cid=str(r[0])
        capital = str(r[1])
        rdate = str(r[2])
        hangye = str(r[3])
    stat=capital+"%"+rdate+"%"+hangye
    fields=fields_process(stat)
    capital_clean = fields.split("%")[0]
    rdate_clean =fields.split("%")[1]
    hangye_clean = fields.split("%")[2]
    score=get_tyc_score(cid)
    if cid!="-1":state="1"
    cur_gs.close()
    conn_gs.close()
    return state+"%"+cid+"%"+capital_clean+"%"+rdate_clean+"%"+hangye_clean+"%"+score

# 通过工商id找天眼查的评分
def get_tyc_score(company_id):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    clueid = ""
    cur_only.execute("select CLue_Id from crm_t_clue where commercialDB_id=" + "\"" + str(company_id) + "\"")
    for r in cur_only.fetchall():
            clueid=r[0]
    cur_only.close()
    conn_only.close()

    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    tyc_score = ""
    sql = "select c_tyc_score from clue_feature where Clue_Id=" + "\"" + clueid + "\""
    cur_test.execute(sql)
    for row in cur_test.fetchall():
        tyc_score = str(row[0])
    if tyc_score == "-1" or tyc_score == "" or tyc_score == None:
        tyc_score = "None"
    return tyc_score

if __name__=='__main__':
    pass



