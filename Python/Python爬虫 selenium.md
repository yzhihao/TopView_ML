#Python 爬虫笔记 Selenium
首先我们需要安装这个库
`pip install selenium`
这个库是用于自动化测试网站的，同样，也可以作为一个爬取网页的手段。
它的原理是模拟浏览器对相应的网页进行操作，简单的说，就是我们用浏览器可以对那个网页做什么，它就可以对那个网页做什么。
正因如此，哪怕是用js渲染过的网页元素，对于selenium来说一样可以轻松抓取。
**但是**，也正是因为如此，它在打开一个网页时需要耗费相当大量的时间，因为一般浏览器对于目标网页做的渲染它也要进行同样的操作，所以**不到万不得已，不建议使用selenium对网页进行抓取**

在安装完selenium后，我们就可以在python代码中import它的webdriver了。
`from selenium import webdriver`
不过在此之前，我们还需要安装一个无头浏览器（headless browser）phantomjs，这个东西也是一个浏览器，但与一般浏览器不同的是，它在使用的时候是没有界面的，也就是说不需要进行界面渲染，直接在底层与网站交互，这样可以节省程序运行的时间，不过事实上，运行的时间还是非常的长。
```
url="http://www.baidu.com"
driver=webdriver.
response=driver.get(url)
print response.page_source
```
很轻松的，用这种方式就可以打印出动态加载后的网页代码了