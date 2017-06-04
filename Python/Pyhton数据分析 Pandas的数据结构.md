#Pyhton 数据分析 Pandas的数据结构

Pandas有两个最主要的数据结构，分别是Series和DataFrame
###Series
Sreies类似于一维数组，由索引和值组成。
```
import pandas as pd

se=pd.Series([5,6,7,8])
print se
>>
0    5
1    6
2    7
3    8
dtype: int64
```
其中0-3就是对应内容的索引。可以通过调用values和index属性来分别显示它的值和索引，不仅如此，我们还可以给series添加自定义的索引
```
se=pd.Series([5,6,7,8],index=['a','b','cc','ddd'])
print se
>>
a      5
b      6
cc     7
ddd    8
dtype: int64
```
访问单个数据的时候可以像dict一样调用，访问多个的时候就可以使用索引组成的列表
```
se=pd.Series([5,6,7,8],index=['a','b','cc','ddd'])
print se['ddd']
>>8
print se[['a','b','cc','ddd']]
>>a      5
b      6
cc     7
ddd    8
```
甚至还保留了numpy的运算方式,可以把它当作一维的ndarray参与numpy运算并且运算结果依然会和相应索引链接在一起。
```
se=pd.Series([5,6,7,8],index=['a','b','cc','ddd'])
print se[se>6]
>>cc     7
ddd    8
dtype: int64
```
还可以当作定长的有序dict，并且能够参与到许多要用到dict作参数的函数
```
se=pd.Series([5,6,7,8],index=['a','b','cc','ddd'])
print 'a' in se
>>True
```
在创建Series时，dict可以作为参数放进构造函数，从而直接创建相应的series，如果加上了index参数，那么就会根据作为index参数的列表中的值与传入的字典的键进行比较，index里有而字典的键中没有的会把这个值作为NaN的索引。
```
di={'a':1,'b':2,'c':3,'d':4}
se=pd.Series(di,index=['a','b','cc','ddd'])
print se
>>a      1.0
b      2.0
cc     NaN
ddd    NaN
dtype: float64
```
NaN在pandas中表示缺失或者NA值。而Missing和NA则在pandas中用于表示缺失的数据。pandas的isnull和notnull可以用于检测缺失数据
```
di={'a':1,'b':2,'c':3,'d':4}
se=pd.Series(di,index=['a','b','cc','ddd'])
print pd.isnull(se)
print pd.notnull(se)
>>a      False
b      False
cc      True
ddd     True
dtype: bool
>>a       True
b       True
cc     False
ddd    False
dtype: bool
```
Series一个很厉害的地方就在于，它可以在算术运算中自动对齐不同索引的数据
```
di={'a':1,'b':2,'c':3,'d':4}
se=pd.Series(di,index=['a','b','cc','ddd'])
se2=pd.Series([5,6,7,8],index=['a','g','b','c'])
print se
print se2
print se+se2
>>a      1.0
b      2.0
cc     NaN
ddd    NaN
dtype: float64
a    5
g    6
b    7
c    8
dtype: int64
a      6.0
b      9.0
c      NaN
cc     NaN
ddd    NaN
g      NaN
dtype: float64
```
我一开始以为这个是指打印出来的时候对齐，实际上作者表示的是运算的时候对齐，就像相加时让两个series的索引相同的链接的值相加，索引不同的就会继承到新series里面。

series对象本身及其索引都有一个name属性，该属性与pandas的其他功能有相当大的关系
```
se.name='Number'
se.index.name='Alphabet'
print se
>>
Alphabet
a      1.0
b      2.0
cc     NaN
ddd    NaN
Name: Number, dtype: float64
```
series的索引还可以通过直接赋值的方式修改，不像dict，一旦创建就是固定的
```
di={'a':1,'b':2,'c':3,'d':4}
se=pd.Series(di,index=['a','b','cc','ddd'])
print se
se.index=[1,2,3,4]
print se
>>a      1.0
b      2.0
cc     NaN
ddd    NaN
dtype: float64
>>1    1.0
2    2.0
3    NaN
4    NaN
dtype: float64
```

###DataFrame
DataFrame是一个表格型数据结构，它含有一组有序的列，每列的数据类型可以是不同的，作者说它的内部结构的技术细节远超当前书本讨论的范围，暂且不必深究，个人感觉，像是小型的数据库表。

