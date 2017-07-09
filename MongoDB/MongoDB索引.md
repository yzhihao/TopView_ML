# MongoDB索引

## 简介

为了加强数据库的查询性能，MongoDB提供了索引功能。
我们可以使用命令`getINdexes()`来查看一个集合中的索引
```
> db.test_collection.getIndexes()
[
        {
                "v" : 2,
                "key" : {
                        "_id" : 1
                },
                "name" : "_id_",
                "ns" : "zyzy.test_collection"
        }
]
> db.test_collection.getIndexes()
[
        {
                "v" : 2,
                "key" : {
                        "_id" : 1
                },
                "name" : "_id_",
                "ns" : "zyzy.test_collection"
        },
        {
                "v" : 2,
                "key" : {
                        "y" : -1
                },
                "name" : "y_-1",
                "ns" : "zyzy.test_collection"
        }
]
```
可以发现索引只有"_id"。

我们可以使用`ensureIndex()`来为集合创建索引，它的使用方式类似于`insert()`，但不同的是，它的值只为“1”（升序）或“-1”（降序）：
```
> db.test_collection.ensureIndex({y:-1})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
```

然后我们在利用索引进行查找时，开销会比没有索引更低：
```
> db.test_collection.find().sort({y:1})
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056ac"), "x" : 9 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056ab"), "x" : 8 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056aa"), "x" : 7 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a9"), "x" : 6 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a8"), "x" : 5 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a7"), "x" : 4 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a6"), "x" : 3 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a5"), "x" : 2 }
{ "_id" : ObjectId("5961e9c7e12ea99cbdc056a4"), "x" : 1 }
```
可以发现索引不作为键值出现在文档中。

一般来说，索引要在创建文档之前就设置好，如果集合里面已经有大量数据，这个时候再创建索引对数据库的开销会非常大。

## 索引分类
MongoDB的索引种类有很多：
1. _id索引
2. 单键索引
3. 多键索引
4. 复合索引
5. 过期索引
6. 全文索引
7. 地理位置索引

### _id索引

在创建大部分集合的时候，MongoDB会自动为每一个集合添加"_id"索引，每个文档都具有一个本集合下唯一的“_id”。

### 单键索引

单键索引就是在简介中创建的那类型简单索引，它不会在集合生成的时候自动创建，而是需要我们手动创建。当我们创建的集合索引和已有的索引重复的时候会报错。

当我们创建的文档中的索引与已有的文档中的索引重叠时，已有的文档会被新的文档覆盖。

单键索引创建的时候，既可以把已有的键值对作为索引，也可以把不存在的键作为索引：
```
> db.test_collection.insert({x:1})
WriteResult({ "nInserted" : 1 })
> db.test_collection.insert({x:2})
WriteResult({ "nInserted" : 1 })
> db.test_collection.ensureIndex({x:1})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
> db.test_collection.find()
{ "_id" : ObjectId("5961f2c0e12ea99cbdc056d4"), "x" : 1 }
{ "_id" : ObjectId("5961f2c3e12ea99cbdc056d5"), "x" : 2 }
#文档中存在“x”的值

> db.test_collection.ensureIndex({y:1})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 2,
        "numIndexesAfter" : 3,
        "ok" : 1
}
> db.test_collection.find().sort({y:-1})
{ "_id" : ObjectId("5961f2c3e12ea99cbdc056d5"), "x" : 2 }
{ "_id" : ObjectId("5961f2c0e12ea99cbdc056d4"), "x" : 1 }
#文档中不存在“y”的值，但索引还是生效了
```

### 多键索引

多键索引的创建方式与单键索引相同，它与单键索引不同的地方在于它的值，是以数组的形式存在的：
```
#将x的值设置为索引
> db.test_collection.ensureIndex({x:1})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}

#创建一条单键索引
> db.test_collection.insert({x:1})
WriteResult({ "nInserted" : 1 })

#创建一条多键索引
> db.test_collection.insert({x:[1,2,3,4,5]})
WriteResult({ "nInserted" : 1 })
```
多键索引在被作单个值为条件查询的时候，它的值的数组内部的每一个值之间可以被视为与其它值时逻辑或的关系：
```
> db.test_collection.find({x:1})
{ "_id" : ObjectId("5961f382e12ea99cbdc056d6"), "x" : 1 }
{ "_id" : ObjectId("5961f3cbe12ea99cbdc056d8"), "x" : [ 1, 2, 3, 4, 5 ] }
```
但以数组作为条件查询时是不行的
```
> db.test_collection.find({x:[1]})
#没有结果

> db.test_collection.find({x:[1,2,3,4,5]})
{ "_id" : ObjectId("5961f3cbe12ea99cbdc056d8"), "x" : [ 1, 2, 3, 4, 5 ] }
```

### 复合索引

