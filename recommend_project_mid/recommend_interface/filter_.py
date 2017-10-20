'''
过滤模块
 1、滤除值<0.5的数据线索
 2、滤除构建模型时使用的正样本（相当于删除了之前已打过的线索）
 3、已下载线索过滤
 4、不感兴趣线索过滤
 5、空号 错号过滤(未添加)
'''

import pymysql

threshold = 0.7 #删除模型预测结果小于该阈值的线索
def filter_recommend_result(result_list, company_code):
    filter_result = []
    clueid_pos = get_pos_trainset(company_code)
    not_interestid = get_not_interest_clue(company_code)
    for element in result_list:
        if float(element.split(":")[1]) > threshold:
            if element.split(":")[0] not in clueid_pos.keys() and element.split(":")[0] not in not_interestid.keys():
                filter_result.append(element)
    return filter_result

def get_pos_trainset(company_code):
    conn_test = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    sql = "select clue_id from call_record where company_code=" + "\"" + company_code + "\""
    clue_info = {}
    cur_test.execute(sql)
    for row in cur_test.fetchall():
        c_id = row[0]
        if c_id not in clue_info:
            clue_info[c_id] = 1
    return clue_info

'''
用户不感兴趣的线索id
'''
def get_not_interest_clue(company_code):
    not_interest_clue = {}
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    cur_only.execute("SELECT User_Id, User_Company_Id FROM crm_t_portaluser WHERE User_Company_Id="+"\""+company_code+"\"" )
    for row in cur_only.fetchall():
        cur_only.execute("select clue_id from crm_t_usernotinterested_clue where User_Id="+"\""+row[0]+"\"")
        for r in cur_only.fetchall():
            if r[0] not in not_interest_clue:
                not_interest_clue[r[0]] = 1
    conn_only.close()
    cur_only.close()
    return not_interest_clue

if __name__=='__main__':
    pass

