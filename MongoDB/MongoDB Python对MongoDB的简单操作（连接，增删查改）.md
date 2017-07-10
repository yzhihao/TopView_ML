# MongoDB Python对MongoDB的简单操作（连接，增删查改）

## 安装pymongo

要通过Pyhton使用MongoDB，我们首先需要下载Python用于操作MongoDB的库**pymongo**
```
pip install pymongo
```

然后就可以在python中导入这个库了，不过通常我们只是导入它的驱动：
```python
from pymongo import MongoClient
```

## 连接MongoDB

导入之后，我们通过下面一段代码获取MongoDB的操作对象：
```python
client=MongoClient('127.0.0.1',27017) #建立和数据库的连接，前者是MongoDB服务所在的地址，后者是对应的端口号

db_auth=client.admin #指定使用哪个数据库的账号，这里用的是数据库admin
db_auth.authenticate("admin","password") #权限认证，第一个参数是账号，第二个参数是密码
#若连接的数据库不需要账号，上述两条可以省略。

db_name="test" #要连接的数据库的名字
db = client[db_name] #获得数据库操作对象，也可以写作`client.db_name`
collection_useraction=db['useraction'] #获得数据库的集合操作对象，集合名为“useraction”
```
获得集合操作对象之后，我们就可以通过这个集合操作对象对数据库的集合进行操作，以上例为例，就是对名为MongoDB的数据库“test”中名为“useraction”的集合进行操作。

## 操作数据库

### 插入数据

往集合插入数据的方法有两种，分别是`insert()`和`save()`，对应的就是MongoDB Shell里面的`insert()`和`save（）`。

它们之间的区别就是，`insert()`在插入和原来信息重复的数据对象的时候，会报错，而`save()`则会将原来的数据对象进行更新。当然，这里的重复指的是唯一索引的重复，类似于“_id”的重复。
```python
collection_useraction.insert({"x":1})
```
用shell查看，发现插入成功
```
> db.useraction.find()
{ "_id" : ObjectId("59635e3a867e573b0c7c8d71"), "x" : 1 }
```
```python
collection_useraction.insert({"x":1,"_id":1})

>...
pymongo.errors.DuplicateKeyError: E11000 duplicate key error collection: test.useraction index: _id_ dup key: { : 1 }

#在已有"_id"为1的数据的时候插入一条上述数据，发现编译器报错
```
在python中的`insertMany()`方法语法为`insert_many()`

可以发现，python中对MongoDB插入数据的方式与MongoDB Shell没有太多区别。

### 更新数据

更新数据使用`update()`方法，语法格式如下：
```python
update(criteria, objNew, upsert, mult)
```
* criteria: 需要被更新的条件表达式
* objNew: 更新表达式
* upsert: 如目标记录不存在，是否插入新文档。
* multi: 是否更新多个文档。

示例：
```python
collection_useraction.update({"x":{"$lt":2}},{"$set":{"y":2}},upsert=True)
```
发现操作符的使用方式也与shell没有区别。

### 删除数据

#### 删除集合

要删除一个集合，有多种方法，方法一是用:
```python
db.collection_name.drop()
```
这个地方的`collection_name`指的是这个集合在MongoDB数据库里面的名字，例如我们上面的例子，它的名字就是“useraction”，而不是“collection_useraction”。

另外一个方法是用：
```python
collection_operator.drop()
```
`collection_operator`指的就是python中该集合的操作对象，如上例，就是“collection_useraction”，而不是集合名字“useraction”

#### 删除文档

删除文档使用`remove()`方法，同样有两种方式调用，与上文中删除集合类似，所以这里只讲一种方法：
```python
collection_operator.remove(self, spec_or_id=None, multi=True, **kwargs)
```
* 第一个参数表示要删除的文档的搜索条件或者该文档的id，默认为None。
* multi表示是否删除多个，为False的时候一次只删除一个。
* 当括号为空的时候会删除集合内所有文档，这一点与shell不同。

```python
collection_useraction.remove({"x":1})
```
表示删除所有集合中“x”值为1的文档。

### 查询

我们先假设我们在集合中插入了100条信息
```python
i=0
while i<100:
    collection_useraction.insert({"x":i,"y":100-i})
    i+=1
```

搜索用的方法同样也是`find()`，使用方式也与shell相同，当我们需要查找并遍历查找结果的时候，可以用这样的方式:
```python
for u in collection_useraction.find({"x":{"$exists":True}}):
    print u
    
>{u'y': 100, u'x': 0, u'_id': ObjectId('59636678867e5717981f18c1')}
{u'y': 99, u'x': 1, u'_id': ObjectId('59636678867e5717981f18c2')}
{u'y': 98, u'x': 2, u'_id': ObjectId('59636678867e5717981f18c3')}
...
```
这是因为语句`collection_useraction.find({"x":{"$exists":True}})`返回了一个可供迭代的对象，用`type()`方法可以看到这个对象的类型:
```python
cursor=collection_useraction.find({"x":{"$exists":True}})
print type(cursor)

><class 'pymongo.cursor.Cursor'>
```

