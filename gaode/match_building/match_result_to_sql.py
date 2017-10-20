# -*- coding: utf-8 -*
'''
result_to_sql():通过地址匹配线索对应的建筑物，将匹配结果存入数据库company_connection_building
'''

import pickle
import pymysql
import uuid

def result_to_sql():
    uid_dict=get_uuid()

    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    file = open("办公楼_match_result_1.csv", encoding='utf8', errors='ignore')
    lines = file.readlines()
    for i in range(0,len(lines)):
        cid=lines[i].split(",")[0].replace("\n","")
        adr=lines[i].split(",")[1].replace("\n","")
        bname=lines[i].split(",")[2].replace("\n","")
        dis=lines[i].split(",")[3].replace("\n","")
        uid = uuid.uuid3(uuid.NAMESPACE_DNS, bname)
        u_id = str(uid).replace("-", "")
        print(u_id)
        # update_test = "update company_connection_building set b_uid=" + "\"" + u_id + "\","+"b_distance="+"\""+dis+"\"" + " where Clue_Id=" + "\"" + cid + "\""
        if u_id not in uid_dict.keys():
            insert_test = "insert into buildings_info(u_id,b_building_name) VALUES (" + "\"" + u_id + "\"," + "\"" + bname + "\"" + ")"
            print(insert_test)
            try:
                # cur_test.execute(update_test)
                cur_test.execute(insert_test)
            except Exception as e:
                print(e)
            conn_test.commit()

    cur_test.close()
    conn_test.close()



def get_building_info(start,banchsize):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    sql_test ="select b_id ,b_building_name from buildings_info limit  "+str(start)+","+str(banchsize)
    building_name={}
    cur_test.execute(sql_test)
    for row in cur_test.fetchall():
        building_name[row[1]]=row[0]
    cur_test.close()
    conn_test.close()
    return building_name

def match_result_update(start,banchsize):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    building_name = get_building_info(start,banchsize)
    for k, v in building_name.items():
        uid = uuid.uuid3(uuid.NAMESPACE_DNS,k)
        u_id = str(uid).replace("-", "")
        update_test = "update buildings_info set u_id=" + "\"" + u_id + "\"" + " where b_building_name=" + "\"" + str(k) + "\""

        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
        conn_test.commit()

    cur_test.close()
    conn_test.close()

def get_uuid():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    sql_test = "select u_id from buildings_info"
    building_uid = {}
    cur_test.execute(sql_test)
    for row in cur_test.fetchall():
        building_uid[row[0]] = 1
    cur_test.close()
    conn_test.close()
    return building_uid

def get_company_id(start,banchsize):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    sql_test = "select Clue_Id,b_id,b_building_name,b_n_id from company_connection_building limit "+str(start)+","+str(banchsize)
    company_info = []
    cur_test.execute(sql_test)
    for row in cur_test.fetchall():
        company_info.append(str(row[0])+";"+str(row[1])+";"+str(row[2])+";"+str(row[3]))
    cur_test.close()
    conn_test.close()
    return company_info

'''
新来 线索-建筑物更新逻辑
'''
def update_company_conn(start,banchsize):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    company_info=get_company_id(start,banchsize)
    count=start
    building_uid = get_uuid()
    is_insert=False
    for i in range(0,len(company_info)):
        count=count+1
        if is_insert==True:
            building_uid = get_uuid()
            is_insert=False
        cid=company_info[i].split(";")[0]
        bid=company_info[i].split(";")[1]
        bname=company_info[i].split(";")[2]
        bnid=company_info[i].split(";")[3]
        if bid!="None":
            uid=building_uid[int(bid)]
            update_test = "update company_connection_building set b_uid="+ "\""+str(uid)+"\""+ "where Clue_Id=" +"\""+cid+"\""
            try:
                cur_test.execute(update_test)
            except Exception as e:
                print(e)
        else:
            if bname!="None":
                uid = uuid.uuid3(uuid.NAMESPACE_DNS, bname)
                u_id = str(uid).replace("-", "")
                if u_id in building_uid.values():
                    update_test = "update company_connection_building set b_uid=" + "\"" + str(u_id) + "\"" + "where Clue_Id=" + "\"" + cid + "\""
                    try:
                        cur_test.execute(update_test)
                    except Exception as e:
                        print(e)
                else:
                    update_test = "update company_connection_building set b_uid=" + "\"" + str(u_id) + "\"" + "where Clue_Id=" + "\"" + cid + "\""
                    insert_test= "insert into buildings_info(b_id,u_id,b_building_name) VALUES ("+ "\""+str(14855+count)+"\","+"\""+str(u_id)+"\","+"\""+bname+"\""+")"
                    is_insert=True
                    try:
                        cur_test.execute(update_test)
                        cur_test.execute(insert_test)
                    except Exception as e:
                        print(e)
        if bid=="None" and bname=="None" and bnid!="None":
            uid = building_uid[int(bnid)]
            update_test = "update company_connection_building set b_uid=" + "\"" + str(uid) + "\"" + "where Clue_Id=" + "\"" + cid + "\""
            try:
                cur_test.execute(update_test)
            except Exception as e:
                print(e)

        conn_test.commit()
    cur_test.close()
    conn_test.close()


if __name__=='__main__':
    result_to_sql()

    # start=0
    # for i in range(0,2000):
    #     print(start)
    #     match_result_update(start,200)
    #     start+=200

    # start=0
    # for i in range(0,100):
    #     update_company_conn(start,200)
    #     start+=200
    #     print(start)

    pass