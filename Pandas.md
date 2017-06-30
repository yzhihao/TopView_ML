# Pandas


* [Pandas 对象](#Pandas 对象)
	* [Series](#Series)
	* [DateFrame](#DateFrame)
	* [索引对象](#索引对象)
* [操作](#操作)
	* [广播](#广播)
	* [函数](#函数)
	* [处理缺失值](#处理缺失值)
	* [排序](#排序)
	* [重复的轴索引](#重复的轴索引)
	* [统计方法](#统计方法)




## Pandas 对象
### Series
#### 类似于一个一维数组按列摆放，左边是索引(索引默认是自然数)，右边是数据。若传入对象是字典，则默认键是索引，值是数据(默认数据类型为object)。
#### 创建方法

- Series(data = [],index = [])/Series([]/{})

```python
In[2]:import pandas as pd # 若pandas安装成功，在ipython中引入pandas会有下面这句话
Backend MacOSX is interactive backend. Turning interactive mode on.
In[3]:from pandas import DataFrame,Series
# 以上都是约定成俗的引入方法
In[4]:series\_1 = Series([1,2,3])
In[5]:series\_1
Out[5]:
In[5]:series\_1
Out[5]:
0    1
1    2
2    3
dtype: int64
#左边是索引从0开始，右边是元素的值
In[6]:series\_2 = Series({'Name':'Chok','Class':'4','Age':'19'})
In[7]:series\_2
Out[7]:
Age        19
Class       4
Name     Chok
dtype: object
# 显然若传入的是字典，则按照了索引的大小排序
# 当然你可以自己替换索引，直接对Series.index赋值。Series默认的索引方式为
# RangeIndex(start=0, stop=4, step=1)
# 因此也可以用range对index赋值

In[8]: series\_3 = Series({'Name':'Chok','Class':'4','Age':'19'},index = ['Name','Class','weight'])
In[9]: series\_3
Out[9]:
Name      Chok
Class        4
weight     NaN
dtype: object
# 若替换有字典生成的Series对象的索引时，新索引和字典的键相匹配的值会找出来，未找到的值结果为NAN(可以用isnull()、notnull()判断数据是否缺失)
```

#### name属性

- Series/Series.index还有name属性,可以直接通过赋值去修改


- - -

### DateFrame
#### DataFrame是一个表格型的数据结构，既有行索引，也有列索引（表头）
<br/>
#### 创建方法DataFrame()

- 传入一个由 键- 数组/列表/元组 组成的字典,每个序列变成一列
- - 由Series组成的字典，每个Series变成一列（如没有显式的指定索引，则各Series索引合并的结果作为行索引）
- 传入二维ndarray(**传入的元素都是值**，如有需要，你可以传入索引)
- 由字典或Series组成的列表
- 由字典组成的字典

```python
In[10]:import numpy as np
# 键 - 列表 组成的字典
In[11]:df1 = DataFrame({'a':[1,2,3],'b':[4,5,6],'c':[7,8,9]},index = ,'f'])
In[12]: df1
Out[12]:
   a  b  c
d  1  4  7
e  2  5  8
f  3  6  9
# 二维ndarray
In[13]: df2 = DataFrame(np.arange(16).reshape(4,4),index = ['a','b','c','d'],	columns = ['e','f','g','h'] )
In[14]:df2
out[14]:
    e   f   g   h
a   0   1   2   3
b   4   5   6   7
c   8   9  10  11
d  12  13  14  15
#由Series组成的列表
In[15]:df3 = DataFrame([Series([1,2,3]),Series([1,2,3]),Series([1,2,3])])
Out[15]:
   0  1  2
0  1  2  3
1  1  2  3
2  1  2  3
# 传入嵌套字典，外面的key变成列索引，里面的Key变成行索引
In[16]: df4 = DataFrame({'1':{'Name':'Lee','Class':'4','Age':'19'},'2':{'Name':'Chok','Class':'3','Age':'19'},'3':{'Name':'John','Class':'2','Age':'19'}})
In[17]: df4
Out[17]:
         1     2     3
Age     19    19    19
Class    4     3     2
Name   Lee  Chok  John

```

#### DateFrame.reindex(index,fill\_value = NAN,method = , column = )


#### 删除操作

- 使用DataFrame.drop([index...])可以删除特定轴以及它的值
- 使用Series.drop([index...])可以删除特定轴以及轴上的值

#### 索引、选取和过滤

- DataFrame索引是获取列,
- DataFrame切片是选取行，不包括末尾而Series的切片是**包含末尾**的
- DataFrame、Series都可以可以用条件索引（实质是用布尔型数组进行索引）
- 用DataFrame.ix([column,[index]])可以选取第colomn列，第index行
- Series可以通过给定的索引值(默认会有自然数索引存在，即使显示的修改了index)

#### DataFrame数据对齐

- 若存在不同索引对，则结果为的索引是运算双方索引的并集，并且对；令不重叠的索引值为NAN
- 与Series一样，若使用DF1.add(DF2,fill\_values = )可以设置缺失值

- - -

### 索引对象
#### 每个DataFrame和Series都有一个index(DataFrame还有colums对象），index对象不可修改

- index对象的实质是把构建DataFrame和Series的那些数组和其他序列转化成一个numpy数组

#### 多重索引

- 使用DataFrame.set\_index(keys, drop=True, append=False, inplace=False, verify\_integrity=False)设置多重索引
- 可以用ix来索引也可以用[:,:,key]来使用内层索引来获取索引值
- swaplevel(,)可以交换两个索引的层次(level)


```python

In[18]: df5 = df4.T
In[19]: df5.index.name = 'NO.'
In[20]: df6 = df5.set\_index([df5['Age'],[1,1,1],[1,2,3],df5['Age'],df5.index])
In[21]: df6
Out[21]:
	             Age Class  Name
Age     Age NO.
19  1 1 19  1     19     4   Lee
      2 19  2     19     3  Chok
      3 19  3     19     2  John
# 外层索引（左边为外），从第一个不是重复的索引开始，里面的索引会全部显示
# 若要用特定的索引则要用DataFrame.xs(key , level = )(level=0是最外层即最左边)
In[22]: df6.ix(2,level = 2)
out[22]:
               Age Class  Name
Age   Age NO.
19  1 19  2     19     3  Chok

```
<br/>
<br/>
#### 列与行索引转化

- 用set\_index()传入一列，可以把列变成行索引，默认删除该行，若想保留则令drop=False即可
- reset\_index()功能与set\_index相反

## 操作

### 广播

- 当Series和DataFrame 列数或行数相等时，两者运算会广播

- - -

### 函数

- numpy的函数可以操作pandas例如 np.abs(df2)
- DataFrame.apply(func,axis = )可以对按某一轴**(只有0和1，0是对每列，1是对每行)**使用函数
- DataFrame.applymap()用法与apply类似，但操作的对象是**元素**而不是某一**行或列**

- - -
### 处理缺失值
#### 判断是否有缺失值

- isnull()、notnull()

#### 处理

- #### DateFrame.reindex(index,fill\_value = NAN,method =  )

	- 该方法可以重新设置索引，若索引值当前不存在，则引入缺失值（fill\_value）
	- method可以设置如何填充（ffill/pad）向前填充/搬运值，(bfill/backfill)后向填充/搬运值

- #### 去除缺失值DateFrame.dropna(axis = ,how = ,thresh = ,)

	- axis 是选定轴，只有0或1
	- how 可以传入 all 或 any all指的是如果该行**全部是NAN**则删除该行，any则是该行**有一个NAN**都会删除该行
	- thresh 给一个整数，若该行非NAN数据个数小于给的数，则删除该行

- #### DataFrame.fillna(value = )
	- 把NAN替换为value

- - -
### 排序
#### 对索引/列名排序

- sort\_index(axis = ，ascending = True) 当axis=0时，对行索引排序，当axis=1对列名排序,默认升序，若要降序令ascending = False即可


#### 对值排序

- Series.sort\_values(axis=0, ascending=True,inplace = False, kind='quicksort', na\_position='last'）
	-   axis 选择轴
	-   ascending 升序(True)还是降序(False)
	-   若inplace=True则**对自身排序**，**不产生副本**，反之...嗯嗯
	-   kind 选择排序方式默认快排，可选的有'mergesort'归并, 'heapsort'堆排
	-   na\_position 让NAN值放在头部('first')还是末尾(默认)
- DataFrame.sort\_values([str,..],axis=0, ascending=True, kind='quicksort', na\_position='last')
	- [str,...] 传入列名，对某一列排序
	-   axis 选择轴
	-   ascending 升序(True)还是降序(False)
	-   若inplace=True则**对自身排序**，**不产生副本**，反之...嗯嗯
	-   kind 选择排序方式默认快排，可选的有'mergesort'归并, 'heapsort'堆排
	-   na\_position 让NAN值放在头部('first')还是末尾(默认)
- DataFrame.rank(axis=0, method=’average’, numeric\_only=None, na\_option=’keep’, ascending=True, pct=False)
	- rank**不关心数值，只关心某一行或列的数值之间大小关系**
	- axis 选取轴 **0 或 1**
	- method 默认为average，**负责处理数值相同情况下的排名**
		- average 当数值一样时则排名会取平均，如两个值相同的时候且排名为x时，两个的排名会变成x.5
		- max 使分组排名最大
		- min 使分组排名最小
		- first 按出现先后排名
	- np\_option **处理NAN值的排名**
		- 'keep' 忽略NAN值
		- 'top' 把NAN值看成是第一
		- 'bottom' 把NAN看成排名最后的
	- ascending 升序或降序
	- pct 把排名变成0-1范围内


```python
In[23]: frame  = DataFrame({'b':[4.3,7,-3,2],'a':[0,1,0,1],'c':[-2,5,8,-2.5]})
In[24]: frame
Out[24]:
   a    b    c
0  0  4.3 -2.0
1  1  7.0  5.0
2  0 -3.0  8.0
3  1  2.0 -2.5
In[25]: frame.rank(axis = 0 ，method = 'average')
Out[25]:
     a    b    c
0  1.5  3.0  2.0
1  3.5  4.0  3.0
2  1.5  1.0  4.0
3  3.5  2.0  1.0

In[26]: frame.rank(axis = 0,method='max')
Out[26]:
     a    b    c
0  2.0  3.0  2.0
1  4.0  4.0  3.0
2  2.0  1.0  4.0
3  4.0  2.0  1.0

In[27]: frame.rank(axis = 0,method='min')
Out[27]:
     a    b    c
0  1.0  3.0  2.0
1  3.0  4.0  3.0
2  1.0  1.0  4.0
3  3.0  2.0  1.0

In[28]: frame.rank(axis = 0,method='first')
Out[28]:
     a    b    c
0  1.0  3.0  2.0
1  3.0  4.0  3.0
2  2.0  1.0  4.0
3  4.0  2.0  1.0

```

- - -
### 重复的轴索引

- 若每个轴索引互异，则Series索引的对象为标量值，否则返回一个Series,DataFrame 类似

- - -

### 统计方法
| 方法 | 描述 |
|--------|--------|
| count |非NA的数量        |
|describe|针对Series或DataFrame的各列进行汇总统计|
|min/max|求最值|
|argmin/argmax|求最值的索引位置(只能用于Series)|
|idmin/idmax|求最值的索引值|
|quantile|求样本分位数|
|sum|求和|
|mean|求平均数|
|median|求中位数|
|mad|根据平均值计算**平均绝对离差**（还不懂）|
|var|求方差|
|std|标准差|
|skew|样本值的**偏度**（还不懂）|
|kurt|样本值的**峰度**（还不懂）|
|cumsum|累计和|
|cummin/cummax|累计最小/最大值|
|cumprod|累计积|
|diff|计算**一阶差分**（还不懂）|
|pct\_change|计算百分数变化（两项差比上前项）|
#### 相关系数
 - 使用Series.corr(Series)即可计算出相关系数(DataFrame的每一列都是一个Series)
 - DataFrame.corrwith()可以计算其列或行跟另一个Series或DataFrame的相关系数

#### 唯一处理
- 用Series.unique()可获得没有排序的、元素互异的Series

#### 统计值的出现次数
- pd.value\_counts(Serise.values,sort) Series的值会变成索引，出现次数为索引值

#### 是否包含某些元素
- Serise/DataFrame.isin([values...]) 返回一个都是布尔值的DataFrame,若对应元素在values中有，则为True



