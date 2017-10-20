# -*- coding: utf-8 -*
'''
抽象出可计算向量，存入特征表，其中原始字段：employees_num
'''

import pymysql

def clean_employees(start,banchsize):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    sql_only = "SELECT CLue_Id,employees_num FROM crm_t_clue limit "+str(start)+","+str(banchsize)+";"
    cur_only.execute(sql_only)

    data=[]
    for row in cur_only.fetchall():
        clueid = str(row[0])
        emp_num=row[1]
        #**********employees_num（员工人数）************
        #如果没有记录员工数，最大值=最小值=均值="-1"
        employees_min=employees_max=employees_mean=-1
        if str.isdigit(emp_num)==True:
            employees_min = employees_max = employees_mean = emp_num
        else:
            if str(emp_num)!='None' and str(emp_num!='null'):
                if len(emp_num.split("-"))==2:
                    employees_min = emp_num.split("-")[0]
                    employees_max =emp_num.split("-")[1].replace("人","")
                    employees_mean =(int(employees_min)+int(employees_max))/2
                if len(emp_num.split("-")) == 1:
                    if "下" in emp_num:
                        employees_min = 0
                        employees_max = str(emp_num).replace("人以下","")
                        employees_mean =(int(employees_min)+int(employees_max))/2
                    if "上" in emp_num:
                        employees_min =str(emp_num).replace("人以上", "").replace("以上","")
                        employees_max = (int(employees_min))*2
                        employees_mean = (int(employees_min) + int(employees_max)) / 2
                    if emp_num=="少于50人":
                        employees_min = 0
                        employees_max = 50
                        employees_mean = 25
                    if "人" in emp_num and "以" not in emp_num:
                        employees_min = emp_num.replace("人","")
                        employees_max = emp_num.replace("人","")
                        employees_mean = emp_num.replace("人","")
        data.append(clueid+"#"+str(employees_max)+"#"+str(employees_min)+"#"+str(employees_mean))

    cur_only.close()
    conn_only.close()
    return data


if __name__ == '__main__':

    pass
