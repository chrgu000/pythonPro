# mongodb 查询语句

mongodb :分布式文件存储数据库，介于关系数据库和非关系数据库之间

TYCHtml数据库：
## 1、查询document数量     

​    db.getCollection('companys').find({}).count()

## 2、find()

db.getCollection('companys').find({"_id":ObjectId("59c12543e1382308c4e0f786")})

​                    = select * from companys where _id="59c12542e1382308c4e0f262"

db.getCollection('companys').find({},{"summary":1})

​                   =select summary from companys 

内嵌文档查询：
db.getCollection('companys').find({"summary.reportCount":4}).limit(1)
db.getCollection('companys').find({"staffCount":{$elemMatch:{"position":"监事","name":"宋家林"}}}).limit(1)
db.getCollection('companys').find({"summary.reportCount":4,"summary.checkCount":1}).limit(1)
MongoDB提供了一组比较操作符：

| $lt  |  <   |
| :--: | :--: |
| $lte |  <=  |
| $gt  |  >   |
| $gte |  >=  |
| $ne  |  !=  |

删除数据库：db.dropDatabase()

查看所有数据库show dbs   

创建数据库：use runoob

插入文档：db.COLLECTION_NAME(document)

更新文档：db.collection.update()

使用$elemMatch操作符查询
同一个元素中的键值组合

模糊查询 $regex
