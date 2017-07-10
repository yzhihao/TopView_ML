# MySQLdb

* [MySQLdb的特点](#MySQLdb的特点)
* [MySQLdb.connect](#MySQLdb.connect)
* [connect](#connect)
* [关于fetch](#关于fetch)
* [记得关闭](#记得关闭)


## MySQLdb的特点
- MySQLdb和JDBC有不一样的地方就是**事务处理commit和rollback**

- #### commit
	- 所有的语句执行后不会马上生效，直到你commit之后
<br/>
- #### rollback
	- 当你执行事务遇到异常，可以用rollback回到执行该事务之前的状态



## MySQLdb.connect
#### MySQLdb.connect.(host= ,user=,passwd=,db=,charset=)
- host:数据库主机名.默认是用本地主机
- user:数据库登陆名.默认是当前用户
- passwd:数据库登陆的密码.默认为空
- db:要使用的数据库名.没有默认值
- port:MySQL服务使用的TCP端口.默认是3306
- charset:数据库编码


```python
In[2]:import MySQLdb
In[3]:connect = MySQLdb.connect(host='localhost',port=3306,user = 'root',passwd ='1.2.3.',db = 'TESTDB')

```

## connect
#### connect.cursor()  游标

- `connect.cursor()`用于执行命令

#### 关于`execute`和`executemany`

- `connect.cursor().execute(SQL，param)`执行sql语句

- `connect.cursor().executemany(SQL，param)`执行多条sql语句

	- 在使用executemany时，变量都用%s占位，param是一个装有数据的元组元组

	- 在执行多次操作时executemany比用execute循环操作快的多

	- 在执行update/insert/delete操作后数据库并没有马上更新，还需要`connect.commit()`数据库内容才会更新

	- 同理在执行查询的时候，也要cursor().fetchall()才可以返回数据

	- `connect.cursor().execute(SQL)`也可以创建一个新表



``` python
In[4]: db.execute("INSERT INTO EMPLOYEE VALUE ('ChokJohn', 'Lee', 19, 'M', 2000)")# 插入
Out[4]: 1L
In[5]: conn.commit()

In[6]: db.execute('select * from EMPLOYEE')# 查询
Out[6]: 1L
In[7]: db.fetchall()
Out[7]: (('ChokJohn', 'Lee', 19L, 'M', 2000.0),)


In[8]: db.execute("Update EMPLOYEE SET INCOME = 666 where AGE = 19")# 更新
Out[8]: 1L

In[9]: db.execute('select * from EMPLOYEE')# 查询
In[10]: db.fetchall()
Out[10]: ('ChokJohn', 'Lee', 19L, 'M', 666.0)
```

## 关于fetch

- cursor.fetchone()     查看查询的第一条记录，一次一条，指针向下移动

- cursor.fetchmany(X)  查看X条记录，若不输入X，则只默认查看一条，指针向下移动

- cursor.fetchall()      一次性查看全部，指针移到最后

- cursor.scroll(self, value, mode=):移动指针到某一行.
	- mode='relative',则表示从当前所在位置**向后**移动value条

	- mode='absolute',则表示从结果集的第一条开始**向后**移动value条.

	- scroll只移动指针不返回数据，故要获取数据还得用上面三个fetch的其中一个

## 记得关闭

- 若不需要连接数据库时应要关闭，包括cursor

- 关闭只需调用cursor.close()和connection.close()
