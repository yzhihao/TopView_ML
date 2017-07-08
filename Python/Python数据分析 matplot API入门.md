#Python数据分析 绘图和可视化 matplotlib API入门
###Ipython
Ipython是使用matplotlib的常用ide，但我这里运行Ipython在打括号时会莫名卡顿，这个让我感觉很莫名。
qidongIpython只需要使用cmd输入`ipython --pylab`即可指定IPython配置matplotlib GUI后端，我们可以使用一行简单的代码测试一切是否准备就绪
```
plot（np.arange(10))
```
![测试图片](D:\study\Markdown\Note\Python\img\Figure_1.png)
不使用ipython的话，我们还需要在后面加上代码`show()`才可以使图片正常显示。
显示图片后，在交互界面我们可以通过鼠标点击或者输入close（）来关闭

###Figure和Subplot
matplotlib的图像都位于Figure图像中，我们可以使用plt.figure来创建一个Figure对象
```
fig=plt.figure()
```
figure方法有一些选项，他宝库figsize来确定保存到磁盘时图像的大小和纵横比，matplotlib中的Figure还支持MATLAB式的编号架构（尽管我现在还没有用过MATLAB），通过plt.gcf()可以得到当前Figure的引用。

要想通过Figure绘图，我们还需要一个subplot对象，他通过Figure对象的add_subplot()方法创建
```
fig=plt.figure()
ax1=fig.add_subplot(2,2,1)
ax2=fig.add_subplot(2,2,2)
ax3=fig.add_subplot(2,2,3)
```
add_subplot方法中前两个数值表示图像是2*2的，第三个数字表示当前选中的是4个subplot中的一个。

如果这个时候发出绘图命令，matplotlib会在最后一个用过的subplot（如果没有则创建一个）上进行绘制。
```
plt.plot(np.random.randn(50).cumsum(),'k--')
plt.show()
```
‘k--’是一个线性选项，用于告诉matplotlib绘制黑色虚线图，这里我们是在ax3上面绘的图，我们可以直接调用ax2或者ax1从而在他们身上绘图
```
plt.plot(np.random.randn(50).cumsum(),'k--')
ax1.hist(np.random.randn(100),bins=20,color='k',alpha=0.3)
ax2.scatter(np.arange(30),np.arange(30)+3*np.random.randn(30))
plt.show()
```
![测试图片2](D:\study\Markdown\Note\Python\img\Figure_2.png)
为了方便批量创建subplot，matplotlib提供了一个更加方便的方法plt.subplots，它返还两个对象，一个是Figure对象，一个是axessubplot对象组成的列表
```
fig,axes=plt.subplots(2,3)
print axes
>>[[<matplotlib.axes._subplots.AxesSubplot object at 0x0000000006CB83C8>
  <matplotlib.axes._subplots.AxesSubplot object at 0x0000000008CBBB38>
  <matplotlib.axes._subplots.AxesSubplot object at 0x0000000008DCB5F8>]
 [<matplotlib.axes._subplots.AxesSubplot object at 0x0000000008E85F28>
  <matplotlib.axes._subplots.AxesSubplot object at 0x0000000008F58BA8>
  <matplotlib.axes._subplots.AxesSubplot object at 0x0000000008EA36D8>]]
```
我们可以利用通过这个方法创建出来的axes轻松地对axes数组进行索引，例如axes[0,1]。并且可以通过sharex和sharey选项指定subplot具有相同的x轴或者y轴界限
详细信息可以参考《利用Python进行数据分析》p235

#####调整subplot周围的间距
默认情况下，matplotlib会在subplot外围留下一定的边距，并在subplot之间留下一定的间距。调整图像时，subplot也会自动调整。
我们可以利用Figure的subplots_adjust方法修改这个间距
```
fig,axes=plt.subplots(2,2)
for i in range(2):
    for j in range(2):
        axes[i,j].hist(np.random.randn(500),bins=50,color='k',alpha=0.5)
plt.subplots_adjust(wspace=0,hspace=0)
plt.show()
```
![](D:\study\Markdown\Note\Python\img\Figure_3.png)

###颜色，标记和线型
plot函数接受一组x和y坐标，还可以接受一个表示颜色和线型的字符串缩写。例如，要根据x和y绘制绿色曲线，可以执行如下代码`axes[1,0].plot(x,y,'g--')`或者`axes[1,0].plot(1,1,linestyle='--',color='g')`常用的颜色都有一个缩写词，要使用不常用的颜色可以通过它的RGB值形式（如'#CECECE')，linestyle的详细信息可以参考plot的文档。

