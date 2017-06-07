
* [Cookie](#Cookie)
	* [Cookie介绍](#Cookie介绍)
	* [Cookielib](#Cookielib)
		* [获取Cookie保存到变量](#获取Cookie保存到变量)
		* [保存Cookie到文件](#保存Cookie到文件)
		* [从文件中获取Cookie并访问](#从文件中获取Cookie并访问)
		* [利用cookie模拟登陆](#利用cookie模拟登陆)
* [URLError](#URLError)
	* [HTTPError](#HTTPError)


<div id="Cookie"></div>

# Cookie

<br >

<div id="Cookie介绍"></div>

## Cookie介绍

**Cookie，指某些网站为了辨别用户身份、进行session跟踪而储存在用户本地终端上的数据（通常经过加密）**  
比如你要打开一些网页是需要用户先登录的，在登陆前无法访问，这时候就可以先模拟登陆，用Urllib2库保存我们登录的Cookie，再访问网页  

<br />

<div id="Cookielib"></div>

## Cookielib

cookielib模块的主要作用是提供可存储cookie的对象，以便于与urllib2模块配合使用来访问Internet资源。Cookielib模块非常强大，我们可以利用本模块的**CookieJar类**的对象来捕获cookie并在后续连接请求时重新发送，比如可以实现模拟登录功能。该模块主要的对象有**CookieJar**、**FileCookieJar**、**MozillaCookieJa**r、**LWPCookieJar**  
**CookieJar -> 派生 -> FileCookieJar -> 派生 –> MozillaCookieJar和LWPCookieJar**  

<br />

<div id="获取Cookie保存到变量"></div>

### 获取Cookie保存到变量

可以用**CookieJar对象**实现cookie的获取和存储，再利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器，再构建opener  
```python
import urllib2
import cookielib

#声明一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler=urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib2.build_opener(handler)
#此处的open方法同urllib2的urlopen方法，也可以传入request
response = opener.open('http://www.baidu.com')
for item in cookie:
    print 'Name = '+item.name
    print 'Value = '+item.value
```

上面的例子将opener打开的网页的cookie保存到变量多，可以打印出cookie的值  

<br />

<div id="保存Cookie到文件"></div>

### 保存Cookie到文件

除了把cookie保存到变量里，还可以用**FileCookieJar类**保存到文件中，这里例子用的是他的子类**MozillaCookieJar**实现的  
```python
import cookielib
import urllib2

#设置保存cookie的文件，同级目录下的cookie.txt
filename = 'cookie.txt'
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib2.build_opener(handler)
#创建一个请求，原理同urllib2的urlopen
response = opener.open("http://www.baidu.com")
#保存cookie到文件
cookie.save(ignore_discard=True, ignore_expires=True)
```
其中`.save()`函数中的**ignore_discard**的意思是即使cookies将被丢弃也将它保存下来，**ignore_expires**的意思是如果在该文件中Cookies已经存在，则覆盖原文件写入  

<br />

<div id="从文件中获取Cookie并访问"></div>

### 从文件中获取Cookie并访问

从文件中获取cookies也同样是用MozillaCookieJar对象  
就像下面的例子，如果你的cookie.txt里保存的是登陆了百度的cookie，那这个例子就可以模拟这个人的账号登录百度  
```python
import cookielib
import urllib2

#创建MozillaCookieJar实例对象
cookie = cookielib.MozillaCookieJar()
#从文件中读取cookie内容到变量
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
#创建请求的request
req = urllib2.Request("http://www.baidu.com")
#利用urllib2的build_opener方法创建一个opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)
print response.read()
```

<br />

<div id="利用cookie模拟登陆"></div>

### 利用cookie模拟登陆

下面的例子是将cookie存储在变量里，模拟登陆教务系统后访问个人主页  
```python
import urllib
import urllib2
import cookielib

url_login = 'http://222.200.98.147/login!doLogin.action'
url = 'http://222.200.98.147/login!welcome.action'
values = {'account': '3116004779', 'pwd': '559ljw', 'verifycode': ''}
data = urllib.urlencode(values)
request_login = urllib2.Request(url_login, data)
request = urllib2.Request(url)
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
response = opener.open(request_login)
response = opener.open(request)
print response.read()
```

<br />

<div id="URLError"></div>

## URLError

URLError可能产生的原因：
1. 网络无连接，即本机无法上网
2. 连接不到特定的服务器
3. 服务器不存在
4. 连接超时

在代码中，我们需要用**try-except语句**来包围并捕获相应的异常  
```python
import urllib2

requset = urllib2.Request('http://www.xxxxx.com')
try:
    urllib2.urlopen(request)
except urllib2.URLError, e:
    print e.reason
```

<br />

<div id="HTTPError"></div>

### HTTPError

HTTPError是URLError的子类，在你利用urlopen方法发出一个请求时，服务器上都会对应一个应答对象response，其中它包含一个数字”状态码”  
HTTP状态码表示HTTP协议所返回的响应的状态  
**由于HTTPError是URLError的子类，所以在捕获HTTPError要在URLError之前**  
还用**hasattr**属性提前对属性进行判断  
```python
import urllib2

req = urllib2.Request('http://blog.csdn.net/cqcre')
try:
    urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.code
except urllib2.URLError, e:
    if hasattr(e,"reason"):
        print e.reason
else:
    print "OK"
```

<br />

**HTTP1.1状态码大致分五大类：**
1. 100-199 用于指定客户端应相应的某些动作
2. 200-299 用于表示请求成功
3. 300-399 用于已经移动的文件并且常被包含在定位头信息中指定新的地址信息
4. 400-499 用于指出客户端的错误
5. 500-599 用于支持服务器错误

**具体的可以遇到时再搜索**


