---

layout: post

title:  "PhantomJS和Selenium"

date:   2017-06-24 15:39:00

categories: python爬虫工具库

---

* [PhantomJS](#PhantomJS)
	* [安装](#安装)
	* [PhantomJS的使用](#PhantomJS的使用)
* [Selenium](#Selenium)
	* [页面操作](#页面操作)
		* [页面交互和填充表单](#页面交互和填充表单)
		* [填充下拉选项卡](#填充下拉选项卡)
		* [元素拖拽](#元素拖拽)
		* [Cookies处理](#Cookies处理)
	* [页面等待](#页面等待)
		* [显式等待](#显式等待)
		* [隐式等待](#隐式等待)

<div id="PhantomJS"></div>

# PhantomJS

PhantomJS是一个**无界面的,可脚本编程**的WebKit浏览器引擎,**它原生支持多种web 标准：DOM 操作，CSS选择器，JSON，Canvas 以及SVG******，简单来说就是个**无界面浏览器**  

<br />

<div id="安装"></div>

## 安装

到[下载地址](http://phantomjs.org/download.html)选择相对应开发平台进行下载即可  

<br />

<div id="PhantomJS的使用"></div>

## PhantomJS的使用

PhantomJS可以**加载网页，捕获屏幕，网络监听，网页自动化处理等等操作**，由于我是将其与python的Selenium库结合使用，在此不详细说明怎么使用，详情可见[官方样例](http://phantomjs.org/examples/index.html)或者[使用教程](http://cuiqingcai.com/2577.html)

<br />

<div id="Selenium"></div>

# Selenium

Selenium是自动化测试工具，它支持各种浏览器，包括 Chrome，Safari，Firefox 等主流界面式浏览器，如果你在这些浏览器里面安装一个 Selenium 的插件，那么便可以方便地实现Web界面的测试  
Selenium支持多种语言开发，比如 Java，C，Ruby还有**python**
**所以可以结合这PhantomJS + Selenium来实现对页面的模拟操作**  
**在使用的时候需要先根据不同浏览器生成不同的driver，可以用**`.get`**方法获取网页**  
**输出page_source属性可以获取网页渲染后的源代码**
**最后需要退出driver，否则会一直运行**  
```python
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get("http://www.python.org")
print driver.page_source
driver.quit()
```

<br />

<div id="页面操作"></div>

## 页面操作

下面是几个常用的页面操作，其他还有更多操作不详细说明，可以参考[教程](http://cuiqingcai.com/2599.html)  

<br />

<div id="页面交互和填充表单"></div>

### 页面交互和填充表单

有时候我们需要和页面进行交互，比如点击，输入等等，那么前提就是要找到页面中的元素,WebDriver提供了各种方法来寻找元素  
例如有这样一个输入框  
```python
<input type="text" name="passwd" id="passwd-id" />
```
有下面四种获取方法  
```python
element = driver.find_element_by_id("passwd-id")
element = driver.find_element_by_name("passwd")
element = driver.find_elements_by_tag_name("input")
element = driver.find_element_by_xpath("//input[@id='passwd-id']")
```
**而且你在用xpath的时候还需要注意的是，如果有多个元素匹配了xpath，它只会返回第一个匹配的元素，如果没有找到，那么会抛出NoSuchElementException的异常**  
```python
element.send_keys("some text")
elem.send_keys(Keys.RETURN)
element.clear()
```
**可以向获取到的输入框输入文本，也可以清除文本**  
`Keys.RETURN`**相当于按了键盘的回车键，提交文本**  

<br />

<div id="填充下拉选项卡"></div>

### 填充下拉选项卡

除了文本框常用的还有下拉选项卡  
**可以先找到选项卡位置，再用WebDriver中提供了一个叫Select的方法，可以根据索引来选择，可以根据值来选择，可以根据文字来选择，还可以全部取消选择**  
**输入完后提交只用先找到提交按钮，再用**`.click()`**方法模拟点击**  
```python
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element_by_name('name'))
select.select_by_index(index)
select.select_by_visible_text("text")
select.select_by_value(value)
select.deselect_all()

driver.find_element_by_id("submit").click()
```

<br />

<div id="元素拖拽"></div>

### 元素拖拽

要完成元素的拖拽，首先你需要指定被拖动的元素和拖动目标元素，然后利用ActionChains类来实现  
元素从 source 拖动到 target 的操作  
```python
element = driver.find_element_by_name("source")
target = driver.find_element_by_name("target")

from selenium.webdriver import ActionChains
action_chains = ActionChains(driver)
action_chains.drag_and_drop(element, target).perform()
```

<br />

<div id="Cookies处理"></div>

### Cookies处理

可以获取页面cookies，也可以添加cookies  
```python
# Go to the correct domain
driver.get("http://www.example.com")
# And now output all the available cookies for the current URL
cookie = driver.get_cookies()


# Go to the correct domain
driver.get("http://www.example.com")
# Now set the cookie. This one's valid for the entire domain
cookie = {‘name’ : ‘foo’, ‘value’ : ‘bar’}
driver.add_cookie(cookie)
```

<br />

<div id="元素选取"></div>

## 元素选取

**元素选取有以下API**  
```python
find_element_by_id
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector
```
以上是单个选取返回第一个符合条件的，也可以使用多个选取返回所有符合的元素，只用将原函数的`element`换成`elements`就可以了，像`find_elements_by_id`  
**另外还可以利用 By 类来确定哪种选择方式**
```python
from selenium.webdriver.common.by import By

driver.find_element(By.XPATH, '//button[text()="Some text"]')
driver.find_elements(By.XPATH, '//button')
```

<br />

<div id="页面等待"></div>

## 页面等待

有些需要等待网页加载完全，所以需要等待某个元素加载出来  
所以 Selenium 提供了两种等待方式，一种是隐式等待，一种是显式等待  
**隐式等待是等待特定的时间，显式等待是指定某一条件直到这个条件成立时继续执行**  

<br />

<div id="显式等待"></div>

### 显式等待

显式等待指定某个条件，然后设置最长等待时间，如果在这个时间还没有找到元素，那么便会抛出异常了  
下面例子设置了默认会500ms调用一次来查看元素是否已经生成，如果本来元素就是存在的，那么会立即返回  
可以使用内置的等待条件，可以直接调用，具体可以看[官方文档](http://selenium-python.readthedocs.io/waits.html)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS()
driver.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
finally:
    driver.quit()
```

<br />

<div id="隐式等待"></div>

### 隐式等待

隐式等待比较简单，就是简单地设置一个等待时间，单位为秒  
默认值为0  
```python
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.implicitly_wait(10) # seconds
driver.get("http://somedomain/url_that_delays_loading")
myDynamicElement = driver.find_element_by_id("myDynamicElement")
```