创建线型图时可以加上一些标记，以强调实际的数据点
```
fig,axes=plt.subplots(2,2)
plt.plot(np.random.randn(30).cumsum(),'ko--')
axes[1,0].plot(np.random.randn(30).cumsum(),'k--')
plt.show()
```
![](D:\study\Markdown\Note\Python\img\Figure_4.png)
我们可以明显的看到二者之间的区别，更为明确的写法还有`plt.plot(np.random.randn(30).cumsum(),linestyle='dashed',color='k',marker='o')`
在线型图中，非司机数据点默认会按照线型方式插值，可以通过drawstyle属性进行修改
```
plt.plot(np.random.randn(30).cumsum(),linestyle='dashed',color='k',marker='o',drawstyle='steps-post')
```
![](D:\study\Markdown\Note\Python\img\Figure_5.png)

###刻度，标签和图例
对于大多数图表装饰项，主要实现方式有两个：过程型的pyplot接口以及更为面向对象的原生matplotlib API

首先介绍xlim方法，不加参数它会返回当前的x轴绘图范围，加入一个列表作为参数，则会将x轴的范围调整为对应的值，如`plt.xlim([0,10])`会将x轴的范围设置为0到10.`plt.xlim`针对的是最近创建的或者最后一个使用的AxesSubplot对象，如果要指定特定的对象，我们可以使用特定的AxesSubplot的方法，`ax.get_xlim`或者`ax.set_xlim`

另外，还有xticks，xticklabels之类的方法，它们分别控制图标的刻度位置，刻度标签等。

#####设置标题，轴标签，刻度以及刻度标签
要修改x轴的刻度，最简单的方法是使用set_xticks和set_xticklables。
```
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(np.random.randn(1000).cumsum())
ticks=ax.set_xticks([0,250,500,750,1000])
labels=ax.set_xticklabels(list('abcde'),rotation=30,fontsize='small')
ax.set_title('My plot')
ax.set_xlabel('Stages')
plt.show()
```
![](D:\study\Markdown\Note\Python\img\Figure_6.png)
对于y轴也可以使用同样的方法。
#####添加图例
图例是另一种用于标识图标元素的重要工具，添加图例的方式有两个，最简单的方法是在添加subplot的时候传入label参数：
```
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(np.random.randn(1000).cumsum(),'k',label='one')
ax.plot(np.random.randn(1000).cumsum(),'k.',label='two')
```
然后可以通过ax.legend()或者plt.legend()来自动创建图例
```
ax.legend(loc='best')
```
loc选项表示图例的位置，best会让它找最不碍事的位置。要从图例中去除一个或多个元素，不传入label或者传入`lable='_nolegend_'`即可。
![](D:\study\Markdown\Note\Python\img\Figure_7.png)

###注解以及在Subplot上绘图
text，arrow和annotate等函数支持我们为图表添加注解。text可以将文本绘制在图表的指定坐标（x，y），还可以加上一些自定义的格式
```
ax.text(x,y,'Hello world!',family='monospace',fontsize=10)
```
复杂的注解可以参考《利用Python进行数据分析》p242或者matplotlib的在线示例库

图形的绘制就更加麻烦，这些常见的图形对象，有一些可以在matplotlib.pyplot里面找到，但完整部分位于amtplotlib.patches。

要在图表中添加图形，首先需要创建一个块对象shp，然后通过`ax.add_patch(shp)`将其添加到subplot中
具体信息参考《利用Python进行数据分析》p242

###将图表保存到文件
plt.savefig可以将当前的图表保存到文件，该方法相当于figure对象的实例化方法savefig，假设我们要将图表保存为SVG文件
```
plt.savefig('figpath.svg')
```
该方法两个重要的选项分别是dpi和bbox_inches，前者控制’每英寸点数‘的分辨率，后者可以剪除当前图表周围的空白部分。假设要得到一张带有最小白边，且分辨率为400DPI的PNG图片，代码如下
```
plt.savefig('figpath.png',dpi=400,bbox_inches='tight')
```
savefig除了写入磁盘，还可以写入任何文件对象，比如StringIO（尽管我现在还不知道Python的StringIO是个什么东西，不过姑且先记录下来）
```
from io import StringIO
buffer=StringIO()
plt.savefig(buffer)
plot_data=buffer.getvalue()
```
具体信息可以参考《利用Python进行数据分析》p244

###matplotlib配置
matplotlib自带一些配色方案，以及为生成的图片设定的默认配置信息。我们可以通过一组全局参数来对这些默认行为进行自定义。操作matplotlib配置系统的主要方式有两种，第一种是Python编程方式，通过rc方法，假设，我们要将全局的图像默认大小调整为10*10：
```
plt.rc('figure',figsize=(10,10))
```
rc的第一个参数是希望自定义的对象，如'figure','axes','xtick','ytick','grid','legend'等。其后可以跟上一系列关键字参数，最简单的方法是将这些选项做成一个字典:
```
font_option={
    'family':'monospace',
    'weight':'bold',
    'size':'small'
}
plt.rc('font',**font_option)
```
要了解全部自定义选项，我们可以查阅matplotlib的配置文件matplotlibrc（位于matplotlib/mpl-data目录中）。如果我们对该文件进行自定义并将其放在我们自己的.matplotlib目录中，则每次使用matplotlib都会加载该文件。