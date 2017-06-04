Grant命令：
在mysql用grant语句可以建立一个只连接特定数据库的账户以提高数据库的安全性
例：
> `grant select,insert,delete,update on database.* to test@localhost identified by 'test';`

select到update设置了账户的操作权限，databas.table 是指定账户可以操作的数据库以及相关表，支持通配符*，test@localhost指名为test的账户仅能从localhost的位置登录，identified by 'test'则为该账户添加密码test，grant的好处在于当指定名称的账户不存在时可以创建该账户。
