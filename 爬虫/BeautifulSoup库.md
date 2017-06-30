# BeautifulSoup

* [简介](#简介)
* [BeautifulSoup中的对象](#BeautifulSoup中的对象)
	* [bs4.BeautifulSoup](#BeautifulSoup//bs4.BeautifulSoup)
	* [Tag(标签)](#bs4.element.Tag)
	* [NavigableString(标签内非属性字符串)](#NavigableString(标签内非属性字符串) 即`tag.string`)
	* [bs4.element.Comment(注释)](#bs4.element.Comment(注释))

## 简介

- Beautiful Soup提供一些简单的、python式的函数用来处理导航、搜索、修改分析树等功能。
- Beautiful Soup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码。你不需要考虑编码方式，除非文档没有指定一个编码方式
- Beautiful Soup已成为和lxml、html6lib一样出色的python解释器，为用户灵活地提供不同的解析策略或强劲的速度。

	```python
	In[2]:from bs4 import BeautifulSoup#常见的引入方式
	In[3]:soup = BeautifulSoup(text,'html.parser')#text为网页源码，'html.parser'是html解析器
	In[4]:soup.a
	out[4]<a class="-logo js-gps-track " data-gps-track="top_nav.click({is_current:true, location:1, destination:8})" href="https://stackoverflow.com">\n<span class="-img">Stack Overflow</span>\n</a>
	```

## BeautifulSoup中的对象
### BeautifulSoup//bs4.BeautifulSoup

- soup.name 为 u'[document]',没有其他属性，指的是解析后的文档的全部内容


### Tag(标签)//bs4.element.Tag

- 标签属性
	- Name 标签名字 如
	```python
    In[5]:soup.a.name
    out[5]:u'a'
    ```
	- attrs 标签属性（字典）如
		- 可以访问标签属性的内容，即访问字典

	```python
	In[5]:soup.a.attrs
    out[5]:
    {u'class': [u'-logo', u'js-gps-track', u''],
	u'data-gps-track': u'top\_nav.click({is\_current:true, location:1, destination:8})',
 	'href': u'https://stackoverflow.com'}
    In[6]:soup.a.attrs['href']
    Out[6]:u'https://stackoverflow.com'}
	```
	- text 标签的内容 如
	```python
    In[7]:soup.a.text
    Out[7]: u'\nStack Overflow\n'
    ```
- 所以在提取页面信息时，可以通过标签一层一层的提取

### NavigableString(标签内非属性字符串) 即`tag.string`

- 有next/previous，可以向上或下遍历

### bs4.element.Comment(注释)

- 网页中可能存在注释，例如 `<b><!--这是注释--></b>`要区分NavigableString和comment只能通过**type**进行类型判断


## 标签树的遍历
### 遍历子标签

- tag.content tag下的所有子标签和换行符以**列表**返回
	- soup.content是本身
- tag.children 返回一个迭代类型，可以用for来迭代遍历

### 遍历父标签

- tag.parent 遍历父标签
- tag.parents 返回迭代类型，可以用for来迭代遍历
	- soup的父标签为None，soup的第一个标签的父标签为本身

### 兄弟标签遍历

- tag.next\_sibling/tag.previous\_sibling 按文本顺序向下/上遍历标签
- tag.next\_siblings/tag.previous\_siblings 返回迭代类型，可用for按文本顺序向下/上遍历后续节点标签

## 标签树的查找
### 子节点查找
#### soup.find\_all(tag,attr，recursive，text，\*\*kwargs,limit)

- name ：按标签的名字查找所有子孙节点
- text ：按标签内容查找所有子孙节点
- attrs ： 按属性（字典）查找所有子孙节点
- \*\*kwargs ： 按关键字查找所有子孙节点(可用正则)
- limit ： 查出几个

#### soup.find()

- 与find\_all()类似，返回第一个匹配的

### 父节点查找
#### find\_parents()

- 返回一个列表，递归的查找父节点符合条件的

####find\_parent()

- 向上查找父节点中符合条件的第一个


### 兄弟节点查找
#### find\_next\_siblings() 合 find\_next\_sibling()

- 与父节点查找类似，不多说

#### find\_previous\_siblings() 和 find\_previous\_sibling()

- 与父节点查找类似，不多说