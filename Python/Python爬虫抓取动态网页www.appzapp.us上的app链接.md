#Python 爬虫笔记 抓取动态页面
这次的考核不小心选了一个相当坑的网站
[苹果App](http://www.appzapp.us/Index.html)

目标是从该网站上爬取所有的app的近段时间的价格变动状况。

起初我使用简单的urllib2加beautifulsoup4的方法来爬取，但是效果不尽人意，因为该网页上用来翻页的按钮以及页面上app的链接通通都用js渲染过，这就很坑爹了，因为这意味着网页的源代码里面不包含我们需要的信息。

于是，为了获取动态网页，我们有两个方法：

第一个是使用selenium库，直接暴力模拟浏览器对网页进行操作，但是耗时太长，这里由于我需要抓取大量数据，这个方法不太好

第二个，便是分析网页在动态加载时我们输送的请求与它的响应信息，从而有针对性的操作相应接口来得到我们想要的内容。
首先，我们用浏览器打开要抓取的网页，我用的是firefox
[苹果App网页](http://www.appzapp.us/Index.html)
然后右键审查要抓取的元素，像是第一个app网页的链接
[Stop! This Discovering Jesus Christ Inform](http://www.appzapp.us/App/Stop-This-Discovering-Jesus-Christ-Information-Could-Change-Your-Life-1103657491.html)
我们可以在查看器中看到，它的链接显示在a标签的href里卖弄，但这个是网页动态加载完成之后的代码，如果我们用urllib2直接open[苹果App网页](http://www.appzapp.us/Index.html)的话，是抓不到这个链接的。
因此我们还需要点到network选项卡上，点两下翻页与回退按钮，观察情况，进行抓包。
我们看到有大量的文件传输，为了方便分辨，我们点XHR帮我们过滤掉一些乱七八糟的文件。XHR全称“XMLHttpRequest”，该对象可在不向服务器提交整个页面的情况下实现局部更新网页的效果，一般来说，都是这些东西在动态加载。
然后我们观察这些动态加载的文件的名字，有一个getRecentActivities与一堆GetActivityDetails,分别点一下，在右边查看，看到请求网址分别是http://www.appzapp.us/Service/listings.asmx/getRecentActivities
与
http://www.appzapp.us/Service/listings.asmx/GetActivityDetails
这就说明，我们在打开这个网页的时候，同时还对这些链接发出了请求，再点击参数和响应，我们可以看到我们向这些链接发送请求时传入的参数，以及这些链接给我们的响应。在getRecentActivities的响应中，我们看到了一个CurrentPage关键字的值为1，根据它的英文意思，我们点击几次换页按钮，可以发现这个CurrentPage指的是当前显示的app页的页码。可想而知，getRecentActivity对象应该是指整个app页，再仔细看它的参数，发现ResultSet关键字以及15串数字，而app页上一次显示的app数量也正好是15个，大概可以猜出，这15串数字是作为某种标识码向服务器端读取需要的app的模块用的。
再看到GetActivityDetails，我们发现它的参数只有一个，'id'后面跟着一串数字，与前面发现的十五串数字比对，发现正好有一串吻合，显然，这便是某个app模块的标识码了。
这个时候，我们先不急着往下看，因为目标是抓取app的链接，我们先点开一个app的链接看看情况。
[Stop! This Discovering Jesus Christ Inform](http://www.appzapp.us/App/Stop-This-Discovering-Jesus-Christ-Information-Could-Change-Your-Life-1103657491.html)
点开后，我们观察它在地址栏中的表现形式，是以http://www.appzapp.us/App/加上app的名字以及一传数字加.html组成的。为了验证猜想，我们可以再多点几个。
通过多次实验之后，我们发现app链接的头部http://www.appzapp.us/App/和尾部.html是不变的，我们需要得到的，就是app的名字内容以及后面那一串数字。
再次回到GetActivityDetails，观察它的响应，为了方便观察，我们可以把它复制到记事本中。然后，我们找到了一个关键字为UrlTitle的东西，它的值恰好就是app名字在地址栏中的表现形式，以及另外个关键字为AppID，值为一串数字的东西。我们把这两个东西复制出来，与之前找到的链接头和链接尾按照它的规则拼接在一起，然后放到浏览器的地址栏中，果不其然，浏览器跳到了这个app的链接。
于是，我们明白了，我们需要先从getRecentActivities对象中获取整页app页中各个app的ActivityID，然后将这个ID作为参数，对GetActivityDetails的请求网址发出请求，并在响应中抽取出UrlTitle与AppID的值与http://www.appzapp.us/App/
和.html拼接在一起，从而得到一条完整的app链接。
明白这些之后，我们就可以把工作交给代码了。

话是这么说，这短短几十行字的过程我也是花了两天....
