# -*- coding: utf-8 -*

import pymysql
import uuid

def get_cid():
    file = open("building_bgl.csv", encoding='utf8', errors='ignore')
    building = file.readlines()
    conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                              port=3306,
                              user='yunkedata',
                              passwd='XingDongJia@2016',
                              db='dataprocess',
                              charset='utf8'
                              )
    cur = conn_gs.cursor()
    file_save = open("bangonglou.csv", 'a')
    for i in range(0, len(building)):
        company_id=building[i].split(",")[0]
        sql = "select address from company_yunke where id=" + "\"" + str(company_id) + "\""
        cur.execute(sql)
        for r in cur.fetchall():
            address=r[0]
            uid = uuid.uuid3(uuid.NAMESPACE_DNS, "")
            file_save.write(company_id+","+str(r[0]))
            file_save.write('\n')
    cur.close()
    conn_gs.close()

if __name__=='__main__':
    get_cid()
    pass
