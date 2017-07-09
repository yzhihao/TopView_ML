# Mongo DB 的介绍与安装
## 简介
Mongodb，分布式文档存储数据库，由`C++` 语言编写，旨在为WEB应用提供可扩展的高性能数据存储解决方案。MongoDB是一个高性能，开源，无模式的文档型数据库，是当前NoSql数据库中比较热门的一种。它在许多场景下可用于替代传统的关系型数据库或键/值存储方式。Mongo使用`C++`开发。

与关系型数据库sql相比，非关系型数据库以键值对作为存储方式（类似于json），结构不像关系型数据库中的字段一样稳定。例如同样是存储字段`班级 姓名 学号`，关系型数据库通过组建一个包含该类字段所有类别的表，在表下的所有数据行都拥有`班级 姓名 学号`，但非关系型数据库仅将其作为一个键值对的一条信息存储在一个文档中，该文档并不需要确保它所包含的每一条信息都拥有`班级 姓名 学号`，可以只有其中一或两个亦或是其它不同的类型。
![](http://www.runoob.com/wp-content/uploads/2013/10/crud-annotated-document.png)
从该图可以更加清楚地看到sql与MongoDB的区别
![](http://www.runoob.com/wp-content/uploads/2013/10/Figure-1-Mapping-Table-to-Collection-1.png)

MongoDB就是一种非关系型数据库，它的优点就在于相比sql，用户的访问速度更快，获取数据的方式更加便携。
## 安装
首先需要在官网地址上下载安装包
[MongoDB下载地址](https://www.mongodb.com/download-center#community)
安装包安装完成后，还需要给MongoDB手动**创建一个数据目录**，用以存贮MongoDB的数据。
```
D:\study\Mongo DB\data\db
```
创建完成后用命令行执行MongoDB目录bin目录下的mongod.exe文件，如果没有问题，就可以看到如下输出信息
```
2015-09-25T15:54:09.212+0800 I CONTROL  Hotfix KB2731284 or later update is not
installed, will zero-out data files
2015-09-25T15:54:09.229+0800 I JOURNAL  [initandlisten] journal dir=c:\data\db\j
ournal
2015-09-25T15:54:09.237+0800 I JOURNAL  [initandlisten] recover : no journal fil
es present, no recovery needed
2015-09-25T15:54:09.290+0800 I JOURNAL  [durability] Durability thread started
2015-09-25T15:54:09.294+0800 I CONTROL  [initandlisten] MongoDB starting : pid=2
488 port=27017 dbpath=c:\data\db 64-bit host=WIN-1VONBJOCE88
2015-09-25T15:54:09.296+0800 I CONTROL  [initandlisten] targetMinOS: Windows 7/W
indows Server 2008 R2
2015-09-25T15:54:09.298+0800 I CONTROL  [initandlisten] db version v3.0.6
```
### 将MongoDB作为Windows服务运行
可以用管理权限打开cmd，然后执行以下命令将MongoDB服务器作为Windows服务运行
```
mongod.exe --bind_ip yourIPadress --logpath "C:\data\dbConf\mongodb.log" --logappend --dbpath "C:\data\db" --port yourPortNumber --serviceName "YourServiceName" --serviceDisplayName "YourServiceName" --install
```
初次设定完成后，我们还要用管理员cmd执行`net start MongoDB`来启动服务
```
> net start MongoDB
MongoDB 服务正在启动 .
MongoDB 服务已经启动成功。
```

mongodb的启动参数与说明

| 参数 | 描述 |
|--------|--------|
|    --bind_ip    |  绑定服务IP，若绑定127.0.0.1，则只能本机访问，不指定默认本地所有IP      |
|--logpath|定MongoDB日志文件，注意是指定文件不是目录|
|--logappend|使用追加的方式写日志|
|--dbpath|指定数据库路径|
|--port|指定服务端口号，默认端口27017|
|--serviceName|指定服务名称|
|--serviceDisplayName|指定服务名称，有多个mongodb服务时执行。|
|--install|指定作为一个Windows服务安装。|

### MongoDB后台管理shell
shell指“提供用户使用界面”的软件。
要进入MongoDB的后台管理，我们需要先打开MongoDB安装目录下的bin目录，然后执行mongo.exe文件，这里的MongoDBShell指的是MongoDB自带的交互式Javascript shell，是用来对MongoDB进行MongoDB进行操作和管理的交互式环境。

当我们进入MongoDB后台后，它默认会链接到test文档（数据库）：
```
> mongo
MongoDB shell version v3.4.6
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.4.6
Welcome to the MongoDB shell.
```
由于它是一个JavaScript shell，我们可以用它进行一些简单的算术运算：
```
> 1+1
2
```
命令`db`用于查看当前操作的文档（数据库）：
```
> db
test
```
然后我们可以插入一些简单的记录，并对其进行查找：
```
将数字 10 插入到 runoob 集合的 x 字段中
> db.runoob.insert({x:10})
WriteResult({ "nInserted" : 1 })

查找runoob里面的键值对
> db.runoob.find()
{ "_id" : ObjectId("595e5d8088408920d1f035c2"), "x" : 10 }
```
