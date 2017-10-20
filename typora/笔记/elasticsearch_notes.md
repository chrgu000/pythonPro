# elasticsearch notes

​    es查询使用json完整的请求体，叫做结构化查询（DSL），包含全文检索、分布式实时文件存储、实时分析的分布式搜索引擎、可扩展到百台服务器，处理PB级的结构过或非结构化数据

名词解释：

cluster：集群

index：索引，index相当于关系型数据库的DataBase

Type：类型，索引下的逻辑划分，把具有共性的文档放到一个类型中，相当于关系型数据库的table

Document：文档，json结构，相当于table中一行数据

Shard、Replica：分片、副本

## Filter DSL: term  、terms、range、exists、missing、bool(must  must_not  should)

range：允许按照指定范围查找一批数据 

{

​    "range":{

​        "age":{

​             "gte":20,

​              "lt":30

​      }

​    }

}

gt:大于

gte：大于等于

lt：小于

lte：小于等于

extists missing 用于查找文档中是否包含指定字段或不包含指定字段

bool 用来合并多个过滤条件查询结果的布尔逻辑，它包含：

​       must：多个查询条件完全匹配，相当于and

​       must_not:多个条件的相反匹配

​        should：至少有一个条件匹配

##  Query DSL: match_all 、match、bool

​    match_all:查询所有文档

​    match：只能就指定某个确切的值进行搜索

​    multi_match:允许做match查询的基础上同事搜索多个字段，在多个字段中同时查一个

​    bool查询：用于合并多个子查询，bool过滤是可以直接给出匹配是否成功，而bool过滤则是需要计算出每一个查询子句的 _score

​      must：查询指定文档一定被包含

​      must _not :查询指定文档一定不要被包含

​       should：查询指定文档，有则可以为文档相关性加分

## wildcards（通配符）查询：标准的shell通配符查询

* *：与零个或多个字符匹配
* ？：与任何单个字符匹配
* [] ：与？类似，但允许指定的更确切，与括号中字符匹配
* [!] ：不与括号中任何字符匹配

## regexp查询：正则查询

prefix查询：以什么字符开头，可以更简单的使用prefix。

## match_prase(短语匹配)