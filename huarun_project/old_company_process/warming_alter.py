# -*- coding: utf-8 -*

import pymysql
from collections import Counter

'''
将xx大厦的信息填充到xx大厦A座字段信息,如果xx大厦A座有信息，则不覆盖
'''
def update_building_1():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    file = open("uic_name_count.csv", encoding='utf8', errors='ignore')
    lines = file.readlines()
    all_name = {}
    for i in range(0, len(lines)):
        bname = lines[i].split("%")[2].replace("\n", "")
        if bname not in all_name:
            all_name[bname] = 1
        else:
            all_name[bname] += 1

    for i in range(8123, len(lines)):
        name_list = []
        bname = lines[i].split("%")[2].replace("\n", "")
        for key, value in all_name.items():
            if bname in key: name_list.append(key)
        price_range=""
        building_floor=""
        property_name=""
        property_tel=""
        room_rate=""
        hangqing=""
        develper=""
        evevator_num=""
        standard_height=""
        building_area=""
        introduce=""

        select_sql = "select b_price_range,b_building_floor,b_property_name,b_property_tel,b_room_rate,b_hangqing,b_building_developer,b_elevator_num,b_standard_height,b_building_area,b_building_introduce from buildings_info where b_building_name=" + "\"" + bname+ "\""
        cur_test.execute(select_sql)
        for r in cur_test.fetchall():
            if r[0] != None:price_range = r[0]
            if r[1] != None:building_floor = str(r[1]).replace("[","").replace("]","").replace("\'","")
            if r[2] != None:property_name = str(r[2]).replace("[","").replace("]","").replace("\'","")
            if r[3]!=None:property_tel = r[3]
            if r[4] != None:room_rate = str(r[4]).replace("[","").replace("]","").replace("\'","")
            if r[5] != None:hangqing = r[5]
            if r[6] != None:develper = str(r[6]).replace("[","").replace("]","").replace("\'","")
            if r[7] != None:evevator_num = str(r[7]).replace("[","").replace("]","").replace("\'","")
            if r[8] != None:standard_height = str(r[8]).replace("[","").replace("]","").replace("\'","")
            if r[9] != None:building_area = str(r[9]).replace("[","").replace("]","").replace("\'","")
            if r[10] != None:introduce = str(r[10]).replace("\"","")

        if len(name_list) <= 5 and len(name_list) >= 2:
            print(bname)
            for j in range(0,len(name_list)):
                if name_list[j]==bname:
                    update_1 = "update buildings_info set b_price_range=" + "\"" + price_range + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_1)
                    update_2 = "update buildings_info set b_building_floor=" + "\"" + building_floor + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_2)
                    update_3 = "update buildings_info set b_property_name=" + "\"" + property_name + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_3)
                    update_4 = "update buildings_info set b_property_tel=" + "\"" + property_tel + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_4)
                    update_5 = "update buildings_info set b_room_rate=" + "\"" + room_rate + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_5)
                    update_6 = "update buildings_info set b_hangqing=" + "\"" + hangqing + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_6)
                    update_7 = "update buildings_info set b_building_developer=" + "\"" + develper + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_7)
                    update_8 = "update buildings_info set b_elevator_num=" + "\"" + evevator_num + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_8)
                    update_9 = "update buildings_info set b_standard_height=" + "\"" + standard_height + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_9)
                    update_10 = "update buildings_info set b_building_area=" + "\"" + building_area + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_10)
                    update_11 = "update buildings_info set b_building_introduce=" + "\"" + introduce + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                    cur_test.execute(update_11)
                    conn_test.commit()
                else:
                    sql="select b_price_range,b_property_name,b_property_name,b_property_tel,b_room_rate,b_hangqing,b_building_developer,b_elevator_num,b_standard_height,b_building_area,b_building_introduce from buildings_info where b_building_name=" +"\""+name_list[j]+"\""
                    cur_test.execute(sql)
                    for r in cur_test.fetchall():
                        if r[0]==None or len(r[0])<1:
                            update_1="update buildings_info set b_price_range="+"\""+price_range+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_1)
                        if  r[1]==None or len(r[1])<1:
                            update_2="update buildings_info set b_building_floor="+"\""+building_floor+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_2)
                        if r[2] == None or len(r[2]) < 1:
                            update_3 = "update buildings_info set b_property_name=" + "\"" + property_name + "\"" + " where b_building_name=" + "\"" + name_list[j] + "\""
                            cur_test.execute(update_3)
                        if r[3] == None or len(r[3]) < 1:
                            update_4="update buildings_info set b_property_tel="+"\""+property_tel+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_4)
                        if r[4] == None or len(r[4]) < 1:
                            update_5="update buildings_info set b_room_rate="+"\""+room_rate+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_5)
                        if r[5] == None or len(r[5]) < 1:
                            update_6="update buildings_info set b_hangqing="+"\""+hangqing+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_6)
                        if r[6] == None or len(r[6]) < 1:
                            update_7="update buildings_info set b_building_developer="+"\""+develper+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_7)
                        if r[7] == None or len(r[7]) < 1:
                            update_8="update buildings_info set b_elevator_num="+"\""+evevator_num+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_8)
                        if r[8] == None or len(r[8]) < 1:
                            update_9="update buildings_info set b_standard_height="+"\""+standard_height+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_9)
                        if r[9] == None or len(r[9]) < 1:
                            update_10="update buildings_info set b_building_area="+"\""+building_area+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_10)
                        if r[10] == None or len(r[10]) < 1:
                            update_11="update buildings_info set b_building_introduce="+"\""+introduce+"\"" +" where b_building_name=" +"\""+name_list[j]+"\""
                            cur_test.execute(update_11)
                    conn_test.commit()
    cur_test.close()
    conn_test.close()

