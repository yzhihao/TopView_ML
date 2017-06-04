#Python数据分析 pandas中的绘图函数
###线型图
Series和DataFrame都有一个用于生成各类图表的plot方法，默认情况下，它们会生成线型图。
Series在调用plot方法时，它的索引会被传给matplotlib，并用于绘制x轴，我们可以通过use_index=False选项来禁用这个功能。x轴的刻度和界限可以通过xticks和xlim选项进行调节，同样，y轴就是yticks和ylim。


pandas的大部分绘图方法都提供一个可选的ax参数，它可以是一个matplotlib的subplot对象。

DataFrame的plot方法则会在一个subplot中为各列绘制一条曲线，并自动创建图例。

详情可参考《利用Python进行数据分析》p246到p247
###柱状图
在生成线型图的代码中加入kind='bar'（垂直柱状图）或者kind='barh'（水平柱状图）选项即可生成对应的柱状图。
Series和DataFrame的索引将会被用作x刻度或者y刻度
利用stacked=True选项可以创建堆叠柱状图
详细信息参考《利用Python进行数据分析》p248
###直方图和密度图
要绘制直方图，我们可以通过pandas对象的hist方法
```
tips['tip_pct']=tips['tip']/tips['total_bill']
tips['tip_pct'].hist(bins=50)
```
与此相关的另一种图标类型是密度图，它是通过调用plot方法里的kind='kde'选项生成的。密度图是通过计算“可能会产生观测数据的连续概率分布的估计”来产生的，简单的说，就是表示一组数据在某个刻度上的密度。
直方图与密度图往往会混合使用。
更多详细信息，可以参考《利用Python进行数据分析》p252

###散布图
散布图主要是用来观察两个一维数据序列之间的关系。他通过matplotlib的scatter方法来绘制。

pandas提供了一个更为方便的，能从DataFrame创建散布图矩阵的scatter_matrix函数，它还支持在对角线上放置各变量的直方图和密度图。