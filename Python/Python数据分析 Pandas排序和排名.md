#Pyhton 数据分析 pandas 排序和排名
###排序
要对Series的索引进行排序，我们可以使用sort_index方法,它将会把索引按照字典顺序排序
```
se=pd.Series(range(5),index=list('bceda'))
print se.sort_index()
>>a    4
b    0
c    1
d    3
e    2
dtype: int64
```
而要排序DataFrame的话，可以通过传入axis参数来表示要排序的轴，老样子，0表示行，1表示列
往里面传入参数ascending=False参数，还可以使的索引按字典顺序降序排序（可见ascending值默认为True）

要按值对Series进行排序的话，可以使用order方法，与sort_index并没有多大的区别

在排序时，所有的缺失值（NaN）都会被放在Series的末尾

在DataFrame上对值进行排序的话还是使用sort_index方法，不过我们需要将要设为排序标准的索引名字传入到方法的by选项中
```
frame=pd.DataFrame({'a':[1,2,3,4],'b':[7,6,9,3]})
print frame.sort_index(by='b')
>>   a  b
3  4  3
1  2  6
0  1  7
2  3  9
```
也可以给by传入索引组成的列表以根据多个索引进行排序。
列表中索引的顺序表示排列时优先照顾的索引的顺序。

###排名
排名函数rank与排序关系密切，它的作用是返回各个元素排序后的排名。
```
se=pd.Series([22,40,22,1,61,7])
print se.rank()
>>0    3.5
1    5.0
2    3.5
3    1.0
4    6.0
5    2.0
dtype: float64
dtype: float64
```
在rank里用method选项可以改变排名的方式，例如，可以通过method=‘first’选项使rank返还值在原数据中出现的顺序的排名。

传入ascending=False的选项则可以选择降序排名

同样，对于DataFrame，可以用axis选项指定应用的轴

method选项有这么几种：
average		默认选项，在相等分组中为各个组分配平均排名
min 		使用整个分组最小的排名
max			使用整个分组最大的排名
first		按值在原始数据中出现的顺序进行排名

