# Python-MySQL

* [安装MySQL(Mac安装教程)](#安装MySQLMac安装教程)
* [配置MySQL](#配置MySQL)
* [安装MySQL Workbench](#安装MySQLWorkbench)
* [安装MySQLdb库(python2.7)](#安装MySQLdb库python2.7)
* [安装pymysql(Python3.X)](#安装pymysqlPython3.X)
* [shell脚本操作MySQL](#shell脚本操作MySQL)


## 安装MySQL(Mac安装教程)

- 去[官网](https://www.mysql.com/)直接下载 MySQL Community Server、MySQL Workbench
	- MySQL Workbench是可视化操作工具

- 安装时打开MySQL Community Server，一直点下去就可以了
	- 要注意的是MySQl 5.7版本后数据库的默认密码是随机给的，Mac系统下在右侧通知处会有一条写着MySQL初始密码的通知

- 安装完之后在系统偏好设置那里会有MySQL，点击启用

## 配置MySQL
#### 在终端运行以下命令：

- `mysql = /usr/local/mysql/bin/mysql`


- `mysqladmin = /usr/local/mysql/bin/mysqladmin`
	- 这样就不用进入MySQL目录就可以执行剩下的命令


- `mysqladmin -u root -p password newpassword`
	- newpassword是你要设置的新密码
	- 执行以上命令时需要输入初始密码(就是通知栏里那个密码)


- 然后在终端输入以下内容，就可以用终端操作数据库了
	-  **mysql -u root -p**
	-  输入新密码

## 安装MySQL Workbench

- MySQL Workbench是官方的可视化操作工具，使用可视化操作工具可以提高效率
- 安装过程没什么特别的，打开MySQL Workbench输入用户名和密码就可以用了

## 安装MySQLdb库(python2.7)

- 一般来说直接在命令行输入 **pip install MySQL-Python** 就好了，但是在安装的过程中很可能会遇到这个问题**mysql\_config not found**

- mysql\_config not found问题解决
	- 在 MySQL-python 的安装包中找到 site.cfg 文件，打开它，找到以下内容：
	- `# mysql_config = /usr/local/bin/mysql_config`
	- 然后改为`mysql_config = /usr/local/mysql/bin/mysql_config`就可以了

## 安装pymysql(Python3.X)

- python3.X不能用MySQLdb连接MySQL

- 安装pymysql非常简单，直接去pycharm>Preferences>Project>Project Interpreter安装就好

## shell脚本操作MySQL
#### MySQL语句结尾必须有分号
#### 常见命令

```sql
mysql> create database Name; 创建数据库，名字为Name
mysql> show databases/tables； 查看所有数据库/所有表
mysql> use Name；使用Name数据库
mysql> create table name(column1 type1 [not null][primary key],column2 type2 [not null],..)
# primary key是主键，not null是不为空
mysql> drop database/table name；删除数据库/表
mysql> alter table tabname add column col type;添加新列
mysql> alter table tablename change OldColumnName NewColumnName type attr;改列名和属性
mysql> Alter table tabname add/drop primary key(col);添加/删除主键

```

#### 以上关于创建表的操作在MySQL WorkBench上会更方便