# requests库

## 一、get()方法
#### 在写爬虫时基本用的是requests的get方法
- requests.get(url,\*params,\*headers，\*timeout)
	- url 为要爬去的网页链接
	- params 可以在url链接后增加一些参数(可以用来翻页或者修改查询关键字)
	- headers 可以定制响应头（一般修改 user-agent）
	- proxies 设置代理
	- timeout 是设置响应时间

```
import requests
try：
	user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
    headers = {'user-agent':user-agent} #改变响应头的user-agent，伪装成浏览器
    url = http://stackoverflow.com/questions'
	params = {'page':1,'sort':'newest'}#设置url参数，选择以最新一页的问题页面作为爬去目标
    web = requests.get(url,params = params,headers = headers)
except：
	print web.status_code
```
#### requests.get()返回response对象
- web.stauts\_code 返回状态码 200 为响应成功
- web.raise\_for\_status() 若返回状态码不为200，则抛出异常(一般get方法都是放在try except 里面)
- web.text 返回响应内容，即页面的html 还有 json
- 一般调用 web.text前会有这么一句 `web.encoding = web.apparent_encoding`来设置编码
- 如果要下载图片或者视频，就要用 web.content,web.content返回二进制响应内容
- 同理，如果要处理json数据，使用web.json()即可,(但有可能解码失败)

## 二、post()方法
#### 把数据放在header提交
- 用法和get()类似

比较：post 比 get 更安全,因为通过get提交数据，密码用户名直接出现在url，不安全