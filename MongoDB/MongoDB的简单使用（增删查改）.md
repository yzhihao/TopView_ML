# MongoDB的简单使用（增删查改）

## 连接数据库

要连接数据库，我们首先需要启动MongoDB的服务，然后通过MongoDB提供的客户端mongo.exe来启动MongoDB。
```
D:\>cd D:\study\Mongo DB\Program\bin

D:\study\Mongo DB\Program\bin>mongo.exe
MongoDB shell version v3.4.6
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.4.6
...
```
当然也可以将bin目录直接添加进环境变量以方便我们可以在cmd直接启动。

## 数据库操作

##### 查看所有数据库
首先是`show dbs`命令，它允许我们查看当前可用的所有数据库：
```
> show dbs
admin  0.000GB
local  0.000GB
test   0.000GB
```

##### 切换数据库

然后是`use`命令，我们可以通过这个命令指定要使用的数据库：
```
> use test
switched to db test
```
不仅是对于存在的数据库，对于不存在的数据库我们也可以使用`use`命令，这个时候，MongoDB会根据情况自动创建对应的数据库：
```
> show dbs
admin  0.000GB
local  0.000GB
test   0.000GB
> use zyzy
switched to db zyzy
```

##### 删除数据库

若是要删除数据库，则在切换到对应数据库后，使用`db.Dropdatabase()`命令，即可删除：
```
> use zyzy
switched to db zyzy
> db.dropDatabase()
{ "ok" : 1 }
> show dbs
admin  0.000GB
local  0.000GB
test   0.000GB
```

## 对数据操作

##### 插入数据

集合相当于mysql中的table，要在数据库中插入一个集合，可以使用`db.collectionname.insert(<json>)`:
```
> db.zyzy_collection.insert({x:1})
WriteResult({ "nInserted" : 1 })
> show dbs
admin  0.000GB
local  0.000GB
test   0.000GB
zyzy   0.000GB
> show collections
zyzy_collection
```
< json >表示往集合插入的文档内容。

MongoDB支持java script语法，因此，我们可以使用一些相应语法来插入多条数据
```
> for(i=0;i<10;i++)db.asd.insert({x:i})
WriteResult({ "nInserted" : 1 })
> db.asd.find()
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca118"), "x" : 0 }
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca119"), "x" : 1 }
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca11a"), "x" : 2 }
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca11b"), "x" : 3 }
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca11c"), "x" : 4 }
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca11d"), "x" : 5 }
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca11e"), "x" : 6 }
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca11f"), "x" : 7 }
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca120"), "x" : 8 }
{ "_id" : ObjectId("5961021cd4fd4ce8ff6ca121"), "x" : 9 }
```

另外，还有`insertMany()`方法，通过接收一个数组来添加多个文档。

##### 查找数据

除了上面使用过的`show collectins`或者`show tables`可以同时查找所有数据库中的集合，还有命令`db.collectionname.find(<json>)`可以查找对应数据库下的集合：
```
> db.zyzy_collection.find()
{ "_id" : ObjectId("5960f85ed4fd4ce8ff6ca115"), "x" : 1 }
```
`find()`中的括号为空时，表示查找所有该数据库下的集合。
我们可以发现，集合中除了`"x":1`这条我们初始化的信息内容之外，还有一条`"_id"`,这条信息不是由我们定义的，它是一个在全集合范围内不会重复的字段，用以标记该文档，它还可以由我们自行定义：
```
> db.asd.insert({x:1})
WriteResult({ "nInserted" : 1 })
> show collections
asd
zyzy_collection
> db.asd.insert({x:2,_id:1})
WriteResult({ "nInserted" : 1 })
> db.zyzy_collection.insert({x:3,_id:1})
WriteResult({ "nInserted" : 1 })
> db.zyzy_collection.insert({x:4,_id:1})
WriteResult({
        "nInserted" : 0,
        "writeError" : {
                "code" : 11000,
                "errmsg" : "E11000 duplicate key error collection: zyzy.zyzy_collection index: _id_ dup key: { : 1.0 }"
        }
})

> db.asd.find()
{ "_id" : ObjectId("5960ff1ed4fd4ce8ff6ca117"), "x" : 1 }
{ "_id" : 1, "x" : 2 }
> db.zyzy_collection.find()
{ "_id" : ObjectId("5960f85ed4fd4ce8ff6ca115"), "x" : 1 }
{ "_id" : ObjectId("5960f95dd4fd4ce8ff6ca116"), "x" : 1, "y" : 1 }
{ "_id" : 1, "x" : 3 }
```
可以发现，数据库`asd`和`zyzy_collection`中可以同时存在`"_id"`为1的文档，但是当我们在`zyzy_colleciotn`中创建第二个`"_id"`为1的文档的时候会弹出错误信息（`"nInserted":0`）

