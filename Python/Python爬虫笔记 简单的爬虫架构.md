Python爬虫笔记 简单的爬虫架构

简单的爬虫架构分为以下几个部分
html_downloader：
html下载器，用于下载目标页面的信息

url_manager:
url管理器，用于管理需要爬取的链接

html_parser:
html分析器，用于下载下来的信息，并从中提取出需要的信息以及可以放入待爬队列的url

html_outputer:
输出器，用于将爬取下来的信息保存起来，换句话说，就是输出到本地