复合索引是指在设置集合的索引的时候插入多条索引键值对，例如，我们希望在使用`find()`的时候同时将x与y作为查询条件，那么就可以设置复合索引：
```
> db.test_collection.ensureIndex({x:1,y:1})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 2,
        "numIndexesAfter" : 3,
        "ok" : 1
}
```

## 过期索引

过期索引用于标记数据，让数据在一定时间之后自动失效，例如网站内的用户登录信息，在一段时间不登陆之后就需要重新输入登录信息。

创建的方式类似于其它索引，但不同的是，它需要使用`ensureIndex({KEY:VALUE},{expireAfterSeconds:<value>})`的第二个参数，`{expireAfterSeconds:<value>}`中`<value>`的值为过期需要经过的秒数：
```
> db.test_collection.ensureIndex({time:1},{expireAfterSeconds:10})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 3,
        "numIndexesAfter" : 4,
        "ok" : 1
}
```
插入一条数据,方法`new Date()`会自动获取当前时间作为ISODate值，插入的数据若是要使用过期索引的效果，那么它必须得是**ISODate或者ISODate数组**，否则将不能被顺利删除（时间戳也无法使用过期索引的效果）。
```
> db.test_collection.insert({x:1,time:new Date()})
WriteResult({ "nInserted" : 1 })
> db.test_collection.find()
{ "_id" : ObjectId("5961f7f2e12ea99cbdc056da"), "x" : 1, "time" : ISODate("2017-07-09T09:31:30.168Z") }
#10秒后该数据就被自动删除了
```
如果，插入的值是ISODate数组，那么就会以数组中**最小的时间值**为基准来进行删除操作：
```
{ "_id" : ObjectId("5961f9ede12ea99cbdc056db"), "x" : 1, "time" : [ ISODate("2017-07-09T09:39:57.094Z"), ISODate("2017-07-09T09:50:30.168Z") ] }
```
例如上面这条，会以“time”中第一个ISODate的时间为基准。

另外我们还需要注意：
* 过期索引不能是复合索引
* 删除时间并不精确（因为删除过程是由后台程序每60s运行一次，而且删除操作本身也需要时间，也就是说，即使我们设定的时间间隔很小，如果是少量的数据，也只会是在60s后被删除）

### 全文索引

##### 创建全文索引
全文索引，顾名思义，是对整个对应的数据中的值进行查询的索引，要创建一个全文索引，我们使用`ensureIndex()`的另外一个参数`"text"`：
```
> db.test_collection.ensureIndex({string:"text"})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 4,
        "numIndexesAfter" : 5,
        "ok" : 1
}
```
它同样支持创建复合索引：
```
> db.test_collection.ensureIndex({article:"text",author:"text"})
{
        "createdCollectionAutomatically" : true,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
```
若是需要在很多不同关键字对应的值里面查找，则需要使用特殊操作符`$**`:
```
> db.test_collection.ensureIndex({"$**":"text"})
{
        "createdCollectionAutomatically" : true,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
```
另外，在MongoDB中，每个集合只允许创建一个全文索引。

##### 查询全文索引
假设我们已经创建了以x为关键字的全文索引，然后又创建了如下几条数据。
```
> db.test_collection.find()
{ "_id" : ObjectId("5961fddbe12ea99cbdc056dc"), "x" : "aa bb cc dd ee ff gg" }
{ "_id" : ObjectId("5961fdeae12ea99cbdc056dd"), "x" : "aavvb cc hh kk ff gg" }
{ "_id" : ObjectId("5961fdfde12ea99cbdc056de"), "x" : "aa ff g g efd nn" }
```

最简单的查询方式是通过操作符`{$text:{$search:<value>}}`:
```
> db.test_collection.find({$text:{$search:"cc"}})
{ "_id" : ObjectId("5961fddbe12ea99cbdc056dc"), "x" : "aa bb cc dd ee ff gg" }
{ "_id" : ObjectId("5961fdeae12ea99cbdc056dd"), "x" : "aavvb cc hh kk ff gg" }
```

**OR查找**

当我们需要查找多个值的时候，可以直接在查找条件中用空格将不同的查找词隔开，例如：
```
> db.test_collection.find({$text:{$search:"aa bb cc"}})
{ "_id" : ObjectId("5961fdeae12ea99cbdc056dd"), "x" : "aavvb cc hh kk ff gg" }
{ "_id" : ObjectId("5961fddbe12ea99cbdc056dc"), "x" : "aa bb cc dd ee ff gg" }
{ "_id" : ObjectId("5961fdfde12ea99cbdc056de"), "x" : "aa ff g g efd nn" }
```
可以发现，包含"aa"或"bb"或"cc"的都在查找结果中出现

**排除查找**

