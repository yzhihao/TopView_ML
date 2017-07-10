# MongoDB安全

MongoDB在默认情况下是不开启权限认证的，所以我们可以直接在cmd使用“mongo”命令打开客户端。要开启安全认证，MongoDB提供了我们两个方法：
1. auth
2. keyfile

## auth

##### 添加配置文件

要使用auth方法给MongoDB添加权限认证，我们首先需要设置MongoDB的配置文件"mongod.config"(Linux中的后缀名是“conf”)，并在其中加入一些MongoDB的启动配置：
```
port=27017
dbpath = ..\..\data\db
logpath = ..\..\dbConf\mongodb.log
fork = true 
```
port代表启动的端口，dbpath代表存储数据的目录，logpath代表日志文件的目录，fork仅在Linux系统下有效，表明作为一个后台进程启动。
创建完成后，我们需要在mongod中将配置文件添加进去：
```
mongod -f ..\..\data\dbConf\mongod.config
```
##### 开启权限认证

在配置文件“mongod.config”下添加参数“auth=true”
```
port=27017
dbpath = ..\..\data\db
logpath = ..\..\dbConf\mongodb.log
auth = true
```
这样子便开启了MongoDB的权限认证。

然后我们需要重新启动一下MongoDB的服务：
```
> db.shutdownServer()
> exit

>mongod -f ..\..\data\dbConf\mongod.config
#如果要使用net start MongoDB的话，需要按照之前的设置重新配置一下windows服务

#用另外一个命令行启动mongo，因为使用mongod的命令行正作为服务运行中
C:\Users\peter>mongo
MongoDB shell version v3.4.6
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.4.6
```
启动之后，我们可以在MongoDB的日志文件中看一下权限的启动情况

##### 创建用户

我们使用createUser语法进行用户创建，创建语法格式如下：
```
db.createUser(
{
user:"username",
pwd:"password",
roles:[{role:"rolename",db:"databasename"},...]
}
)
```
参数信息如下表：

| 参数 | 功能 |
|--------|--------|
|    username    |用户名        |
|password|密码|
|roles|角色，表示该用户的权限|
|rolename|权限类型，可以自行定义，也可以使用内建的权限名|
|databasename|权限对应的数据库|

常用的内建角色如下表：

|角色大类| 内建权限名 | 功能 |
|---|--------|--------|
|数据库用户角色（Database User Roles）|read|授予User只读数据的权限|
||readWrite|授予User读写数据的权限|
|数据库管理角色（Database Administration Roles）|dbAdmin|在当前dB中执行管理操作|
||dbOwner|在当前DB中执行任意操作|
||userAdmin|在当前DB中管理User|
|备份和还原角色（Backup and Restoration Roles）|backup||
||restore||
|跨库角色（All-Database Roles）|readAnyDatabase|授予在所有数据库上读取数据的权限|
||readWriteAnyDatabase|授予在所有数据库上读写数据的权限|
||userAdminAnyDatabase|授予在所有数据库上管理User的权限|
||dbAdminAnyDatabase|授予管理所有数据库的权限|
|集群管理角色（Cluster Administration Roles）|clusterAdmin|授予管理集群的最高权限|
||clusterManager|授予管理和监控集群的权限（A user with this role can access the config and local databases, which are used in sharding and replication, respectively.）|
||clusterMonitor|授予监控集群的权限，对监控工具具有readonly的权限|
||hostManager|管理Server|
更多内建角色可参考文档[MongoDB的内建角色](http://docs.mongoing.com/manual-zh/reference/built-in-roles.html)

示例：
```
> db.createUser({user:"admin",pwd:"password",roles:[{role:"root",db:"admin"}]})
Successfully added user: {
        "user" : "admin",
        "roles" : [
                {
                        "role" : "root",
                        "db" : "admin"
                }
        ]
}
```
创建完成后，就需要使用用户名与密码来登录数据库：
```
mongo -u username -p password
```
否则即使登录成功，也无法拥有操作数据库的权限。

这里要注意的一点是，我们在示例中创建的用户拥有的是对数据库“admin”进行操作的权限，但是MongoDB在我们登陆时往往会让我们**默认登录到数据库“test”**，这个时候会报错：
```
2017-07-10T16:52:30.844+0800 E QUERY    [thread1] Error: Authentication failed. :
DB.prototype._authOrThrow@src/mongo/shell/db.js:1461:20
@(auth):6:1
@(auth):1:2
exception: login failed
```
要解决这个问题，我们需要在登陆时加入要登陆的数据库地址（[db address]），如上例，我们登陆时需要这样写：
```
mongo -u admin -p password admin
#这里的第二个admin就是数据库的地址（名字）

MongoDB shell version v3.4.6
connecting to: mongodb://127.0.0.1:27017/admin
MongoDB server version: 3.4.6
#显示登陆成功
```

##### 角色创建

前面说到，除了MongoDB自带的内建角色之外，我们还可以创建自定义的角色，只需要通过命令`db.createRole()`，它使用的格式如下：
```
>db.createRole(
>{
_id:"idname" #id
role:"rolename" #角色名
db:"databasename" #角色所在数据库
privileges:[ #权限细分
	{resource:{db:"databasename1",collection:"collectionname"},
    actions:["action1,"action2"...]},
    {resource:{db:"databasename2",collection:"collectionname"},
    actions:["action1,"action2"...]}
    ...
], 
#resource：表示一份数据库的操作权限，collection表示对应的集合（为空表示所有集合），actions表示允许用户进行的操作，例如“find”，“insert”等等，就是操作对应的命令的名字。

roles:[role:{"rolename"},db:"databasename"] 
#角色，使用方式同创建用户的角色，不同的是此处可以为空，表示无角色
}
)
```
自定义角色允许我们对一个角色的权限进行细分。




