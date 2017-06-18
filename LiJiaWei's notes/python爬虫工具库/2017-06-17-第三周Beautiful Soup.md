
* [Beautiful Soup](#BS)
	* [解析器](#解析器)
	* [四大对象种类](#四大对象种类)
		* [BeautifulSoup](#BeautifulSoup)
		* [Tag](#Tag)
		* [NavigableString](#NavigableString)
		* [Comment](#Comment)
	* [遍历文档树](#遍历文档树)
		* [子节点](#子节点)
		* [所有子孙节点](#所有子孙节点)
		* [其他遍历](#其他遍历)
	* [搜索文档树](#搜索文档树)
		* [过滤器](#过滤器)
			* [字符串](#字符串)
			* [正则表达式](#正则表达式)
			* [列表](#列表)
			* [True](#True)
			* [方法](#方法)
		* [find_all](#find_all)
			* [name参数](#name参数)
			* [keyword参数](#keyword参数)
			* [text参数](#text参数)
			* [limit参数](#limit参数)
			* [recursive参数](#recursive参数)
	* [CSS选择器](#CSS选择器)
	* [get_text](#get_text)


<div id="BS"></div>

# Beautiful Soup

**这里所讲述Beautiful Soup4，导入时import bs4**  
Beautiful Soup是python的一个库，最主要的功能是从网页抓取数据  
Beautiful Soup将复杂**HTML文档**转换成一个复杂的**树形结构**，**每个节点都是Python对象**，所有对象可以归纳为**4种**  
[官方文档](http://beautifulsoup.readthedocs.io/zh_CN/latest/)  

<br />

<div id="解析器"></div>

## 解析器

**Beautiful Soup支持Python标准库中的HTML解析器**,还支持一些第三方的解析器，下面例子都是使用**lxml解析器**，速度更快，更强大，**不过在使用前需要安装**，如果要使用Python标准库中的HTML解析器只需，**创建Beautiful Soup对象时，将**`“lxml”`**改为**`“html.parser”`  

<br />

<div id="四大对象种类"></div>

## 四大对象种类

Beautiful Soup将HTML文档转换成树形结构的时候，**每个节点都是Python对象，对象种类可以归纳为4类**  
- BeautifulSoup
- Tag
- NavigableString
- Comment

<br />

<div id="BeautifulSoup"></div>

### BeautifulSoup

**BeautifulSoup对象表示的是一个文档的全部内容**.大部分时候,可以把它当作 Tag 对象，**是一个特殊的 Tag**  
在将HTML文档转换为树形结构时，需要创建一个Beautiful Soup对象  
```python
from bs4 import BeautifulSoup

# index.html是一个HTML文件，html是一个HTML文档的字符串
soup1 = BeautifulSoup(open('index.html'), "lxml")
soup2 = BeautifulSoup(html, "lxml")

print soup1.prettify()
```
其中使用了BeautifulSoup对象的`prettify()`**用于将BeautifulSoup格式化输出**  

<br />

<div id="Tag"></div>

### Tag

Tag就是 HTML 中的一个个标签，例如  
```python
<title>The Dormouse's story</title>
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
```

<br />

可以用BeautifulSoup对象来获取Tags  
我们可以利用**soup加标签名**轻松地获取这些标签的内容  
**不过它查找的是在所有内容中的第一个符合要求的标签**  
```python
print soup.title
#<title>The Dormouse's story</title>

print soup.head
#<head><title>The Dormouse's story</title></head>
```

<br />

对于 Tag，它有两个重要的属性，是`name`和`attrs`  
**除了soup对象外，它的**`name`**是[document]**，**其他内部标签，输出的值便为标签本身的名称**  
**查看**`attrs`**可以查看标签的所有属性，得到的类型是一个字典**  
```python
print soup.name
print soup.head.name
#[document]
#head

print soup.p.attrs
#{'class': ['title'], 'name': 'dromouse'}
```

<br />

<div id="NavigableString"></div>

### NavigableString

如果想获取标签内部的文字，可以`.string()`，得到的对象就是一个NavigableString对象  
注意
```python
print soup.p.string
#The Dormouse's story

print type(soup.p.string)
#class 'bs4.element.NavigableString'
```

<br />

<div id="Comment"></div>

### Comment

**Comment对象是一个特殊类型的NavigableString对象**，其实输出的内容仍然不包括注释符号  
**如果想将注释内容单独处理，可以先判断得到的对象是否是Comment对象，再进行处理**  
```python
if type(soup.a.string)==bs4.element.Comment:
    print soup.a.string
```

<br />

<div id="遍历文档树"></div>

## 遍历文档树

<div id="子节点"></div>

### 子节点

tag的`.content`属性可以将tag的子节点以列表的方式输出  
```python
print soup.head.contents
#[<title>The Dormouse's story</title>]
```

<br />

Tag的`.children`属性可以得到所有子节点的**list生成器对象**， **通过遍历输出** 
```python
for child in  soup.body.children:
    print child
```

<br />

<div id="所有子孙节点"></div>

### 所有子孙节点

`.descendants`属性可以对所有tag的子孙节点进行递归循环，和`.children`类似，我们也需要**遍历获取其中的内容**  
**先从最外层的 HTML标签，其次从 head 标签一个个剥离，以此类推**  
```python
for child in soup.descendants:
    print child
```

<br />

<div id="其他遍历"></div>

### 其他遍历

还可以**遍历父节点，全部父节点，兄弟节点，全部兄弟节点，前后节点，全部前后节点**，用法和遍历子节点类似，由于用的较少，在此不详细讲解，有需要可以查找[文档](http://beautifulsoup.readthedocs.io/zh_CN/latest/#id18)

<br />

<div id="搜索文档树"></div>

## 搜索文档树

<div id="过滤器"></div>

### 过滤器

**过滤器可以被用在tag的name中，节点的属性中，字符串中或他们的混合中**  

<br />

<div id="字符串"></div>

#### 字符串

最简单的过滤器是字符串，在搜索方法中传入一个字符串参数，Beautiful Soup会查找与字符串完整匹配的内容  
```python
soup.find_all('b')
# [<b>The Dormouse's story</b>]
```

<br />

<div id="正则表达式"></div>

#### 正则表达式

如果传入正则表达式作为参数，Beautiful Soup会通过正则表达式的`match()`来匹配内容  
```python
import re
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)
# body
# b
```

<br />

<div id="列表"></div>

#### 列表

如果传入列表参数，Beautiful Soup会将与列表中任一元素匹配的内容返回  
```python
soup.find_all(["a", "b"])
# [<b>The Dormouse's story</b>,
#  <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
```

<br />

<div id="True"></div>

#### True

True 可以匹配任何值，下面代码查找到所有的tag，但是不会返回字符串节点  
```python
for tag in soup.find_all(True):
    print(tag.name)
# html
# head
# title
# body
# p
# b
# a
```

<br />

<div id="方法"></div>

#### 方法

还可以定义一个方法，**方法只接受一个元素参数**，**如果这个方法返回True表示当前元素匹配并且被找到，如果不是则返回False**  
```python
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

soup.find_all(has_class_but_no_id)
# [<p class="title"><b>The Dormouse's story</b></p>,
#  <p class="story">Once upon a time there were...</p>,
#  <p class="story">...</p>]
```

<br />

<div id="find_all"></div>

### find_all(name, attrs, recursive, text, \*\*kwargs)

`find_all()`方法搜索**当前tag的所有tag子节点**，并判断是否符合过滤器的条件，返回一个list  
`find()`**方法与find_all()类似，但只返回第一个搜索的节点**  

<br />

<div id="name参数"></div>

#### name参数

name参数可以查找所有名字为name的tag,字符串对象会被自动忽略掉  
**name参数的值可以是任一类型的过滤器，字符串，正则表达式，列表，方法或是True**
```python
soup.find_all("title")
# [<title>The Dormouse's story</title>]
```

<br />

<div id="keyword参数"></div>

#### keyword参数

**如果一个指定名字的参数不是搜索内置的参数名，搜索时会把该参数当作指定名字tag的属性来搜索，如果包含一个名字为id的参数,Beautiful Soup会搜索每个tag的”id”属性**  
**class作为参数时加下划线**  
```python
soup.find_all(href=re.compile("elsie"), id='link1')
# [<a class="sister" href="http://example.com/elsie" id="link1">three</a>]

# 可以和name参数组合使用
soup.find_all("a", class_="sister")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
```

<br />

<div id="text参数"></div>

#### text参数

通过text参数可以搜搜文档中的字符串内容，与name参数的可选值一样，**text参数接受 字符串，正则表达式，列表，True**  
```python
soup.find_all(text="Elsie")
# [u'Elsie']

soup.find_all(text=re.compile("Dormouse"))
[u"The Dormouse's story", u"The Dormouse's story"]
```

<br />

<div id="limit参数"></div>

#### limit参数

**limit参数限制返回结果的数量，当搜索到的结果数量达到limit的限制时，就停止搜索返回结果**  

<br />

<div id="recursive参数"></div>

#### recursive参数

调用tag的 find_all()方法时，Beautiful Soup会检索当前tag的所有子孙节点，**如果只想搜索tag的直接子节点，可以使用参数**`recursive=False`  

<br />

<div id="其他搜索方法"></div>

### 其他搜索方法

其他搜索方法与`find_all()`和`find()`类似，搜索父节点`find_parents()`和`find_parent()`，搜索后面的兄弟节点`find_next_siblings()`和`find_next_sibling()`，搜索前面的兄弟节点`find_previous_siblings()`和`find_previous_sibling()`，搜索后面节点`find_all_next()`和`find_next()`，搜索前面节点`find_all_previous()`和`find_previous()`，由于用法功能与`find_all()`和`find()`类似，不详细展开，可以查询[文档](http://beautifulsoup.readthedocs.io/zh_CN/latest/#id27)  

<br />

<div id="CSS选择器"></div>

## CSS选择器

可以用写CSS的类似方法来筛选元素，标签名不加任何修饰，类名前加点，id名前加\#，用到的方法是`soup.select()`返回一个list

<div id="通过标签名查找"></div>

### 通过标签名查找

```python
print soup.select('title')
#[<title>The Dormouse's story</title>]

print soup.select('a')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```

<br />

<div id="通过类名查找"></div>

### 通过类名查找

```python
print soup.select('.sister')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```

<br />

<div id="通过id名查找"></div>

### 通过id名查找

```python
print soup.select('#link1')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```

<br />

<div id="属性查找"></div>

### 属性查找

查找时还可以加入属性元素，属性需要用**中括号**括起来，**注意属性和标签属于同一节点，所以中间不能加空格**  
```python
print soup.select('a[href="http://example.com/elsie"]')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```

<br />

<div id="组合查找"></div>

### 组合查找

上面这几种查找方法也可以组合查找  
**不在同一节点的空格隔开，同一节点的不加空格**  
```python
print soup.select('p #link1')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]

print soup.select('p a[href="http://example.com/elsie"]')
#[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```

<br />

也可以直接查找子标签  
```python
print soup.select("head > title")
#[<title>The Dormouse's story</title>]
```

<br />

<div id="get_text"></div>

## get_text()

如果只想得到tag中包含的文本内容,那么可以用get_text()方法,这个方法获取到tag中包含的所有文版内容包括子孙tag中的内容,并将结果作为Unicode字符串返回  
可以通过参数指定tag的文本内容的分隔符,还可以设置`strip`去除获得文本内容的前后空白  
```python
markup = '<a href="http://example.com/">\nI linked to <i>example.com</i>\n</a>'
soup = BeautifulSoup(markup)

soup.get_text()
u'\nI linked to example.com\n'

soup.get_text("|", strip=True)
# u'I linked to|example.com'
```

<br />

`.string`和`get_text()`都可以获取节点文本，区别在于`.string`**只找寻唯一的节点或子节点文本内容，若有多个则返回**`None`，而`get_text()`**则是找寻所有子孙节点的文本内容**  

<br />

`.strings`得到生成器来循环也可以得到节点下所有的字符串，`stripped_strings`可以清除空格  
```python
for string in soup.strings:
    print(repr(string))
    # u"The Dormouse's story"
    # u'\n\n'
    # u"The Dormouse's story"
    # u'\n\n'
    # u'Once upon a time there were three little sisters; and their names were\n'
    # u'Elsie'

for string in soup.stripped_strings:
    print(repr(string))
    # u"The Dormouse's story"
    # u"The Dormouse's story"
    # u'Once upon a time there were three little sisters; and their names were'
    # u'Elsie'
```