若是想指定不查找的字段，我们可以在这个字段前用“-”做前缀，这样就不会查找有这个字段的文档：
```
> db.test_collection.find({$text:{$search:"aa bb -cc"}})
{ "_id" : ObjectId("5961fdfde12ea99cbdc056de"), "x" : "aa ff g g efd nn" }
```
发现，包含“cc”的文档没有出现在查找结果中。

**AND查找**

若是要查找以“和”关系相关联的文档，例如既包含“aa”又包含“bb”，则需要通过内部加引号来表示，但是为了防止歧义，我们会在内部的引号前面加上反斜杠以表示转义：
```
> db.test_collection.find({$text:{$search:"aa bb \"cc\""}})
{ "_id" : ObjectId("5961fdeae12ea99cbdc056dd"), "x" : "aavvb cc hh kk ff gg" }
{ "_id" : ObjectId("5961fddbe12ea99cbdc056dc"), "x" : "aa bb cc dd ee ff gg" }
```
发现找的是“x”中包含“aa”和“cc”或者“bb”和“cc”的文档。

##### 全文索引相似度查询

相似度表示文档与查找信息之间的相似度。在`find()`添加参数`{<score>:{$meta:"textScore"}}`来获取文档与我们定义的搜索条件的相似度,其中`<score>`内可以是自定义的任意字符串，一般用“score”：
```
> db.test_collection.find()
{ "_id" : ObjectId("5961fddbe12ea99cbdc056dc"), "x" : "aa bb cc dd ee ff gg" }
{ "_id" : ObjectId("5961fdeae12ea99cbdc056dd"), "x" : "aavvb cc hh kk ff gg" }
{ "_id" : ObjectId("5961fdfde12ea99cbdc056de"), "x" : "aa ff g g efd nn" }
{ "_id" : ObjectId("596230e62c1607a4c93adbd9"), "x" : "aa bb" }

> db.test_collection.find({$text:{$search:"aa bb"}},{score:{$meta:"textScore"}})
{ "_id" : ObjectId("5961fddbe12ea99cbdc056dc"), "x" : "aa bb cc dd ee ff gg", "score" : 1.1428571428571428 }
{ "_id" : ObjectId("5961fdfde12ea99cbdc056de"), "x" : "aa ff g g efd nn", "score" : 0.5833333333333334 }
{ "_id" : ObjectId("596230e62c1607a4c93adbd9"), "x" : "aa bb", "score" : 1.5 }
```
查找结果多出了一个“score”项用于表示相似度，相似度越高，则表示文档与查找条件中的字段越相似。

我们可以加上`sort()`方法来实现相似度的排序：
```
> db.test_collection.find({$text:{$search:"aa bb"}},{score:{$meta:"textScore"}}).sort({score:{$meta:"textScore"}})
{ "_id" : ObjectId("596230e62c1607a4c93adbd9"), "x" : "aa bb", "score" : 1.5 }
{ "_id" : ObjectId("5961fddbe12ea99cbdc056dc"), "x" : "aa bb cc dd ee ff gg", "score" : 1.1428571428571428 }
{ "_id" : ObjectId("5961fdfde12ea99cbdc056de"), "x" : "aa ff g g efd nn", "score" : 0.5833333333333334 }
```
可以发现，相似度高的将会排在前面。

##### 全文索引的限制

**只能有一个$text查询**

在使用全文索引查询的时候，`find()`只能接收一个`$text`查询符。

**操作符$text不能出现在nor查询中**

`$nor`查询是指排除查询，即查询不包含`$nor`后面的值的数据：
```
> db.test_collection.find({$nor:[{x:"aa bb"}]})
{ "_id" : ObjectId("5961fddbe12ea99cbdc056dc"), "x" : "aa bb cc dd ee ff gg" }
{ "_id" : ObjectId("5961fdeae12ea99cbdc056dd"), "x" : "aavvb cc hh kk ff gg" }
{ "_id" : ObjectId("5961fdfde12ea99cbdc056de"), "x" : "aa ff g g efd nn" }
```
发现“x”的值为字符串“aa bb”的文档没有出现在查询结果中。

**包含了$text的查询中，hint无法起作用**

`hint()`是用来给查询增加强制索引，用以增强查找性能的方法，我们常常先用**explain()**方法来查看一次查找的详细信息:
```
> db.test_collection.find().explain()
{
        "queryPlanner" : {
                "plannerVersion" : 1,
                "namespace" : "zyzy.test_collection",
                "indexFilterSet" : false,
                "parsedQuery" : {

                },
                "winningPlan" : {
                        "stage" : "COLLSCAN",
                        "direction" : "forward"
                },
                "rejectedPlans" : [ ]
        },
        "serverInfo" : {
                "host" : "iPhone",
                "port" : 27017,
                "version" : "3.4.6",
                "gitVersion" : "c55eb86ef46ee7aede3b1e2a5d184a7df4bfb5b5"
        },
        "ok" : 1
}
```

