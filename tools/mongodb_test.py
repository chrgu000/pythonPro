# -*- coding: utf-8 -*


from pymongo import MongoClient

# 连接mongodb

client = MongoClient("103.234.21.72", 27017)
db = client.TYCHtml
db.authenticate("tychtml", "2zeg4uei0364h21thw9m6")
collections = db.companys
print()

def change_cid_to_mongoid():
    result = collections.find({"companyPortray.comName": "锦州越光农产有限公司"}, {"_id": 1})
    for i in result:
        print(i)


if __name__ == '__main__':
    change_cid_to_mongoid()
    pass