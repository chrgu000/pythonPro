# -*- coding: utf-8 -*
'''
更新company_connection_building.c_capital_detail字段，统一注册资金单位
'''
import pymysql
def capital_unified():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    cur_test.execute("select c_id,c_capital_detail from company_connection_building WHERE LENGTH(c_capital_detail)=3")
    print("******************")
    for row in cur_test.fetchall():
        cid=row[0]
        capital=str(row[1])
        print(str(cid)+":"+str(capital))
        # cur_test.execute("update company_connection_building set c_capital_detail="+"\""+""+"\""+"where c_id="+"\""+str(cid)+"\"")
        # cur_test.execute("update company_connection_building set c_capital_detail=" + "\"" + str(capital.split(" ")[0].replace("万人民币",""))+" 万元" + "\""+"where c_id="+"\""+str(cid)+"\"")
        cur_test.execute("update company_connection_building set c_capital_detail="+"\""+capital.replace(" ","")+" 万元"+"\""+"where c_id="+"\""+str(cid)+"\"")
        # cur_test.execute("update company_connection_building set c_capital_detail="+"\""+str(float(capital.split(" ")[0].replace("万美元",""))*6)+" 万元"+"\""+"where c_id="+"\""+str(cid)+"\"")
        conn_test.commit()

    cur_test.close()
    conn_test.close()


if __name__ == "__main__":
    capital_unified()
    pass