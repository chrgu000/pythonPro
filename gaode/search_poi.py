# -*- coding: utf-8 -*
import urllib
import urllib.request as req
import urllib.parse as parse
import json

def search_poi():
    c = ["0","1","2","3","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    for i1 in range(0,len(c)):
        for i2 in range(0, len(c)):
            for i3 in range(0, len(c)):
                for i4 in range(0, len(c)):
                    for i5 in range(0, len(c)):
                        counter="B000A"+c[i1]+c[i2]+c[i3]+c[i4]+c[i5]
                        print(counter)
                        url = "http://ditu.amap.com/detail/"+counter+"?citycode=110000"
                        try:
                            record_req = req.urlopen(url, timeout=3)
                            html=record_req.read().decode("utf_8")
                            if "<title>高德地图</title>" not in html and "商务住宅;楼宇;商务写字楼</span>" in html:
                                print(url)
                                file = open("./poi/" + counter + ".csv", 'a', encoding="utf-8")
                                file.write(html)
                                file.close()
                        except Exception as e:
                            print("")
if __name__=='__main__':
    search_poi()
    pass