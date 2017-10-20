#!user/bin/env python3
#-*- coding: utf-8 -*

import re
import json
import os
import shutil
import time
from pymongo import MongoClient

client = MongoClient("117.122.215.26", 27017)
db = client.TYCHtml
collection = db.companys

field = ["changeCount", "reportCount", "zhixing", "staffCount", "qualification", "companyPortray",
         "patentCount", "inverstCount", "bidCount", "tmCount", "taxCreditCount", "holderCount",
         "icpCount", "productinfo", "abnormalCount", "cpoyRCount", "punishment", "recruitCount",
         "checkCount", "dishonest", "jigouTzanli", "companyRongzi", "companyJingpin", "branchCount",
         "lawsuitCount", "mortgageCount", "equityCount", "courtCount", "companyTeammember", "companyProduct"]

null = lambda x: None
data = lambda x: x["data"]
data_result = lambda x: x["data"]["result"]
data_items = lambda x: x["data"]["items"]
data_parseitems = lambda x: json.loads(x["data"])["items"]
data_page_rows = lambda x: x["data"]["page"]["rows"]
data_court = lambda x: x["courtAnnouncements"]
data_employ = lambda x: x["data"]["companyEmploymentList"]
parseDict = {
    "abnormalCount": data_result,  # 经营异常
    "bidCount": data_items,  # 招投标
    "branchCount": null,  # 分支机构
    "changeCount": data_result,  # 变更记录
    "checkCount": data_items,  # 抽查检查
    "companyJingpin": data_page_rows,  # 竞品信息
    "companyPortray": null,  # 基本信息
    "companyProduct": data_page_rows,  # 企业业务
    "companyRongzi": data_page_rows,  # 融资历史
    "companyTeammember": data_page_rows,  # 核心团队
    "courtCount": data_court,  # 法院公告
    "cpoyRCount": data_items,  # 著作权
    "dishonest": data_items,  # 失信人
    "equityCount": data_items,  # 股权出质
    "holderCount": data_result,  # 股东信息
    "icpCount": data,  # 网站备案
    "inverstCount": data_result,  # 对外投资
    "jigouTzanli": null,  # 投资事件
    "lawsuitCount": data_items,  # 法律诉讼
    "mortgageCount": data_parseitems,  # 动产抵押
    "patentCount": data_items,  # 专利
    "productinfo": data_items,  # 产品信息
    "punishment": data_items,  # 行政处罚
    "qualification": data_items,  # 资质证书
    "recruitCount": data_employ,  # 招聘
    "reportCount": data,  # 企业年报
    "staffCount": data_result,  # 主要人员
    "taxCreditCount": data_items,  # 税务评级
    "tmCount": data_items,  # 商标信息
    "zhixing": data_items  # 被执行人
}
nameDict = {
    "abnormalCount": "经营异常",
    "bidCount": "招投标",
    "branchCount": "分支机构",
    "changeCount": "变更记录",
    "checkCount": "抽查检查",
    "companyJingpin": "竞品信息",
    "companyPortray": "基本信息",
    "companyProduct": "企业业务",
    "companyRongzi": "融资历史",
    "companyTeammember": "核心团队",
    "courtCount": "法院公告",
    "cpoyRCount": "著作权",
    "dishonest": "失信人",
    "equityCount": "股权出质",
    "holderCount": "股东信息",
    "icpCount": "网站备案",
    "inverstCount": "对外投资",
    "jigouTzanli": "投资事件",
    "lawsuitCount": "法律诉讼",
    "mortgageCount": "动产抵押",
    "patentCount": "专利",
    "productinfo": "产品信息",
    "punishment": "行政处罚",
    "qualification": "资质证书",
    "recruitCount": "招聘",
    "reportCount": "企业年报",
    "staffCount": "主要人员",
    "taxCreditCount": "税务评级",
    "tmCount": "商标信息",
    "zhixing": "被执行人",

    "graphInfo": "企业关系",
    "illegalCount": "严重违法",
    "ownTaxCount": "欠税公告",
    "bondCount": "债券信息",
    "goudiCount": "购地信息"
}


def parse(f, content):
    # return content
    try:
        return parseDict[f](content)
    except Exception as e:
        return None


Dict = {f: [] for f in field}
Success = {f: 0 for f in field}
Total = {f: 0 for f in field}

insertSuccess = []
insertFailed = []
fileFailed = []


def write2db(company):
    try:
        collection.insert_one(company)
        # insertSuccess.append(company["_id"])
    except Exception as e:
        print(e)

def process(jsonDir):
    print("process dir: %s" % jsonDir)
    for file in os.listdir(jsonDir):
        try:
            company = json.loads(open(jsonDir + "//" + file, 'r').read())
            summary = company["summary"]
            companyWrite = {}
            companyWrite["_id"] = company["cid"]
            companyWrite["name"] = company["title"]
            companyWrite["summary"] = company["summary"]
            for f in field:
                try:
                    if int(summary[f]) != 0: Total[f] += 1
                except Exception as e:
                    pass
                if f in company:
                    obj = parse(f, company[f])
                    if obj:
                        companyWrite[f] = obj
                        Success[f] += 1
                        if Success[f] <= 100: Dict[f].append(obj)
            write2db(companyWrite)
        except Exception as e:
            fileFailed.append(jsonDir + "/" + file)
            # write companyWrite to database
            # write2db(companyWrite)

    return len(os.listdir(jsonDir))


def main(dataDir):
    print("***")
    count = 0
    timestart = time.time()

    for jsonDir in os.listdir(dataDir):
        print("processed count:", count)
        if not re.match(r"\d{4}", jsonDir): continue
        count += process(dataDir + "/" + jsonDir)

    print("Process data used: %.1f seconds" % (time.time() - timestart))
    print("data length is : %d" % count)

    try:
        shutil.rmtree("log")
    except:
        print("log目录不存在.")
    os.mkdir("log")

    open("log/success", 'w').write(json.dumps(insertSuccess))
    open("log/failed", 'w').write(json.dumps(insertFailed))
    open("log/filefailed", 'w').write(json.dumps(fileFailed))

    try:
        shutil.rmtree("field")
    except:
        print("field目录不存在.")
    os.mkdir("field")

    for f in field:
        # l = len(Dict[f])
        l = Success[f]
        open("field/%s.%d-%d-%.2f%%-%.2f%%" % (nameDict[f], l, Total[f], 100 * (1 if Total[f] == 0 else l / Total[f]), \
                                               100 * l / count), 'w').write(
            json.dumps(Dict[f], indent=2, ensure_ascii=False))
        print("%s\t%d\t%d\t%.2f%%\t%.2f%%" % (nameDict[f], l, Total[f], 100 * (1 if Total[f] == 0 else l / Total[f]), \
                                              100 * l / count))


if __name__ == '__main__':
    main("out")
