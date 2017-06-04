# Python爬虫笔记 urllib2
首先确保已经安装urllib2包，然后在文件中导入urllib2包
`import urllib2`
然后用urlopen方法打开对应的url，这里设置url为address
`address = 'http://www.appzapp.us/Top100.html'
response=urllib2.urlopen(address)`
urlopen有三个参数，第一个就是url即上文中的address，第二个是data，作为打开该网页时需要传入的数据，这个暂且不表。

两行代码得到response对象,response对象可以通过read方法直接返回网页的源代码
`pageCode = response.read()`
打印pageCode可以看见网页的源代码
不过这只能用于比较简单的网页读取，实际上，我们还需要通过request对象来传入更多的信息
```
import urllib2
address='http://www.appzapp.us/Top100.html'
request=urllib2.Request(address)
response=urllib2.urlopen(request)
```
一般来说，如果网页需要用户名和密码的话，我们还需要用到post和get

post方法：
```
import urllib
import urllib2

values = {"username":"user","password":"password"}
data = urllib.urlencod(values)
address='http://www.appzapp.us/Top100.html'
request=urllib2.Reques(url,data)
response=urllib2.urlopen(request)
```
get方法:
```
import urllib
import urllib2

values={}
values['username'] = "1016903103@qq.com"
values['password']="XXXX"
data = urllib.urlencode(values)
url = "http://passport.csdn.net/account/login"
geturl = url + "?"+data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
print response.read()
```

实际上两者的区别就是post将传入信息单独拉出来作为一个data参数在打开url的时候传入，而get这是将data信息在urlencode之后与url的address合并成一个字符串作为一个url参数传入