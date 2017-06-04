#Python 爬虫笔记 Request库
首先我们需要安装requests库
然后在python文件中导入requests
`import requests`
requests库的相较于urllib2在网页的抓取上面更加简洁有效，它同样支持post，get等方法，并且可以传入参数。

###post：
```
import requests
url='http://www.baidu.com'
data={'key1':'value1','key2':'value2'}
headers={'User-Agent':'Mozilla.xxx'}
request=requests.post(url,data=data,headers=headers)
```
然后便可以使用
`request.text`或者`request.content`查看返回的内容，用`request.json()`查看返回的json

如果要传入的参数是json的话，还可以使用json=data

###get：
```
#其他地方没有什么不同，省略
reques=request.get(url,params=data,headers=headers)
```
这里主要是data参数变成了params，它同样支持传入json，方法同post一样

二者都支持传入cookie，只需要增加参数`cookies=要传入的cookie`即可