当我们需要查找特定的文档时，就可以在`find()`中的括号内写上查找的条件，同样也是json格式：
```
> db.zyzy_collection.find({x:1})
{ "_id" : ObjectId("5960f85ed4fd4ce8ff6ca115"), "x" : 1 }
{ "_id" : ObjectId("5960f95dd4fd4ce8ff6ca116"), "x" : 1, "y" : 1 }
```
如上，找到所有包含`"x":1`的信息。

**find（）的方法**

`find()`还有一些特殊的方法，例如`count()`可以对集合中的文档数量进行计数：
```
> db.asd.find().count()
2
```
命令`skip()`表示查找时跳过的文档数：
```
> for(i=0;i<100;i++)db.asd.insert({x:i})
WriteResult({ "nInserted" : 1 })
> db.asd.find()
{ "_id" : ObjectId("5960ff1ed4fd4ce8ff6ca117"), "x" : 1 }
{ "_id" : 1, "x" : 2 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca124"), "x" : 0 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca125"), "x" : 1 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca126"), "x" : 2 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca127"), "x" : 3 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca128"), "x" : 4 }
...
> db.asd.find().skip(3)
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca125"), "x" : 1 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca126"), "x" : 2 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca127"), "x" : 3 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca128"), "x" : 4 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca129"), "x" : 5 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca12a"), "x" : 6 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca12b"), "x" : 7 }
```
显然，查找结果跳过了前面三条文档。

命令`limit()`用于表示最多显示的文档数：
```
> db.asd.find().limit(4)
{ "_id" : ObjectId("5960ff1ed4fd4ce8ff6ca117"), "x" : 1 }
{ "_id" : 1, "x" : 2 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca124"), "x" : 0 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca125"), "x" : 1 }
```
命令`sort(KEY：<1 or -1>)`用于对查找结果进行排序：
```
> db.asd.find().sort({x:1}).limit(4)
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca124"), "x" : 0 }
{ "_id" : ObjectId("5960ff1ed4fd4ce8ff6ca117"), "x" : 1 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca125"), "x" : 1 }
{ "_id" : 1, "x" : 2 }
> db.asd.find().sort({x:-1}).limit(4)
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca187"), "x" : 99 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca186"), "x" : 98 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca185"), "x" : 97 }
{ "_id" : ObjectId("596103dcd4fd4ce8ff6ca184"), "x" : 96 }
```

一些常用的方法记录在下表：

| 方法 | 功能 |
|--------|--------|
|    count（）    |  对查找结果进行计数      |
|skip（NUMBER）|查找时跳过NUMBER个文档|
|limit（NUMBER）|仅查找前NUMBER个结果|
|sort（KEY：<1 or -1>）|对查找结果按照键KEY进行排序，1表示升序，-1表示降序|
|pretty（）|以易读的方式来读取数据|

将`find()`改为`findOne()`可以只查找一条文档

**条件查找**
一些特殊的操作符允许我们对文档执行一定条件的查找

例如，要查找某个键中小于某个数的值，我们使用`{KEY:{$lt:<value>}}`:
```
> for(i=0;i<100;i++)db.test_collection.insert({x:i})
WriteResult({ "nInserted" : 1 })
> db.test_collection.find({x:{$lt:30}})
{ "_id" : ObjectId("5961bd0f540435d89b5c5ed1"), "x" : 0 }
{ "_id" : ObjectId("5961bd0f540435d89b5c5ed2"), "x" : 1 }
{ "_id" : ObjectId("5961bd0f540435d89b5c5ed3"), "x" : 2 }
{ "_id" : ObjectId("5961bd0f540435d89b5c5ed4"), "x" : 3 }
```
小于或等于使用`{KEY：{$lte:<value>}}`，更多方法可以参考下表

