# -*- coding: utf-8 -*
'''
添加公司所处的地理层级
'''
import urllib.request as req
import urllib.parse as parse
import json
import pymysql

def get_loc():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select u_id,b_lat,b_lon from buildings_info")
    count = 0
    for r in cur_test.fetchall():
        print(count)
        uid = r[0]
        lat = r[1]
        lon = r[2]
        url = "http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location="+lat+","+lon+"&output=json&pois=1&ak=nPPBW9xruVM07MG5B3QLqjpwoPCLtP6E"
        # url = "http://api.map.baidu.com/geocoder/v2/?address="+parse.quote(aname)+"&output=json&ak=nPPBW9xruVM07MG5B3QLqjpwoPCLtP6E&callback=showLocation"
        json_geo = get_builds(url)
        if "无相关结果" not in json_geo:
            json_dict = eval(json_geo)
            one = json_dict["result"]["addressComponent"]["district"]
            two = json_dict["result"]["addressComponent"]["street"]
            try:
                cur_test.execute("update buildings_info set adr_scale_one="+"\""+one+"\"" +","+"adr_scale_two="+"\""+two+"\"" +" where u_id="+"\""+uid+"\"")
                print("update buildings_info set adr_scale_one="+"\""+one+"\"" +","+"adr_scale_two="+"\""+two+"\"" +" where u_id="+"\""+uid+"\"")
                conn_test.commit()
            except Exception as e:
                print(e)
        count += 1
            # lng = str(json_dict["result"]["location"]["lng"])
            # lat = str(json_dict["result"]["location"]["lat"])
            #
            # try:
            #     cur_test.execute("insert into map_scale(loc_name,lat,lng) VALUES ("+"\""+aname+"\""+","+"\""+lat+"\""+","+"\""+lng+"\""+")")
            # except Exception as e:
            #     print(e)
            # conn_test.commit()

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

def get_builds(url):
    try:
        record_req = req.urlopen(url, timeout=5)
        result = record_req.read().decode("utf_8").replace("renderReverse&&renderReverse","").replace("(","").replace(")","")
        return(result)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    get_loc()
    pass