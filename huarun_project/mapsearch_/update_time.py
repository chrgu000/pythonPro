# -*- coding: utf-8 -*
'''
更新company_connection_building中c_rdate字段
'''
import pymysql

def clean_date():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    cur_test = conn_test.cursor()
    cur_test.execute("select c_id,c_industry,c_rdate,c_capital from company_connection_building limit 100000,1277059")

    for row in cur_test.fetchall():
        cid=row[0]
        print(cid)
        if row[1]=="None" or row[2]=="-1" or row[2]==None or row[2]=="":
            cur_test.execute("update company_connection_building set c_industry='无' where c_id="+"\""+str(cid)+"\"")

        if row[3]=="None" or row[2]=="-1" or row[2]==None or row[2]=="":
            cur_test.execute("update company_connection_building set c_capital='无' where c_id="+"\""+str(cid)+"\"")

        cdate = row[2]
        if "-" not in row[2] and "<" not in row[2]:
            if row[2] == "None" or row[2]=="-1" or row[2]==None or row[2]=="无":
                cdate = "无"
            else:
                if int(row[2]) <= 2017 and int(row[2]) >= 2016: cdate = "2016-2017"
                if int(row[2]) <= 2015 and int(row[2]) >= 2014: cdate = "2014-2015"
                if int(row[2]) <= 2013 and int(row[2]) >= 2012: cdate = "2012-2013"
                if int(row[2]) <= 2011 and int(row[2]) >= 2010: cdate = "2010-2011"
                if int(row[2]) <= 2009 and int(row[2]) >= 2008: cdate = "2008-2009"
                if int(row[2]) <= 2007 and int(row[2]) >= 2006: cdate = "2006-2007"
                if int(row[2]) <= 2005 and int(row[2]) >= 2004: cdate = "2004-2005"
                if int(row[2]) <= 2003 and int(row[2]) >= 2002: cdate = "2002-2003"
                if int(row[2]) <= 2001 and int(row[2]) >= 2000: cdate = "2000-2001"
                if int(row[2]) <= 1999 and int(row[2]) >= 1998: cdate = "1998-1999"
                if int(row[2]) <= 1997 and int(row[2]) >= 1996: cdate = "1996-1997"
                if int(row[2]) <= 1995 and int(row[2]) >= 1994: cdate = "1994-1995"
                if int(row[2]) <= 1993 and int(row[2]) >= 1992: cdate = "1992-1993"
                if int(row[2]) <= 1991 and int(row[2]) >= 1990: cdate = "1990-1991"
                if int(row[2]) <= 1989 and int(row[2]) >= 1988: cdate = "1988-1989"
                if int(row[2]) <= 1987 and int(row[2]) >= 1986: cdate = "1986-1987"
                if int(row[2]) <= 1985 and int(row[2]) >= 1984: cdate = "1984-1985"
                if int(row[2]) <= 1983 and int(row[2]) >= 1982: cdate = "1982-1983"
                if int(row[2]) < 1982 and row[2]!="-1": cdate = "<1982"
            cur_test.execute("update company_connection_building set c_rdate="+"\""+cdate+"\""+" where c_id="+"\""+str(cid)+"\"")
        conn_test.commit()
    cur_test.close()
    conn_test.close()

if __name__=='__main__':
    clean_date()
    pass