| 操作 | 格式 |
|--------|--------|
|小于|	`{<key>:{$lt:<value>}}`|
|小于或等于|	`{{<key>:{$lte:<value>}}`|
|大于|	`{<key>:{$gt:<value>}}`|
|大于或等于|`	{<key>:{$gte:<value>}}`|
|不等于|	`{<key>:{$ne:<value>}}`|

**AND查找**

`find({key1:value1, key2:value2})`括号内支持多个查找条件，只需要在括号用逗号将不同的查找条件隔开
```
> db.test_collection.insert({x:1,y:1,z:1})
WriteResult({ "nInserted" : 1 })
> db.test_collection.find({x:1,y:1})
{ "_id" : ObjectId("5961bec3540435d89b5c5f35"), "x" : 1, "y" : 1, "z" : 1 }
```

**OR查找**

MongoDB提供关键字`$or`来使用条件或的查找方式：
```
> db.test_collection.find({x:1})
{ "_id" : ObjectId("5961bd0f540435d89b5c5ed2"), "x" : 1 }
{ "_id" : ObjectId("5961bec3540435d89b5c5f35"), "x" : 1, "y" : 1, "z" : 1 }
{ "_id" : ObjectId("5961bf8d540435d89b5c5f36"), "x" : 1, "y" : 2, "z" : 1 }
{ "_id" : ObjectId("5961bf93540435d89b5c5f37"), "x" : 1, "y" : 2, "z" : 3 }

> db.test_collection.find({x:1,$or:[{y:1},{z:3}]})
{ "_id" : ObjectId("5961bec3540435d89b5c5f35"), "x" : 1, "y" : 1, "z" : 1 }
{ "_id" : ObjectId("5961c01b540435d89b5c5f39"), "x" : 1, "y" : 2, "z" : 3 }
```
上例表示查找同时包含`x:1`且包含`y:1`或者`z:3`的文档

**类型查找**

有时候我们需要根据数据类型来查找相应的数据，这个时候我们就需要用到`$type`操作符。
`$type`操作符基于BSON类型来检索集合中匹配的类型，并返回结果。

例如，我们想获取集合中“x”的值为数字类型的文档：
```
> db.test_collection.insert({x:1})
WriteResult({ "nInserted" : 1 })
> db.test_collection.insert({x:"asd"})
WriteResult({ "nInserted" : 1 })

> db.test_collection.find({x:{$type:1}})
{ "_id" : ObjectId("5961e906e12ea99cbdc056a1"), "x" : 1 }
> db.test_collection.find({x:{$type:"double"}})
{ "_id" : ObjectId("5961e906e12ea99cbdc056a1"), "x" : 1 }
```

MongoDB中支持的类型如下表：

| 类型 | 数字 |备注|
|--------|--------|
|Double|	1	 ||
|String	|2	 ||
|Object	|3	 ||
|Array	|4	 ||
|Binary data|	5	 ||
|Undefined	|6	|已废弃。|
|Object id|	7	 ||
|Boolean|	8	 ||
|Date	|9	 ||
|Null	|10	 ||
|Regular Expression	|11	 ||
|JavaScript	|13	 ||
|Symbol	|14	 ||
|JavaScript (with scope)|	15	 ||
|32-bit integer	|16	 ||
|Timestamp|	17	 ||
|64-bit integer	|18	 ||
|Min key	|255|	Query with -1.|
|Max key	|127	 ||

**存在性查找**

MongoDB支持我们对一项数据是否存在的结果进行查找，通过`$exists`命令符：
```
> db.test_collection.insertMany(
... [
... {x:1},{y:1}
... ]
... )

> db.test_collection.find({x:{$exists:true}})
{ "_id" : ObjectId("59623f322c1607a4c93adc40"), "x" : 1 }
```
发现仅查找到拥有x关键字的文档。

##### 数据更新

更新集合中的数据使用`update(CONDITION,OPERATE)`命令，它接收两个参数，前者为条件，后者为进行更新的操作:
```
> db.asd.insert({x:1})
WriteResult({ "nInserted" : 1 })
> db.asd.find()
{ "_id" : ObjectId("5961087fd4fd4ce8ff6ca18a"), "x" : 1 }
> db.asd.update({x:1},{x:2})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.asd.find()
{ "_id" : ObjectId("5961087fd4fd4ce8ff6ca18a"), "x" : 2 }
```
如上例，将文档中有`x:1`的改成`x:2`。

**局部更新**

