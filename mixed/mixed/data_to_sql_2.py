# -*- coding: utf-8 -*

import pymysql

#Clue_Longitude,
# Clue_Latitude,
# registed_capital_num,
# registed_capital_currency
def clue_clean(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql_only = "SELECT CLue_Id,Clue_Longitude,Clue_Latitude,Clue_entry_Major,registed_capital_num,registed_capital_currency FROM crm_t_clue limit "+str(start)+","+str(banchsize)+";"
    cur_only.execute(sql_only)

    data=[]
    for row in cur_only.fetchall():
        cid = str(row[0])

        #**********Clue_Longitude,Clue_Latitude（经纬度）********
        #如果经纬度为空，值="-1"
        clon="-1"
        clat="-1"
        if clon!="" or clon!="None" or clon!="null" and clat!="" or clat!="None" or clat!="null":
            clon = str(row[1])
            clat = str(row[2])

        #*************registed_capital_num（注册资金）,registed_capital_currency******************
        # 如果无，值="-1"
        capital = "-1"
        if str.isdigit(str(row[3]))==True :
            if str(row[4])=="人民币":
                capital= str(row[5])
            if str(row[4])=="美元":
                capital=str(int(str(row[3])) * 6.5)#(美元兑人民币汇率：6.5)

        data.append(cid+"#"+clon+"#"+clat+"#"+str(capital))
    cur_only.close()
    conn_only.close()
    return data

def updata(data):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )

    cur_test = conn_test.cursor()
    for i in range(0,len(data)):
        clueid=data[i].split("#")[0]
        lon=data[i].split("#")[1]
        lat=data[i].split("#")[2]
        capital=data[i].split("#")[3]

        update_test="UPDATE clue_feature SET location_lat="+lat+","+"locati_lon="+lon+","+"registed_capital="+capital+" where Clue_Id="+"\""+clueid+"\""
        try:
            cur_test.execute(update_test)
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.commit()
    conn_test.close()

if __name__ == '__main__':
    start=0
    banchsize=1000000
    while(True):
        data = clue_clean(start,banchsize)
        if len(data)==0:break
        updata(data)
        start+=banchsize
        print("第"+str(start)+"完成")
    pass
