# -*- coding: utf-8 -*
'''
添加公司所处的地理层级
建立ms_map_area_info相关代码
'''
import urllib.request as req
import urllib.parse as parse
import json
import pymysql
import uuid
import math

def get_loc():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select u_id,b_lat,b_lon,b_building_name from buildings_info where adr_scale_two="+"\""+"\"")
    count = 0
    for r in cur_test.fetchall():
        print(r[3])
        print(count)
        uid = r[0]
        lat = str(r[1]).replace("\n", "")
        lon = str(r[2]).replace("\n", "")
        url = "http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location="+lat+","+lon+"&output=json&pois=1&ak=nPPBW9xruVM07MG5B3QLqjpwoPCLtP6E"
        # url = "http://api.map.baidu.com/geocoder/v2/?address="+parse.quote(aname)+"&output=json&ak=nPPBW9xruVM07MG5B3QLqjpwoPCLtP6E&callback=showLocation"
        json_geo = get_builds(url)
        print(json_geo)
        if "无相关结果" not in json_geo:
            json_dict = eval(json_geo)
            one = json_dict["result"]["addressComponent"]["district"]
            two = json_dict["result"]["addressComponent"]["street"]
            print(two)
            # try:
            #     cur_test.execute("update buildings_info set adr_scale_one="+"\""+one+"\"" +","+"adr_scale_two="+"\""+two+"\"" +" where u_id="+"\""+uid+"\"")
            #     print("update buildings_info set adr_scale_one="+"\""+one+"\"" +","+"adr_scale_two="+"\""+two+"\"" +" where u_id="+"\""+uid+"\"")
            #     conn_test.commit()
            # except Exception as e:
            #     print(e)
        #count += 1
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

def set_map_scale_two():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    #scale_two = "安贞 奥林匹克公园 安苑 北沙滩 北苑 百子湾 常营 CBD 朝阳北路 朝阳公园 朝阳门 草房 大山子 东坝 东八里庄 定福庄 东大桥 大悦城 大望路 豆各庄 垡头 甘露园 高碑店 管庄 工体 国贸 国展 花家地 呼家楼 红庙 惠新西街 和平街 华威桥 欢乐谷 健翔桥 酒仙桥 劲松 建国门外 来广营 柳芳 马甸 潘家园 芍药居 石佛营 四惠 双桥 双井 十八里店 三里屯 三元桥 十里堡 四方桥 太阳宫 团结湖 甜水园 望京 西坝河 亚奥 亚运村 亚运村小营 燕莎 左家庄 枣营"
    #scale_two = "白石桥 北京大学 北太平庄 厂洼 车道沟 大钟寺 定慧寺 大慧寺 二里庄 公主坟 航天桥 花园桥 蓟门桥 军博 牡丹园 马连洼 清华大学 清河 人民大学 双榆树 上地 世纪城 苏州桥 四季青 苏州街 田村 魏公村 五道口 五棵松 万寿路 万柳 万泉河 小西天 西二旗 西三旗 香山 西北旺 学院路 西山 西直门外 学院南路 圆明园 颐和园 玉泉路 永定路 知春路 中关村 增光路 紫竹桥 皂君庙"
    #scale_two = "北大地 北京西站 成寿寺 菜户营 草桥 长辛店 大红门 东高地 方庄 丰益桥 丰台科技园 丰台体育馆 和义 花乡 角门 看丹桥 丽泽桥 六里桥 卢沟桥 刘家窑 马家堡 木樨园 南苑 蒲黄榆 青塔 七里庄 宋家庄 五里店 西罗园 新发地 洋桥 玉泉营 岳各庄 右安门外 赵公口 左安门"
    #scale_two = "安定门 北新桥 朝阳门内 崇文门 磁器口 东四十条 东单 灯市口 东四 东花市 东直门 光明楼 广渠门 和平里 交道口 金宝街 建国门 龙潭湖 前门 天坛 天坛 王府井 雍和宫 永定门"
    #scale_two ="白纸坊 白云路 白广路 车公庄 长椿街 菜市口 地安门 德胜门 大栅栏 复兴门 阜成门 鼓楼大街 官园 广安门 甘家口 和平门 虎坊桥 金融街 积水潭 六铺炕 马连道 木樨地 南礼士路 牛街 什刹海 三里河 天宁寺 天桥 陶然亭 新街口 西四 西便门 宣武门 西单 西直门 右安门 月坛 展览路"
    #scale_two ="八角 八宝山 八大处 高井 古城 金顶街 老山 鲁谷 模式口 苹果园 杨庄"
    #scale_two = "黄村北 黄村南 黄村 旧宫 旧宫西 庞各庄 天宫院 西红门 亦庄"
    # scale_two = "八里桥 北关 东关 果园 九棵树 焦王庄 梨园 潞苑 马驹桥 乔庄 通州北苑 土桥 武夷花园 新华大街 玉桥 运河大街"
    # scale_two ="后沙峪 空港工业区 李桥 马坡 首都机场 顺义城 天竺 杨镇 中央别墅区"
    #scale_two ="北七家 百善镇 昌平县城 回龙观 霍营 立水桥 南口 沙河 天通苑 小汤山"
    #scale_two ="长阳 窦店 房山城关 韩村河 良乡 琉璃河 青龙湖 石楼镇 燕山 阎村 周口店"
    #scale_two = "百泉街道 香水园街道 儒林街道 康庄镇 八达岭镇 永宁镇 旧县镇 张山营镇 四海镇 千家店镇 沈家营镇 大榆树镇 井庄镇 刘斌堡乡 大庄科乡 香营乡 珍珠泉乡"
    # scale_two = "滨河街道 兴谷街道 平谷镇 峪口镇 马坊镇 金海湖镇 东高村镇 山东庄镇 南独乐河镇 大华山镇 夏各庄镇 马昌营镇 王辛庄镇 大兴庄镇 刘家店镇 镇罗营镇 黄松峪乡 熊儿寨乡"
    # scale_two ="大峪街道 城子街道 东辛房街道 大台街道 龙泉地区 永定地区 王平地区 龙泉镇 永定镇 潭柘寺镇 军庄镇 王平镇 雁翅镇 斋堂镇 清水镇 妙峰山镇"
    # scale_two="鼓楼街道、果园街道、密云镇、十里堡镇、河南寨镇、溪翁庄镇、穆家峪镇、巨各庄镇、西田各庄镇、大城子镇、石城镇、太师屯镇、北庄镇、高岭镇、不老屯镇、古北口镇、冯家峪镇、东邵渠镇、新城子镇、檀营满族蒙古族乡"
    scale_two = "怀柔镇、雁栖镇、北房镇、杨宋镇、庙城镇、桥梓镇、怀北镇、汤河口镇、渤海镇、九渡河镇、琉璃庙镇、宝山镇、长哨营满族乡、喇叭沟门满族乡、泉河街道、龙山街道"
    slist = scale_two.split("、")
    print(slist)
    for i in range(0, len(slist)):
        try:
            cur_test.execute("insert into search_map_scale(map_scale,area_name) VALUES ( "+"\""+"s_"+str((i+1))+"\""+","+"\""+slist[i]+"\""+")")
            conn_test.commit()
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.close()

