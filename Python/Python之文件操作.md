# Python 文件操作
## 打开文件
- file = open(path,pattern)
	- path 是文件路径
	- pattern 是对文件操作的模式，有：

| Parttern | 简介 |
|--------|--------|
|r       | 只读|
|w       | 只写（会覆写整个文件）|
|a       |追加 (从 EOF 开始, 必要时创建新文件)|
|r+      |读与写|
|w+      |读与写|
|a+      |读与写|
|rb      |以二进制只读模式打开|
|wb      |以二进制只写模式打开 |
|ab      |以二进制追加模式打开  |
|rb+     |以二进制读写模式打开 |
|wb+     |以二进制读写模式打开 |
|ab+     |以二进制读写模式打开       |

## 读取
| 方法 | 简介 |
|--------|--------|
|   file.read()|一次性读完|
|file.readline()|读取一行|
|file.readlines()|读取一行|

- 当读取内容大于内存大小不能使用read
- readlines是一次性读完整个文件再分成行，readline比readline快

## 写入
| 方法 | 简介 |
|--------|--------|
|   file.write()|一次性写入|
|file.writelines()|读取一行|

- 当使用write写入时，若写入的内容大于缓冲区，则会直接写入文件(一般会先写入缓存区)
- writelines可以把列表当参数
- 一般写入操作之后都应调用flush()，把缓存区的内容写到文件去

## 关闭文件
- 每当完成文件操作之后都应关闭文件，即调用 close()，原因如下：
	1. close关闭文件的同时会把缓存区的内容写到文件去
	2. 文件不关闭会占用资源
- 所以我们可以用try/finally来确保文件可以正常关闭
- 如果不想每次都写try/finally,可以用with语句打开文件

## 与文件操作比较相关的库是 os

- os.listdir() 返回指定目录下的所有文件和目录名

### 创建目录
- os.mkdir（“test”）创建单个目录
- os.makedirs（r“c：\python\test”）创建多级目录

### 删除文件或目录
- os.remove()删除一个文件
- os.removedirs（）删除多个目录

### 路径判断
- os.path.isfile()   是否是一个**文件**
- os.path.isdir() 是否是一个**目录**
- os.path.isabs() 是否是**绝对路径**
- os.path.exists()  路径是否**存在**(一般需要用这个判断路径是否存在，不存在则创建)

### 路径
- os.path.split() 返回一个由**路径目录名**和**文件名**组成的元组
- os.path.splitext() 返回一个路径(**路径中没有拓展名**)和拓展名的一个元组
- os.path.dirname() 获取**路径名**

### 文件信息
- os.path.basename() 获取文件名
- os.stat（）获取文件属性：
- os.path.getsize（）获取文件大小
- os.rename（oldName,newName）重命名
