# -*- coding: utf-8 -*

'''
b_industry_distribution:行业分布
b_date_distribution:注册时间分布
b_capital_distribution 注册资本分布
'''

import pymysql

def alter_fields_dict():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select u_id from buildings_info")
    for row in cur_test.fetchall():
        print(row[0])
        industry_dict = {}
        date_dict = {}
        capital_dict = {}
        cur_test.execute("select c_industry,c_rdate,c_capital from company_connection_building where b_uid="+"\""+row[0]+"\"")
        for r in cur_test.fetchall():
            if r[0] not in industry_dict.keys():
                industry_dict[r[0]] = 1
            else:
                industry_dict[r[0]] += 1
            if r[1] not in date_dict.keys():
                date_dict[r[1]] = 1
            else:
                date_dict[r[1]] += 1
            if r[2] not in capital_dict.keys():
                capital_dict[r[2]] = 1
            else:
                capital_dict[r[2]] += 1
        industry_sort = sort_industry(industry_dict)
        date_sort = sort_date(date_dict)
        capital_sort = sort_capital(capital_dict)

        industry_str = "{"
        for i in range(0, len(industry_sort)):
            industry_str += "'"
            if i != (len(industry_sort)-1):
                industry_str += industry_sort[i][0] + "'" + ": " + str(industry_sort[i][1]) + ", "
            else:
                industry_str += industry_sort[i][0] + "'" + ": " + str(industry_sort[i][1])
        industry_str += "}"

        date_str = "{"
        for i in range(0, len(date_sort)):
            date_str += "'"
            if i != (len(date_sort) - 1):
                date_str += date_sort[i].split(":")[0] + "'" + ": " + str(date_sort[i].split(":")[1]) + ", "
            else:
                date_str += date_sort[i].split(":")[0] + "'" + ": " + str(date_sort[i].split(":")[1])
        date_str += "}"

        capital_str = "{"
        for i in range(0, len(capital_sort)):
            capital_str += "'"
            if i != (len(capital_sort) - 1):
                capital_str += capital_sort[i].split(":")[0] + "'" + ": " + str(capital_sort[i].split(":")[1]) + ", "
            else:
                capital_str += capital_sort[i].split(":")[0] + "'" + ": " + str(capital_sort[i].split(":")[1])
        capital_str += "}"

        print(str(industry_str))
        print(str(date_str))
        print(str(capital_str))
        try:
            update_sql = "update buildings_info set b_industry_distribution=" + "\"" + str(industry_str) + "\"," \
                            +"b_date_distribution=" + "\"" + str(date_str) + "\"," \
                            +"b_capital_distribution=" + "\"" + str(capital_str) + "\""+" where u_id="+ "\""+str(row[0])+"\""
            print(update_sql)
            cur_test.execute(update_sql)
            conn_test.commit()
        except Exception as e:
            print(e)

    conn_test.close()
    cur_test.close()

def conn_test_yunketest():
    conn_test = pymysql.connect(host='rds0710650me01y6d3ogo.mysql.rds.aliyuncs.com',
                                port=3306,
                                user='yunker',
                                passwd='yunke2016',
                                db='yunketest',
                                charset='utf8'
                                )
    return conn_test

def sort_industry(industry_dict):
    dict_sort = sorted(industry_dict.items(), key=lambda item: item[1], reverse=True)
    return dict_sort

def sort_date(date_dict):
    date_sort = []
    if "2016-2017" in date_dict.keys():
        date_sort.append("2016-2017"+":"+str(date_dict["2016-2017"]))
    if "2014-2015" in date_dict.keys():
        date_sort.append("2014-2015"+":"+str(date_dict["2014-2015"]))
    if "2012-2013" in date_dict.keys():
        date_sort.append("2012-2013"+":"+str(date_dict["2012-2013"]))
    if "2010-2011" in date_dict.keys():
        date_sort.append("2010-2011"+":"+str(date_dict["2010-2011"]))
    if "2008-2009" in date_dict.keys():
        date_sort.append("2008-2009"+":"+str(date_dict["2008-2009"]))
    if "2006-2007" in date_dict.keys():
        date_sort.append("2006-2007"+":"+str(date_dict["2006-2007"]))
    if "2004-2005" in date_dict.keys():
        date_sort.append("2004-2005"+":"+str(date_dict["2004-2005"]))
    if "2002-2003" in date_dict.keys():
        date_sort.append("2002-2003"+":"+str(date_dict["2002-2003"]))
    if "2000-2001" in date_dict.keys():
        date_sort.append("2000-2001"+":"+str(date_dict["2000-2001"]))
    if "1998-1999" in date_dict.keys():
        date_sort.append("1998-1999"+":"+str(date_dict["1998-1999"]))
    if "1996-1997" in date_dict.keys():
        date_sort.append("1996-1997"+":"+str(date_dict["1996-1997"]))
    if "1994-1995" in date_dict.keys():
        date_sort.append("1994-1995"+":"+str(date_dict["1994-1995"]))
    if "1992-1993" in date_dict.keys():
        date_sort.append("1992-1993"+":"+str(date_dict["1992-1993"]))
    if "1990-1991" in date_dict.keys():
        date_sort.append("1990-1991"+":"+str(date_dict["1990-1991"]))
    if "1988-1989" in date_dict.keys():
        date_sort.append("1988-1989"+":"+str(date_dict["1988-1989"]))
    if "1986-1987" in date_dict.keys():
        date_sort.append("1986-1987"+":"+str(date_dict["1986-1987"]))
    if "1984-1985" in date_dict.keys():
        date_sort.append("1984-1985"+":"+str(date_dict["1984-1985"]))
    if "1982-1983" in date_dict.keys():
        date_sort.append("1982-1983"+":"+str(date_dict["1982-1983"]))
    if "<1982" in date_dict.keys():
        date_sort.append("<1982"+":"+str(date_dict["<1982"]))
    if "保密" in date_dict.keys():
        date_sort.append("保密"+":"+str(date_dict["保密"]))

    return date_sort

def sort_capital(capital_dict):
    capital_sort = []
    if ">5000w" in capital_dict.keys():
        capital_sort.append(">5000w"+":"+str(capital_dict[">5000w"]))
    if "3000w-5000w" in capital_dict.keys():
        capital_sort.append("3000w-5000w"+":"+str(capital_dict["3000w-5000w"]))
    if "1000w-3000w" in capital_dict.keys():
        capital_sort.append("1000w-3000w"+":"+str(capital_dict["1000w-3000w"]))
    if "500w-1000w" in capital_dict.keys():
        capital_sort.append("500w-1000w"+":"+str(capital_dict["500w-1000w"]))
    if "100w-500w" in capital_dict.keys():
        capital_sort.append("100w-500w"+":"+str(capital_dict["100w-500w"]))
    if "<100w" in capital_dict.keys():
        capital_sort.append("<100w"+":"+str(capital_dict["<100w"]))
    if "保密" in capital_dict.keys():
        capital_sort.append("保密"+":"+str(capital_dict["保密"]))

    return capital_sort

if __name__ == '__main__':
    alter_fields_dict()
    pass