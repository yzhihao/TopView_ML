#Python 爬虫笔记 BeautifulSoup
老样子，我们先安装
`pip install bs4`
然后导入
`from bs4 import BeautifulSoup`
这个模块，用于对已经截取到的网页源代码进行解析，它的原理类似于lxml，将网页源代码字符串转化成节点树，然后我们就可以按照它的规则在这个树中搜索我们想要的内容。
假设，我们已经获取了一段网页源代码
`pageSource="..."`
要从这份源代码中找到我们想要的信息，我们就需要先把它转化成bs4对象的结构树。
`soup=BeautifulSoup(pageSource,'html.parser')`
这里html.parser是指网页的解析器，这个解析器是python自带的解析器，稳定，方便，速度适中，还有更好的解析器是lxml解析器，速度更快，不过需要另外下载。
有了soup以后，我们就可以操作它
```
nameNode=soup.find('title')
name=nameNode.get_text()
#查找标签为title的节点，并返回它包含的text内容
nodes=soup.find('div',class_="activities").find_all('div',class_=re.compile(r'\d+'))
#用find方法找到标签为'div',class属性为'activities'的节点，
#并找到其下所有标签为'div',class属性符合代码所示正则表达式的节点，同时返还一个可以迭代的对象
```
除了属性之外，还可以查找链接参数'href'，id参数'id',不过属性的写法比较特殊，需要在后面加一个下划线，像是'class_'
同时，bs4还支持正则表达式的匹配方式，着实让解析网页方便了不少