def set_map_scale_loc():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    file = open("scale_two_lon.csv", encoding="utf-8")
    loc = file.readlines()
    for i in range(0, 87):
        aname = loc[i].split(":")[0]
        lng = loc[i].split(":")[1].split(",")[0].replace("\n", "")
        lat = loc[i].split(":")[1].split(",")[1].replace("\n", "")
        try:
            sql = "update search_map_scale set area_lat="+"\""+str(lat)+"\"" +","+"area_lng="+"\""+str(lng)+"\""+" where area_name="+"\""+aname+"\""
            print(sql)
            cur_test.execute(sql)
            conn_test.commit()
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.close()


def add_uuid():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select area_name from search_map_scale")
    for r in cur_test.fetchall():
        print(r[0])
        auid = get_uuid(r[0])
        try:
            sql = "update search_map_scale set a_uid="+"\""+auid+"\""+" where area_name="+"\""+r[0]+"\""
            print(sql)
            cur_test.execute(sql)
            conn_test.commit()
        except Exception as e:
            print(e)
    cur_test.close()
    conn_test.close()

def get_uuid(name):
    uid_ = uuid.uuid3(uuid.NAMESPACE_DNS, name)
    uid = str(uid_).replace("-", "")
    return uid

def update_scale():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select u_id,adr_scale_one,adr_scale_two,b_lat,b_lon,b_building_name from buildings_info")
    for row in cur_test.fetchall():
        buid = row[0]
        print(row[5])
        one_uid = ""
        lat1 = row[3]
        lon1 = row[4]
        cur_test.execute("SELECT a_uid,map_scale FROM search_map_scale where area_name="+"\""+row[1]+"\"")
        map_scale = ""
        for r1 in cur_test.fetchall():
            one_uid = r1[0]
            map_scale = r1[1]

        two_uid = ""
        cur_test.execute("select a_uid,area_lat,area_lng from search_map_scale where map_scale like "+"\"%"+map_scale+"%\"")
        min_dis = 100000
        for r2 in cur_test.fetchall():
            lat2 = r2[1]
            lon2 = r2[2]
            if dis(lat1, lon1, lat2, lon2) < min_dis:
                min_dis = dis(lat1, lon1, lat2, lon2)
                two_uid = r2[0]
        print("update buildings_info set adr_scale_one=" +"\""+one_uid +"\""+","+"adr_scale_two="+"\""+two_uid+"\"" +"where u_id="+"\""+buid+"\"")
        if one_uid !="":
            cur_test.execute("update buildings_info set adr_scale_one=" +"\""+one_uid +"\""+","+"adr_scale_two="+"\""+two_uid+"\"" +"where u_id="+"\""+buid+"\"")
            conn_test.commit()

    cur_test.close()
    conn_test.close()

def dis(lat1, lon1, lat2, lon2):
    dist = math.sqrt((float(lat1)-float(lat2))*(float(lat1)-float(lat2))+(float(lon1)-float(lon2))*(float(lon1)-float(lon2)))
    return dist


def contain_building_num():
    conn_test = conn_test_yunketest()
    cur_test = conn_test.cursor()
    cur_test.execute("select a_uid,map_scale from search_map_scale")
    for r in cur_test.fetchall():
        count = 0
        if "_" not in r[1]:
            cur_test.execute("SELECT COUNT(*) FROM buildings_info WHERE adr_scale_one=" + "\"" + r[0] + "\"")
            for c in cur_test.fetchall():
                count = str(c).replace("(","").replace(")","").replace(",","")
        else:
            cur_test.execute("SELECT COUNT(*) FROM buildings_info WHERE adr_scale_two="+"\""+r[0]+"\"")
            for c in cur_test.fetchall():
                count = str(c).replace("(","").replace(")","").replace(",","")
        print("update search_map_scale set contain_buildings_num="+"\""+str(count)+"\""+" where a_uid="+"\""+ r[0]+"\"")
        cur_test.execute("update search_map_scale set contain_buildings_num="+"\""+str(count)+"\""+" where a_uid="+"\""+ r[0]+"\"")
        conn_test.commit()
    cur_test.close()
    conn_test.close()


if __name__ == '__main__':
    # get_loc()
    #set_map_scale_two()
    #set_map_scale_loc()
    #add_uuid()
    #update_scale()
    contain_building_num()
    pass