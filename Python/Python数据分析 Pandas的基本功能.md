#Pyhton数据分析 Pandas的基本功能

###重新索引
reindex方法可以让pandas对象拥有一个新的索引，传入fill_value参数，可以让生成的pandas对象自动给缺失值补完
```
data = {
    'name': ['a', 'b', 'c', 'd'],
    'hits': [1, 2, 3, 4],
    'like': [0, 1, 2, 3]
}
frame = pd.DataFrame(data, columns=['name', 'hits', 'like'], index=['a', 'b', 'c', 'd'])
print frame
frame=frame.reindex(['a','b','c','d','e'])
print frame
frame=frame.reindex(['a','b','c','d','e'],fill_value=0)
print frame
>>  name  hits  like
a    a     1     0
b    b     2     1
c    c     3     2
d    d     4     3
  name  hits  like
a    a   1.0   0.0
b    b   2.0   1.0
c    c   3.0   2.0
d    d   4.0   3.0
e  NaN   NaN   NaN
  name  hits  like
a    a   1.0   0.0
b    b   2.0   1.0
c    c   3.0   2.0
d    d   4.0   3.0
e  NaN   NaN   NaN
```
如果重新索引中传入的索引列表包含元素少于原来的DataFrame，那么生成的DataFrame会直接截去少的那一部分

在重新索引时传入method参数，可以选择一些方法，像是'ffill'方法就可以对时间序列这样的有序数据进行前（我感觉这里有应该是‘后’，但是书上写的是’前‘）向值填充的插值处理
```
data = {
    'name': ['a', 'b', 'c', 'd'],
    'hits': [1, 2, 3, 4],
    'like': [0, 1, 2, 3]
}
frame = pd.DataFrame(data, columns=['name', 'hits', 'like'], index=[0,2,4,6])
print frame
frame=frame.reindex(range(8),method='ffill')
print frame
>>  name  hits  like
0    a     1     0
2    b     2     1
4    c     3     2
6    d     4     3
  name  hits  like
0    a     1     0
1    a     1     0
2    b     2     1
3    b     2     1
4    c     3     2
5    c     3     2
6    d     4     3
7    d     4     3
```
除了把ffill和pad传给method进行前向填充（或搬运）值之外，还有bfill或者backfill选项支持后向填充（或搬运）值。

往reindex方法里卖弄传入columns参数可以对DataFrame的列项进行重排
```
data = {
    'name': ['a', 'b', 'c', 'd'],
    'hits': [1, 2, 3, 4],
    'like': [0, 1, 2, 3]
}
frame = pd.DataFrame(data, columns=['name', 'hits', 'like'], index=[0,2,4,6])
print frame.reindex(columns=[0,'name',4])
>>    0 name   4
0 NaN    a NaN
2 NaN    b NaN
4 NaN    c NaN
6 NaN    d NaN
```
也可以再引入index参数同时对列项与索引进行修改，但是method方法只能够按行应用，因此紧跟index之后
```
frame2=frame.reindex(index=[0,1,2,3],method='ffill',columns=['a','b'])
```
利用ix的标签索引功能，重新索引任务可以变得更加简洁
```
frame2=frame.ix[[0,1,2,3],['a','b']]
```
更多关于reindex的内容可以查阅《利用Python进行数据分析》p129

###丢弃指定轴上的项

丢弃某条轴上的一个或多个项需要调用pandas对象的drop方法
对于Series，可以通过往drop方法里传入单个索引或者索引组成的列表来删除对应的值
```
se=pd.Series(np.arange(5.),index=[0,1,2,3,4])
print se
print se.drop(1)
>>
0    0.0
1    1.0
2    2.0
3    3.0
4    4.0
dtype: float64
0    0.0
2    2.0
3    3.0
4    4.0
dtype: float64
```
而对于DataFrame则可以通过传入要删除的索引组成的列表来删除索引上对应的所有值，也可以通过传入列项的名以及axis参数（表示列所在的轴）来删除整个一列
```
data = {
    'name': ['a', 'b', 'c', 'd'],
    'hits': [1, 2, 3, 4],
    'like': [0, 1, 2, 3]
}
frame = pd.DataFrame(data, columns=['name', 'hits', 'like'], index=[0,2,4,6])
print frame.drop([0,2])
print frame.drop(['hits'],axis=1)
print frame.drop(['name','hits'],axis=1)
>>  name  hits  like
4    c     3     2
6    d     4     3
  name  like
0    a     0
2    b     1
4    c     2
6    d     3
   like
0     0
2     1
4     2
6     3
```
实际上，不指定axis的值时axis默认为0，表示轴0

###索引/选取/过滤

Series的切片不同于Numpy的数组，它在进行切片时，：后面的内容也是包含的，不过仅限于自定义的索引，如果没有自定义索引，切片时就不会包含后面的
```
se=pd.Series(np.arange(4),index=[0,2,4,6])
se2=pd.Series(np.arange(4))
print se[0:2]
print se2[0:2]
>>0    0
2    1
dtype: int32
0    0
1    1
dtype: int32
```
但是，要是传入的索引列表与默认列表产生的索引顺序是一样的，那么切片时同样也不会有包含末端的效果。

DataFrame同样可以进行切片，不同的是，直接以列表形式访问，访问的是列，用切片的形式访问，就会访问到行，而且对于索引，它还支持使用布尔型数组选取行。
```
data = {
    'name': ['a', 'b', 'c', 'd'],
    'hits': [1, 2, 3, 4],
    'like': [0, 1, 2, 3]
}
frame = pd.DataFrame(data, columns=['name', 'hits', 'like'], index=[0,2,4,6])
print frame[['name','hits']]
print frame[[0,2]]
print frame[:2]
>>  name  hits
0    a     1
2    b     2
4    c     3
6    d     4
  name  like
0    a     0
2    b     1
4    c     2
6    d     3
  name  hits  like
0    a     1     0
2    b     2     1
print frame[frame['hits']>3]
>>  name  hits  like
6    d     4     3
```
需要注意的是，对于自定义索引，DataFrame的切片效果和Series是一样的，都是末端包含。

DataFrame在各项都是相同类型的时候，他还可以像ndarray一样被处理。

要在DataFrame上进行行标签索引，有专门的索引字段ix
```
data = {
    'name': ['a', 'b', 'c', 'd'],
    'hits': [1, 2, 3, 4],
    'like': [0, 1, 2, 3]
}
frame = pd.DataFrame(data, columns=['name', 'hits', 'like'], index=[0,2,4,6])
print frame.ix[0:2,:2]
>>  name  hits
0    a     1
2    b     2
```
ix后的中括号里，第二个位置可以用来表示选定的列，也可以为空，表示选定所有列。

关于DataFrame的其它索引选项，可以参考《利用Python进行数据分析》p132




