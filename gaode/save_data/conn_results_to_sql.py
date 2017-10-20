# -*- coding: utf-8 -*
import pickle
import pymysql

def get_all_buildings():
    file = open("buildings_list.csv", encoding='utf8', errors='ignore')
    building_1 = file.readlines()
    file = open("match_result.csv", encoding='utf8', errors='ignore')
    building_2 = file.readlines()
    file = open("match_result_1.csv", encoding='utf8', errors='ignore')
    building_3 = file.readlines()

    building_dict={}

    for b in building_1:
        b=b.replace("\n","")
        if b in building_dict:
            building_dict[b]+=1
        else:
            building_dict[b]=1

    for b in building_2:
        bu=b.split(";")[2]
        if bu in building_dict:
            building_dict[bu]+=1
        else:
            building_dict[bu]=1

    for b in building_3:
        bu=b.split(";")[2]
        if bu in building_dict:
            building_dict[bu]+=1
        else:
            building_dict[bu]=1

    idf_dic = open("building_dic.pkl", 'wb')
    pickle.dump(building_dict, idf_dic)
    print(len(building_dict))

def build_buildings():
    file = open("building_list.csv", encoding='utf8', errors='ignore')
    buildings = file.readlines()
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    for i in range(10,len(buildings)):
        b=buildings[i].replace("\n","")
        update_test = "insert into buildings_info (b_id,b_building_name) values ("+str((i+1))+","+"\""+b+"\""+")"
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()


if __name__=='__main__':

    pass