这个对象同时还支持我们直接用索引访问:
```python
print cursor[10]
>{u'y': 90, u'x': 10, u'_id': ObjectId('59636678867e5717981f18cb')}
```
并且还支持一些shell的方法：
```python
print cursor.explain()
>{u'executionStats': {u'executionTimeMillis': 0, u'nReturned': 100, u'totalKeysExamined': 0, u'allPlansExecution': [], u'executionSuccess': True, u'executionStages': {u'needYield': 0, u'direction': u'forward', u'saveState': 0, u'restoreState': 0, u'isEOF': 1, u'docsExamined': 100, u'nReturned': 100, u'needTime': 1, u'filter': {u'x': {u'$exists': True}}, u'executionTimeMillisEstimate': 0, u'invalidates': 0, u'works': 102, u'advanced': 100, u'stage': u'COLLSCAN'}, u'totalDocsExamined': 100}, u'queryPlanner': {u'parsedQuery': {u'x': {u'$exists': True}}, u'rejectedPlans': [], u'namespace': u'test.useraction', u'winningPlan': {u'filter': {u'x': {u'$exists': True}}, u'direction': u'forward', u'stage': u'COLLSCAN'}, u'indexFilterSet': False, u'plannerVersion': 1}, u'ok': 1.0, u'serverInfo': {u'host': u'iPhone', u'version': u'3.4.6', u'port': 27017, u'gitVersion': u'c55eb86ef46ee7aede3b1e2a5d184a7df4bfb5b5'}}
```
并且可以对它进行深拷贝：
```python
gg=cursor.clone()
aa=cursor
print aa == cursor
print gg == cursor

>True
False
```

若是想一次只查找一条信息，可以使用方法`find_one()`。

#### 查询特定键

当我们只想查询指定的关键字的值的时候，就需要用到`find()`的第二个参数“projection”:
```python
cursor=collection_useraction.find({},{"x":1})
print cursor[10]
>{u'x': 10, u'_id': ObjectId('59636678867e5717981f18cb')}

cursor=collection_useraction.find({},projection={"x":1})
print cursor[10]
>{u'x': 10, u'_id': ObjectId('59636678867e5717981f18cb')}
```

#### 排序

排序用的同样是方法`sort()`，但是使用方式与shell略有不同：
```python
useraction.find().sort([("KEY",<sort_method>)])
```

"KEY"指作为排序基准的关键字的名字，`<sort_method>`则表示排序的方法，有两个选项，分别是`pymongo.ASCENDING`（升序，可用1代替）和`pymongo.DESCENDING`（降序，可用-1代替）对象，示例：
```python
for u in collection_useraction.find().sort([("x",pymongo.DESCENDING)]):
    print u
>{u'y': 1, u'x': 99, u'_id': ObjectId('59636679867e5717981f1924')}
{u'y': 2, u'x': 98, u'_id': ObjectId('59636679867e5717981f1923')}
{u'y': 3, u'x': 97, u'_id': ObjectId('59636679867e5717981f1922')}
{u'y': 4, u'x': 96, u'_id': ObjectId('59636679867e5717981f1921')}
...
```

也可以直接使用`find()`方法中的`sort`参数：
```python
for u in collection_useraction.find(sort=[("x",pymongo.DESCENDING)]):
    print u
```

#### 切片

在shell中我们使用`skip()`与`limit()`方法来对查询结果进行切片，python中一样可以:
```python
for u in collection_useraction.find().skip(90).limit(3):
    print u
>{u'y': 10, u'x': 90, u'_id': ObjectId('59636679867e5717981f191b')}
{u'y': 9, u'x': 91, u'_id': ObjectId('59636679867e5717981f191c')}
{u'y': 8, u'x': 92, u'_id': ObjectId('59636679867e5717981f191d')}
```
skip与limit同样支持参数写法。

不及如此，我们还可以对查询结果使用**索引切片**：
```python
for u in collection_useraction.find()[2:5]:
    print u
>{u'y': 98, u'x': 2, u'_id': ObjectId('59636678867e5717981f18c3')}
{u'y': 97, u'x': 3, u'_id': ObjectId('59636678867e5717981f18c4')}
{u'y': 96, u'x': 4, u'_id': ObjectId('59636678867e5717981f18c5')}
```

#### 正则查询

在查询文本的时候，除了MongoDB原有的文本查询格式，我们还可以使用正则表达式：
```python
pattern=re.compile(r"aa*")
for u in collection_useraction.find({"x":pattern}):
    print u
>{u'x': u'aa bb cc dd', u'_id': ObjectId('596377bd687384c0a1b9d5e9')}

#下面这个查询方式显然shell中也是支持的
for u in collection_useraction.find({"x":{"$regex":r"aa b{2} c{1,3} dd"}}):
    print u
>{u'x': u'aa bb cc dd', u'_id': ObjectId('596377bd687384c0a1b9d5e9')}
```

