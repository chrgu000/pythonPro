# -*- coding: utf-8 -*

import pymysql

def updata():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    file = open("simi.csv", 'r')
    data=file.readlines()

    for i in range(0,len(data)):
        print(i)
        clueid=data[i].replace(",","").replace("\n","")
        print(clueid)
        update_test="UPDATE clue_feature SET clue_feature.`employees_num_mean`=1000"+" where Clue_Id="+"\""+clueid+"\""
        print(update_test)
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()
if __name__=='__main__':
    updata()
    pass