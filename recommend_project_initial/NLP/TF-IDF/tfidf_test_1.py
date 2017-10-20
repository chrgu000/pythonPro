#!user/bin/env python3
# -*- coding: utf-8 -*


# 提取公司简介中的关键词
import pymysql
import os
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='my.log',
                filemode='w')
def text_vec_to_sql():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    path_dir = os.listdir("../vector")
    for file in path_dir:
        f = open("../vector/" + file, encoding='utf-8', errors='ignore')
        print(file)
        logging.info(file)
        line_list = f.readlines()
        start=0
        end=200
        while(True):
            for k in range(start,end):
                companyid=line_list[k].split(":")[0]
                c_vector = line_list[k].split(":")[1]
                list_id=get_clueid(companyid)
                if len(list_id)>0:
                    for j in range(0,len(list_id)):
                        update_test = "UPDATE clue_feature SET c_tfidf_vec=" + "\""+c_vector +"\""+ " where Clue_Id=" + "\"" + list_id[j] + "\""
                        try:
                            cur_test.execute(update_test)
                        except Exception as e:
                            print(e)
            conn_test.commit()
            start=end
            end+=200
            # print(str(start)+","+str(end))
            if start<len(line_list) and end > len(line_list): end=len(line_list)
            if start>=len(line_list):break

    cur_test.close()
    conn_test.close()

def get_clueid(companyid):
    clue_list=[]
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur = conn_only.cursor()
    sql_4 = "SELECT CLue_Id FROM crm_t_clue WHERE commercialDB_id='" + companyid + "';"
    cur.execute(sql_4)
    for row in cur.fetchall():
        clue_list.append(row[0])
    cur.close()
    conn_only.close()
    return clue_list

if __name__ == '__main__':
    text_vec_to_sql()
    pass