构建DataFrame最常用的方法是直接传入一个由等长列表或NumPy的ndarray组成的字典
```
data={
    'name':['a','b','c','d'],
    'hits':[1,2,3,4],
    'like':[0,1,2,3]
}
frame=pd.DataFrame(data)
print frame
>>   hits  like name
0     1     0    a
1     2     1    b
2     3     2    c
3     4     3    d
```
可以在创建时指定columns参数来指定列项的顺序
```
data={
    'name':['a','b','c','d'],
    'hits':[1,2,3,4],
    'like':[0,1,2,3]
}
frame=pd.DataFrame(data,columns=['name','hits','like'])
print frame
>>  name  hits  like
0    a     1     0
1    b     2     1
2    c     3     2
3    d     4     3
```
可以传入一个列表作为index参数来修改每个字段的索引，传入columns时，发现有找不到的数据会以NaN显示
```
data={
    'name':['a','b','c','d'],
    'hits':[1,2,3,4],
    'like':[0,1,2,3]
}
frame=pd.DataFrame(data,columns=['name','hits','like','Nothing'],index=['a','b','c','d'])
print frame
>>  name  hits  like Nothing
a    a     1     0     NaN
b    b     2     1     NaN
c    c     3     2     NaN
d    d     4     3     NaN
```
调用columns属性和index属性时也可以直接访问相应的列项或者索引的信息列表。

通过类似于访问dict的方法访问某一列的项，可以将DataFrame的列获取为一个Series
```
data={
    'name':['a','b','c','d'],
    'hits':[1,2,3,4],
    'like':[0,1,2,3]
}
frame=pd.DataFrame(data,columns=['name','hits','like','Nothing'],index=['a','b','c','d'])
print frame['name']
print frame.hits
>>a    a
b    b
c    c
d    d
Name: name, dtype: object
a    1
b    2
c    3
d    4
Name: hits, dtype: int64
```
返回的Series拥有原来的DataFrame的索引，而且其name属性也会被相应的修改。DataFrame的行也可以通过位置或名称进行访问，不过需要调用到索引字段ix
```
data={
    'name':['a','b','c','d'],
    'hits':[1,2,3,4],
    'like':[0,1,2,3]
}
frame=pd.DataFrame(data,columns=['name','hits','like','Nothing'],index=['a','b','c','d'])
print frame.ix['a']
>>name         a
hits         1
like         0
Nothing    NaN
Name: a, dtype: object
```

DataFrame的列还可以通过赋值的方式直接进行批量修改，也可以通过把一个长度相同的列表或者ndarray赋值给它进行批量修改。
如果赋值给它的是Series，它还可以精确匹配DataFrame的索引，而空位依然会被填上缺失值
```
data={
    'name':['a','b','c','d'],
    'hits':[1,2,3,4],
    'like':[0,1,2,3]
}
se=pd.Series([5,6,7,8],index=['a','bb','c','b'])
frame=pd.DataFrame(data,columns=['name','hits','like','Nothing'],index=['a','b','c','d'])
frame['Nothing']=se
print frame
>>  name  hits  like  Nothing
a    a     1     0      5.0
b    b     2     1      8.0
c    c     3     2      7.0
d    d     4     3      NaN
```
为不存在的列赋值可以创建出一个新列，还可以用关键字del删除列
```
data = {
    'name': ['a', 'b', 'c', 'd'],
    'hits': [1, 2, 3, 4],
    'like': [0, 1, 2, 3]
}
frame = pd.DataFrame(data, columns=['name', 'hits', 'like'], index=['a', 'b', 'c', 'd'])
frame['NewColumn'] = frame['name']=='a'
print frame
>>  name  hits  like NewColumn
a    a     1     0      True
b    b     2     1     False
c    c     3     2     False
d    d     4     3     False
del frame['NewColumn']
print frame
>>  name  hits  like
a    a     1     0
b    b     2     1
c    c     3     2
d    d     4     3
```

还有一种创建DataFrame的方法就是传入嵌套字典，外层字典的键会作为列，内层的键会作为行索引。
创建时，内层字典的键会被合并，并排序称为最终的索引，如果用index参数显式指定索引则不会这样

DataFrame支持转置功能，用法如frame.T

传入Sreries和传入字典的功能差不多

DataFrame的index和columns属性分别都具有各自的name属性，如果对其进行设置，那么它们将会显示出来。

DataFrame也具有values属性，调用时它会以ndarray的形式返回DataFrame中的数据
```
data = {
    'name': ['a', 'b', 'c', 'd'],
    'hits': [1, 2, 3, 4],
    'like': [0, 1, 2, 3]
}
frame = pd.DataFrame(data, columns=['name', 'hits', 'like'], index=['a', 'b', 'c', 'd'])
frame['NewColumn'] = frame['name']=='a'
print frame.values
>>[['a' 1L 0L True]
 ['b' 2L 1L False]
 ['c' 3L 2L False]
 ['d' 4L 3L False]]
```
因为各列的数据类型可能会不一样，所以调用values属性返还的ndarray会尽可能使用所有列都能够兼容的数据类型

###索引对象

pandas的索引对象（index）负责管理轴标签和其他元素。构建Series和DataFrame的时候，所用到的任何数组或者其它序列的标签都会被转换成一个索引

索引对象无法修改，它的不可修改性使得index对象能够在多个数据结构之间安全共享。

索引和columns都支持`xx in frame.columns`或者`xx in frame.index`的用法

索引还拥有一些特殊的方法以及属性，这里不再赘述，详细内容可以查阅资料——《利用Pyhton进行数据分析》p126。