而**hint**就是能够增强索引效果的查找方式：
```
> db.test_collection.ensureIndex({y:1})
{
        "createdCollectionAutomatically" : true,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
> for(i=0;i<100;i++)db.test_collection.insert({x:i,y:i})
WriteResult({ "nInserted" : 1 })
#添加100条有y索引的文档

> db.test_collection.find().hint({y:1}).explain()
{
...
                "winningPlan" : {
                        "stage" : "FETCH",
                        "inputStage" : {
                                "stage" : "IXSCAN",
                                "keyPattern" : {
                                        "y" : 1
                                },
                                "indexName" : "y_1",
                                "isMultiKey" : false,
                                "multiKeyPaths" : {
                                        "y" : [ ]
                                },
                                "isUnique" : false,
                                "isSparse" : false,
                                "isPartial" : false,
                                "indexVersion" : 2,
                                "direction" : "forward",
                                "indexBounds" : {
                                        "y" : [
                                                "[MinKey, MaxKey]"
                                        ]
...
}
```
可以发现，查找信息中“y”被设定为强制使用的查找索引。

**老版本的MongoDB全文索引暂不支持中文**
```
> db.test_collection.insertMany(
... [
... {x:"你好 很好 不错"},
... {x:"你好 不错 很不好"}
... ]
... )
{
        "acknowledged" : true,
        "insertedIds" : [
                ObjectId("596239822c1607a4c93adc3e"),
                ObjectId("596239822c1607a4c93adc3f")
        ]
}
> db.test_collection.find({$text:{$search:"你好"}})
{ "_id" : ObjectId("596239822c1607a4c93adc3e"), "x" : "你好 很好 不错" }
{ "_id" : ObjectId("596239822c1607a4c93adc3f"), "x" : "你好 不错 很不好" }
```
目前看来，新版本的MongoDB的全文索引是支持中文的。

## 索引属性
创建索引的方法`ensueIndex()`接收两个参数，第一个是索引，第二个是索引的属性。
除了过期索引中提到的“是否定时删除”的索引属性，索引还具有一些其他的属性：
1. 名字
2. 唯一性
3. 稀疏性

### 名字
name属性用于指定索引的名字，当我们不指定name属性的时候，MongoDB会自动给创建的索引添加名字：
```
> db.test_collection.ensureIndex({x:1,y:1})
{
        "createdCollectionAutomatically" : true,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
> db.test_collection.getIndexes()
[
        {
                "v" : 2,
                "key" : {
                        "_id" : 1
                },
                "name" : "_id_",
                "ns" : "zyzy.test_collection"
        },
        {
                "v" : 2,
                "key" : {
                        "x" : 1,
                        "y" : 1
                },
                "name" : "x_1_y_1",
                "ns" : "zyzy.test_collection"
        }
]
```
“name”项里面便是MongoDB给索引添加的名字。

要修改索引的名字，我们在创建方法的后面添加name参数：
```
> db.test_collection.ensureIndex({x:1,y:1},{name:"normal_index"})
{
        "createdCollectionAutomatically" : true,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
> db.test_collection.getIndexes()
[
        {
                "v" : 2,
                "key" : {
                        "_id" : 1
                },
                "name" : "_id_",
                "ns" : "zyzy.test_collection"
        },
        {
                "v" : 2,
                "key" : {
                        "x" : 1,
                        "y" : 1
                },
                "name" : "normal_index",
                "ns" : "zyzy.test_collection"
        }
]
```

在**删除索引**的时候，我们也可以借用索引的名字来进行删除：
```
> db.test_collection.dropIndex("normal_index")
{ "nIndexesWas" : 2, "ok" : 1 }
> db.test_collection.getIndexes()
[
        {
                "v" : 2,
                "key" : {
                        "_id" : 1
                },
                "name" : "_id_",
                "ns" : "zyzy.test_collection"
        }
]
```
当然也可以**直接将索引作为参数**放入删除方法中。

### 唯一性

`unique`参数供我们确定索引的唯一性，当其值为“true”时，索引是唯一的：
```
> db.test_collection.ensureIndex({x:1},{name:"normal_index",unique:true})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
```
这个时候如果我们插入索引重复的文档，会发生报错。

### 稀疏性

在上面说到，如果我们创建的文档中**不包含被设定为索引的字段，那么MongoDB会自动为其加上一个隐藏的索引**，如果我们不希望MongoDB这么做的话，就在`ensueIndex()`方法后面给`sparse`参数设定为“true”:
```
> db.test_collection.ensureIndex({x:1},{sparse:true})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
```

要注意的是，如果我们指定了`sparse`值为“ture”，那么在使用存在性查找（`$exists`）的时候，如果是以该索引为查找条件，并且用hint强制指定了的话，是查找不到结果的。


