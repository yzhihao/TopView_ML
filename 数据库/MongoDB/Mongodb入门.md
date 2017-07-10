# MongoDB

* [简介](#简介)
* [安装](#安装)
* [使用](#使用)
	* [增](#插入数据)
	* [查](#查找数据)
	* [改](#数据更新)
	* [删](#删除数据/集合/数据库)


## 简介
- MongoDB就是一种非关系型数据库，它的优点就在于相比sql，用户的访问速度更快，获取数据的方式更加便携。


## 安装
- Mac os 下安装MongoDB只需终端简单的命令(前提是你安装了homebrew)，

- 安装 mongodb
- ```python
sudo brew install mongodb
```
如果要安装支持 TLS/SSL 命令如下：
```python
sudo brew install mongodb --with-openssl
```
安装最新开发版本：
```python
sudo brew install mongodb --devel
```

## 使用

- 终端输入一下命令，打开mongodb shell
```python
$ mongo
```

### 查看全部数据库/集合

- ```python
> show dbs
admin         0.000GB
local         0.000GB
pymongo_test  0.000GB
student       0.000GB
> show collections
asd
student
```

### 切换/创建数据库
- 当数据库不存在的时候用 **use** **databaseName** 自动创建名字为 **databaseName** 的数据库
- ```python
> use student
```

### 插入数据
- 用 **db.collectionName.insert()** 即可插入数据，可以发现在插入的数据中有 **"\_id"** 这一项，它是一个在全集合范围内**不重复**的字段，用以标记该文档，它还可以由我们自行定义(自己手动插入)。同一集合只能的\_id必须**互异**
- ```python
> db.student.insert({No : 1,name : 'chok'})
> db.student.find()
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
```

- 用 **db.collectionName.insertMany()** 可以插入一个数组的数据
- ```python
> db.student.insertMany([
... {No : 2,name : 'JoJo'},
... {No : 3,name : 'Alan'},
... {No : 4,name : 'misaka'},
... {No : 5,name : 'test to Delete'}])
{
	"acknowledged" : true,
	"insertedIds" : [
		ObjectId("5962e804e5faf5471f4839bb"),
		ObjectId("5962e804e5faf5471f4839bc"),
		ObjectId("5962e804e5faf5471f4839bd"),
		ObjectId("5962e804e5faf5471f4839be")
	]
}
> db.student.find()
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bd"), "No" : 4, "name" : "misaka" }
{ "_id" : ObjectId("5962e804e5faf5471f4839be"), "No" : 5, "name" : "test to Delete"}
```



### 查找数据
- 查找数据可以使用 **db.collectionName.find()** 进行数据查找，**findOne()** 查找一条文档
```python
> db.student.find()
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bd"), "No" : 4, "name" : "misaka" }
{ "_id" : ObjectId("5962e804e5faf5471f4839be"), "No" : 5, "name" : "test to Delete"}
```

- 还有一些常见的对结果集操作的方法
| 方法 | 功能 |
|--------|--------|
|count() |对查找结果进行计数|
|skip( **Number** )|   查找时跳过 **Number** 个文档     |
|limit( **Number** ) |	仅查找前 **Number** 个结果|
|sort( **KEY：****1或-1** ) 	|对查找结果按照键 **KEY** 进行排序，1表示升序，-1表示降序|
|pretty() |	以易读的方式来读取数据|
```python
> db.student.find().limit(3)
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
```

#### 条件查找
- 在find()中传入参数，返回符合要求的结果集
| 操作 | 格式 |
|--------|--------|
| 小于 	 |{ key :  { $lt : value}}|
|小于或等于 |{ key : { $lte : value}}|
|大于 	 |{ key : { $gt : value}}|
|大于或等于 |{ key : { $gte : value}}|
|不等于    |{ key : { $ne : value}}   |
```python
> db.student.find({'No':{$lt:3}})
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
```

#### or 和 And
- 若想使用 **And** 查找，各条件用**逗号**隔开就好
```python
> db.student.find({'No':1,'name':'chok'})
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
```

- **or** 若想使用 "or" 查找，则可以使用 **$or** 关键字
```python
> db.student.find({$or:[{'No':3},{'name': "misaka"}]})
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bd"), "No" : 4, "name" : "misaka" }
```


#### 类型查找
- 有时候我们需要根据数据类型来查找相应的数据，这个时候我们就需要用到 **$type操作符** 。 **$type**   操作符基于BSON类型来检索集合中匹配的类型，并返回结果。
```python
> db.student.insert({No : '1',name : 'chok'})
> db.student.find({'No':{$type:2})
{ "_id" : ObjectId("5962f603e5faf5471f4839bf"), "No" : "1", "name" : "chok" }
```
| 类型 | 数字 |类型|数字|类型|数字|类型|数字|
|--------|--------|--------|--------|--------|--------|
|Double| 1 |String |2 |Object |3 |Array |4 |
|Binary data|5 |Undefined(已废弃) |6 |Object id| 7 |Boolean| 8 |
|Date |9 |Null |10 |Regular Expression |11 |JavaScript |13 |
|Symbol |14 |JavaScript (with scope)| 15|32-bit integer |16 | Timestamp| 17 |
|64-bit integer |18 |Min key |255| Query with| -1.| Max key |127 |

#### 存在性查找
- MongoDB支持我们对一项数据是否存在的结果进行查找，通过$exists命令符：
```python
> db.student.insert({x:1})
> db.student.find({'x':{$exists:true}})
{ "_id" : ObjectId("5962f87de5faf5471f4839c0"), "x" : 1 }
```

#### 数据更新
- 更新集合中的数据使用update(CONDITION,OPERATE)命令，它接收两个参数，前者为条件，后者为进行更新的操作:
```python
> db.student.update({'No':5},{'No':5,'name':'test'})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.student.find()
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bd"), "No" : 4, "name" : "misaka" }
{ "_id" : ObjectId("5962e804e5faf5471f4839be"), "No" : 5, "name" : "test" }
{ "_id" : ObjectId("5962f603e5faf5471f4839bf"), "No" : "1", "name" : "chok" }
{ "_id" : ObjectId("5962f87de5faf5471f4839c0"), "x" : 1 }
```

- 更新数据默认会覆盖原来的文档（如果你们有完整输入数据，则会造成部分数据缺失），若只是想局部修改数据可以使用$set 关键字
```python
> db.student.update({'No':5},{$set:{'name':'Test'}})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.student.find()
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bd"), "No" : 4, "name" : "misaka" }
{ "_id" : ObjectId("5962e804e5faf5471f4839be"), "No" : 5, "name" : "Test" }
{ "_id" : ObjectId("5962f603e5faf5471f4839bf"), "No" : "1", "name" : "chok" }
{ "_id" : ObjectId("5962f87de5faf5471f4839c0"), "x" : 1 }
```

- 如果你想要更新一个数据，但这个数据不一定存在，你可以在 **update** 的第三个参数传入一个 **true**，这种情况比较像 目录是否存在，不存在我就创建的意思。
```python
> db.student.update({"x":2},{"y":1},true)
WriteResult({
	"nMatched" : 0,
	"nUpserted" : 1,
	"nModified" : 0,
	"_id" : ObjectId("5963081c9a976a763f7f1f6c")
	> db.student.find()
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bd"), "No" : 4, "name" : "misaka" }
{ "_id" : ObjectId("5962e804e5faf5471f4839be"), "No" : 5, "name" : "Test" }
{ "_id" : ObjectId("5962f603e5faf5471f4839bf"), "No" : "1", "name" : "chok" }
{ "_id" : ObjectId("5962f87de5faf5471f4839c0"), "x" : 1 }
{ "_id" : ObjectId("5963081c9a976a763f7f1f6c"), "y" : 1 }
})
```

- 如果你想一次更新多条数据(update在使用的时候，默认只更新被查找到的第一条数据),则传入第四个参数为**true**

```python
db.student.update({"y":1},{"x":1})
> db.student.find()
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bd"), "No" : 4, "name" : "misaka" }
{ "_id" : ObjectId("5962e804e5faf5471f4839be"), "No" : 5, "name" : "Test" }
{ "_id" : ObjectId("5962f603e5faf5471f4839bf"), "No" : "1", "name" : "chok" }
{ "_id" : ObjectId("5962f87de5faf5471f4839c0"), "x" : 1 }
{ "_id" : ObjectId("5963081c9a976a763f7f1f6c"), "x" : 1 }
> db.student.update({x:1},{$set:{x:2}},false,true)
WriteResult({ "nMatched" : 2, "nUpserted" : 0, "nModified" : 2 })
> db.student.find()
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bd"), "No" : 4, "name" : "misaka" }
{ "_id" : ObjectId("5962e804e5faf5471f4839be"), "No" : 5, "name" : "Test" }
{ "_id" : ObjectId("5962f603e5faf5471f4839bf"), "No" : "1", "name" : "chok" }
{ "_id" : ObjectId("5962f87de5faf5471f4839c0"), "x" : 2 }
{ "_id" : ObjectId("5963081c9a976a763f7f1f6c"), "x" : 2 }
```

- **"errmsg" : "multi update only works with $ operators"** 使用多条更新时必须要与操作符同时使用

### 删除数据/集合/数据库
- **remove** 会删除所有匹配到的数据，但如果只想删除匹配的第一条数据令**remove**第二个参数为**true**即可
```python
> db.student.remove({x:2})
db.student.find()
{ "_id" : ObjectId("5962e740e5faf5471f4839ba"), "No" : 1, "name" : "chok" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bb"), "No" : 2, "name" : "JoJo" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bc"), "No" : 3, "name" : "Alan" }
{ "_id" : ObjectId("5962e804e5faf5471f4839bd"), "No" : 4, "name" : "misaka" }
{ "_id" : ObjectId("5962e804e5faf5471f4839be"), "No" : 5, "name" : "Test" }
{ "_id" : ObjectId("5962f603e5faf5471f4839bf"), "No" : "1", "name" : "chok" }
> db.asd.drop()
true
> db.dropDatabase()
{ "dropped" : "student", "ok" : 1 }
```