'''
xx大厦统计信息修正，需要包含xx大厦A座、B座等统计信息和
'''
def update_building():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    file = open("uic_name_count.csv", encoding='utf8', errors='ignore')
    lines = file.readlines()
    all_name={}
    for i in range(0,len(lines)):
        bname=lines[i].split("%")[2].replace("\n","")
        if bname not in all_name:
            all_name[bname]=1
        else :
            all_name[bname]+=1

    for i in range(50,len(lines)):
        name_list=[]
        bname = lines[i].split("%")[2].replace("\n","")
        for key ,value in all_name.items():
            if bname in key:name_list.append(key)
        if len(name_list)<=5 and len(name_list)>=2:
            print(bname)
            all_enterprise_stat=0
            all_trademark_stat=0
            all_patent_stat=0
            all_copyright_stat=0
            all_recruit_stat=0
            no_trademark_stat=0
            no_patent_stat=0
            no_copyrightr_stat=0
            has_trademark_stat=0
            has_patent_stat=0
            has_copyright_stat=0

            industry_distribution={}
            date_distribution={}
            capital_distribution={}

            for j in range(0,len(name_list)):
                select_sql="select b_all_enterprise_stat,b_all_trademark_stat,b_all_patent_stat,b_all_copyright_stat,b_all_recruit_stat,b_no_trademark_stat,b_no_patent_stat,b_no_copyright_stat,b_has_trademark_stat,b_has_patent_stat,b_has_copyright_stat,b_industry_distribution,b_date_distribution,b_capital_distribution from buildings_info where b_building_name="+"\""+name_list[j]+"\""
                cur_test.execute(select_sql)
                for r in cur_test.fetchall():
                    all_enterprise_stat += int(r[0])
                    all_trademark_stat+=int(r[1])
                    all_patent_stat+=int(r[2])
                    all_copyright_stat+= int(r[3])
                    all_recruit_stat+=int(r[4])
                    no_trademark_stat+=int(r[5])
                    no_patent_stat +=int(r[6])
                    no_copyrightr_stat +=int(r[7])
                    has_trademark_stat += int(r[8])
                    has_patent_stat +=int(r[9])
                    has_copyright_stat +=int(r[10])

                    industry_distribution= dict(Counter(industry_distribution)+Counter(eval(r[11])))
                    date_distribution = dict(Counter(date_distribution)+Counter(eval(r[12])))
                    capital_distribution = dict(Counter(capital_distribution)+Counter(eval(r[13])))

            print(bname+":"+str(all_enterprise_stat))
            print(industry_distribution)
            print(date_distribution)
            print(capital_distribution)

            update_sql_1="update buildings_info set b_all_enterprise_stat="+"\""+str(all_enterprise_stat)+"\""+"where b_building_name="+"\""+bname+"\""
            cur_test.execute(update_sql_1)

            update_sql_2 = "update buildings_info set b_all_trademark_stat=" + "\"" + str(all_trademark_stat) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_2)

            update_sql_3 = "update buildings_info set b_all_patent_stat=" + "\"" + str(all_patent_stat) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_3)

            update_sql_4 = "update buildings_info set b_all_copyright_stat=" + "\"" + str(all_copyright_stat) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_4)

            update_sql_5 = "update buildings_info set b_all_recruit_stat=" + "\"" + str(all_recruit_stat) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_5)

            update_sql_6 = "update buildings_info set b_no_trademark_stat=" + "\"" + str(no_trademark_stat) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_6)

            update_sql_7 = "update buildings_info set b_no_patent_stat=" + "\"" + str(no_patent_stat) + "\"" + "where b_building_name=" + "\"" + bname+ "\""
            cur_test.execute(update_sql_7)

            update_sql_8 = "update buildings_info set b_no_copyright_stat=" + "\"" + str(no_copyrightr_stat) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_8)

            update_sql_9 = "update buildings_info set b_has_trademark_stat=" + "\"" + str(has_trademark_stat) + "\"" + "where b_building_name=" + "\"" + bname+ "\""
            cur_test.execute(update_sql_9)

            update_sql_10 = "update buildings_info set b_has_patent_stat=" + "\"" + str(has_patent_stat) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_10)

            update_sql_11 = "update buildings_info set b_has_copyright_stat=" + "\"" + str(has_copyright_stat) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_11)

            update_sql_12 = "update buildings_info set b_industry_distribution=" + "\"" + str(industry_distribution) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_12)

            update_sql_13 = "update buildings_info set b_date_distribution=" + "\"" + str(date_distribution) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_13)

            update_sql_14 = "update buildings_info set b_capital_distribution=" + "\"" + str(capital_distribution) + "\"" + "where b_building_name=" + "\"" + bname + "\""
            cur_test.execute(update_sql_14)
            conn_test.commit()

    cur_test.close()
    conn_test.close()

#对字段清洗无关字符
def update_conn():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()

    sql_test = "select u_id,b_room_rate from buildings_info"
    cur_test.execute(sql_test)
    all_list=[]
    for r in cur_test.fetchall():
        if r[1]!=None:
            all_list.append(r[0]+"%"+r[1])

    for i in range(0,len(all_list)):
        property_name=all_list[i].split("%")[1]
        u_id=all_list[i].split("%")[0]
        if "[" in property_name or "\'" in property_name:
            property_name_clean=str(property_name).replace("[","").replace("]","").replace("\'","").replace(" ","")
            update="update buildings_info set b_room_rate="+"\""+property_name_clean+"\"" +" where u_id="+"\""+u_id+"\""
            print(update)
            cur_test.execute(update)
            conn_test.commit()
    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    update_building()
    # update_building_1()
    pass