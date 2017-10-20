import pymysql

# 测试库 alg
def conn_test_alg(sql):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='alg',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    cur_test.execute(sql)
    list_row = []
    for row in cur_test.fetchall():
        list_row.append(row)
    cur_test.close()
    conn_test.close()
    return list_row

# 测试库 yunketest
def conn_test_yunketest(sql):
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    cur_test.execute(sql)
    list_row = []
    for row in cur_test.fetchall():
        list_row.append(row)
    cur_test.close()
    conn_test.close()
    return list_row

# 测试库--工商库
def conn_test_dataprocess(sql):
    conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                              port=3306,
                              user='yunkedata',
                              passwd='XingDongJia@2016',
                              db='dataprocess',
                              charset='utf8'
                              )
    cur_gs = conn_gs.cursor()
    cur_gs.execute(sql)
    list_row = []
    for row in cur_gs.fetchall():
        list_row.append(row)
    cur_gs.close()
    conn_gs.close()
    return list_row


# 只读库
def conn_only_dataprocess(sql):
    conn_gs = pymysql.connect(host='rds0710650me01y6d3og.mysql.rds.aliyuncs.com',
                              port=3306,
                              user='yunkedata',
                              passwd='XingDongJia@2016',
                              db='dataprocess',
                              charset='utf8'
                              )
    cur_gs = conn_gs.cursor()
    cur_gs.execute(sql)
    list_row = []
    for row in cur_gs.fetchall():
        list_row.append(row)
    cur_gs.close()
    conn_gs.close()
    return list_row

def conn_only_xddb(sql):
    conn_only = pymysql.connect(host='rr-2zeg40364h2thw9m6.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunker2016EP',
                                db='xddb',
                                charset='utf8'
                                )
    cur_only = conn_only.cursor()
    cur_only.execute(sql)
    list_row = []
    for row in cur_only.fetchall():
        list_row.append(row)
    cur_only.close()
    conn_only.close()
    return list_row


#正式库
def conn_formal_xddb(sql):
    conn_formal = pymysql.connect(host='rds5943721vp4so4j16r.mysql.rds.aliyuncs.com',
                                  port=3306,
                                  user='yunker',
                                  passwd='yunker2016EP',
                                  db='xddb',
                                  charset='utf8'
                                  )
    cur_formal = conn_formal.cursor()
    cur_formal.execute(sql)
    list_row = []
    for row in cur_formal.fetchall():
        list_row.append(row)
    cur_formal.close()
    conn_formal.close()
    return list_row