有些时候，我们需要对文档进行局部更新，MongoDB中，默认一般情况的修改会对整个文档造成影响
```
> db.asd.insert({x:1,y:1,z:1})
WriteResult({ "nInserted" : 1 })
> db.asd.update({x:1},{y:2})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.asd.find()
{ "_id" : ObjectId("59610918d4fd4ce8ff6ca18b"), "y" : 2 }
```
例如上面的例子，我们只想对`{x:1,y:1,z:1}`进行修改使得`y:1`变为`y:2`，但如果直接使用`update()`会使得整个文档被修改的只剩下`y:1`。

这个时候，就需要使用`$set`来对文档进行局部更新
```
> db.asd.update({x:1},{$set:{y:2}})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.asd.find()
{ "_id" : ObjectId("596109e0d4fd4ce8ff6ca18c"), "x" : 1, "y" : 2, "z" : 1 }
```

**更新不存在的数据**

有时候，我们需要直接更新一条数据库中并不存在的数据，这个时候，仅仅用原来的`update()`的使用方法是达不到效果的，我们需要在括号里面加上第三个参数（Bool）来实现我们想要的效果
```
> db.zyzy.find()
> db.zyzy.update({x:1},{y:1},true)
WriteResult({
        "nMatched" : 0,
        "nUpserted" : 1,
        "nModified" : 0,
        "_id" : ObjectId("5961b6f09f1fbf45940b7f04")
})
> db.zyzy.find()
{ "_id" : ObjectId("5961b6f09f1fbf45940b7f04"), "y" : 1 }
```
**更新多条数据**

`update`在使用的时候，默认只更新被查找到的第一条数据，这是为了防止用户进行误操作。
```
> for(i=0;i<3;i++)db.zyzy.insert({x:1})
WriteResult({ "nInserted" : 1 })
#插入三条x为1的文档
> db.zyzy.update({x:1},{x:2})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.zyzy.find()
{ "_id" : ObjectId("5961b7fe540435d89b5c5eca"), "x" : 2 }
{ "_id" : ObjectId("5961b7fe540435d89b5c5ecb"), "x" : 1 }
{ "_id" : ObjectId("5961b7fe540435d89b5c5ecc"), "x" : 1 }
```
发现只有第一个文档被更新了。

要同时更新多条数据，就需要使用`update()`的第四个也是最后一个参数（Bool）。
```
> db.zyzy.update({x:1},{$set:{x:2}},false,true)
WriteResult({ "nMatched" : 2, "nUpserted" : 0, "nModified" : 2 })
> db.zyzy.find()
{ "_id" : ObjectId("5961b7fe540435d89b5c5eca"), "x" : 2 }
{ "_id" : ObjectId("5961b7fe540435d89b5c5ecb"), "x" : 2 }
{ "_id" : ObjectId("5961b7fe540435d89b5c5ecc"), "x" : 2 }
```
这里的更新方式通常都是使用局部更新的方式，也是为了防止误操作。

##### 数据删除

要删除集合中的数据，我们使用`remove(<query>)`方法，它接收一个参数，作为查找删除数据的条件，该参数不能为空。如果想清除集合里面的所有数据，可以直接时候用`drop()`废除集合。
```
> db.test_collection.find()
{ "_id" : ObjectId("5961b9d8540435d89b5c5ecd"), "x" : 1 }
{ "_id" : ObjectId("5961b9e9540435d89b5c5ece"), "x" : 1 }
{ "_id" : ObjectId("5961b9e9540435d89b5c5ecf"), "x" : 1 }
{ "_id" : ObjectId("5961b9e9540435d89b5c5ed0"), "x" : 1 }
> db.test_collection.remove({x:1})
WriteResult({ "nRemoved" : 4 })
> db.test_collection.find()
>
```

**删除有限项**

但也有时候我们只想删除被找到的第一条数据，这个时候可以利用`remove`的第二个参数
```
> for(i=0;i<10;i++)db.test_collection.insert({x:i})
WriteResult({ "nInserted" : 1 })
> db.test_collection.remove({x:{$type:1}},true)
WriteResult({ "nRemoved" : 1 })
> db.test_collection.find()
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a4"), "x" : 1 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a5"), "x" : 2 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a6"), "x" : 3 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a7"), "x" : 4 }
...
```
上例中，第一条，即包含`x:0`的文档被删掉了。




