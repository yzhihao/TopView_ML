# Python数据分析 合并数据集
pandas对象中的数据可以通过一些内置的方式进行合并：
`pandas.merge`可以根据一个或多个键将不同DataFrame中的行连接起来。
`pandas.concat`可以沿着一条轴将多个对象堆叠到一起
实例方法`combine_first`可以将重复数据编接在一起，用一个对象中的值填充另一个对象中的缺失值。

### 数据库风格的DataFrame合并
数据集的合并(merge)或连接（join）运算是通过一个或多个键将行连接起来的。

先来看merge，在不传入参数的情况下，它会默认将重叠的列名作为键来合并两个DataFrame，而在这个列名下，两个DataFrame的不同值会被抛弃
```python
fr1=pd.DataFrame({
    'a':list('abcd'),
    'b':list('afgb')
})
fr2=pd.DataFrame({
    'b':list('ab'),
    'c':[1,2]
})
print pd.merge(fr1,fr2)
>>
   a  b  c
0  a  a  1
1  d  b  2
```
例子中，b被作为键来连接两个DataFrame，而fr1中b列下的f，g值被抛弃了。
我们可以使用on选项来显式指定要作为键的列，这样子会比较好一些。
若是两个DataFrame的列名不同，我们可以用left_on与right_on选项来进行分别指定。

若是想要不抛弃不同的键进行连接该怎么办呢，事实上，merge默认做的是‘inner’的连接方式，这表示取键的交集，其他方式还有‘left’，‘right’，‘outer’。外连接取的便是键的并集，它组合了‘left’和‘right’连接方式的效果。我们使用how选项来传入这些参数。

对于多对多的连接，pandas会采取笛卡儿积的方式来连接两者，例如一个DataFrame中用来merge的键下有3个‘b’，另外一个DataFrame有2个‘b’值，那么在merge后二者会产生6个‘b’值以及其对应的行以满足所有的连接后可能出现的情况。

要采用多键连接的方式，我们只需要把多个键组成一个列表传给on选项即可，具体的连接效果取决于我们在how选项上传入的连接方式。

关于合并运算，还有一个问题就是对重复列名的处理，merge提供一个suffixes选项，用于指定附加到左右两个DataFrame对象的重叠列名上的字符串。
```python
left1=pd.DataFrame({'key':list('abaabc'),'value':range(6)})
right1=pd.DataFrame({'key':list('bbc'),'value':range(3)})

print pd.merge(left1,right1,on='key',suffixes=("_left","_right"),how="outer")
>>
  key  value_left  value_right
0   a           0          NaN
1   a           2          NaN
2   a           3          NaN
3   b           1          0.0
4   b           1          1.0
5   b           4          0.0
6   b           4          1.0
7   c           5          2.0
```

| 参数 | 说明 |
|--------|--------|
|on|用于连接的列名。必须存在于左右两个DataFrame对象中。如果未指定，且其它连接键也未指定，则以left和right列名的交集作为连接键|
|left_on|左侧DataFrame中用作连接键的列|
|right_on|右侧DataFrame中用作连接键的列|
|left_index|将左侧的行索引用作其连接键|
|right_index|类同left_index|
|sort|根据连接键对合并后的数据进行排序，默认为True。又是在处理大数据集时，禁用该选项可获得更好的性能|
|suffixes|字符串元组，用于追加到重叠列名的末尾，默认为（'_x','_y'）。例如，如果左右两个DataFrame对象都有“data”，则结果中就会出现"data_x","data_y"|
|copy|设置为False，可以在某些特殊情况下避免将数据复制到结果数据结构中。默认总是复制|
有关merge的更多信息，查阅《利用Python进行数据分析》p190

### 索引上的合并
有时候DataFrame的连接键位于其索引中。在这种情况下，可以通过传入`left_index=True`或者`rigth_index=True`（或者两者皆传）以将索引用作连接键：
```python
left1=pd.DataFrame({'key':list('abaabc'),'value':range(6)})
right1=pd.DataFrame({'value':range(7)},index=list('abbcbad'))

print pd.merge(left1,right1,left_on='key',right_index=True,suffixes=("_left","_right"),how="inner")

>>  key  value_left  value_right
0   a           0            0
0   a           0            5
2   a           2            0
2   a           2            5
3   a           3            0
3   a           3            5
1   b           1            1
1   b           1            2
1   b           1            4
4   b           4            1
4   b           4            2
4   b           4            4
5   c           5            3
```
至于层次化索引，像下面这种
```python
left1=pd.DataFrame({'key':list('abaabc'),'key2':list('121231'),'value':range(6)})
right1=pd.DataFrame({'value':range(7)},index=[list('aabbcda'),list('1112233')])

print left1,'\n',right1

>>  key key2  value
0   a    1      0
1   b    2      1
2   a    1      2
3   a    2      3
4   b    3      4
5   c    1      5 
     value
a 1      0
  1      1
b 1      2
  2      3
c 2      4
d 3      5
a 3      6
```
我们则需要通过列表的方式指明用作合并键的多个列（注意对重复索引值的处理）
```python
left1=pd.DataFrame({'key':list('abaabc'),'key2':list('121231'),'value':range(6)})
right1=pd.DataFrame({'value':range(7)},index=[list('aabbcda'),list('1112233')])

print pd.merge(left1,right1,left_on=['key','key2'],right_index=True)

>>  key key2  value_x  value_y
0   a    1        0        0
0   a    1        0        1
2   a    1        2        0
2   a    1        2        1
1   b    2        1        3
```
这个时候，“inner”模式下连接键的匹配模式就会更加严格，只有两个连接键都匹配的值才会被保留下来。

还可以同时使用合并双方的索引，这里就不再赘述。

DataFrame还提供一个** `join`实例方法 **，它能更为方便的实现按索引合并。不仅如此，它还可以用于合并多个带有相同或相似索引的DataFrame对象，而不管它们之间是否有重叠的列。
```python
left1=pd.DataFrame({'value':range(3)},index=list('ace'))
right1=pd.DataFrame({'value':[int(x*10) if x<1 and x>-1 else int(x) for x in np.random.randn(5).flat ]},index=list('abcde'))

print left1,'\n',right1
>>   value
a      0
c      1
e      2 
   value
a      1
b     -4
c     -1
d     -4
e      3

print left1.join(right1,lsuffix='_left',rsuffix='_right',how='outer')

>>   value_left  value_right
a         0.0            1
b         NaN           -4
c         1.0           -1
d         NaN           -4
e         2.0            3
```
DataFrame的join方法是在连接键上做** 左连接 **(left_on)。

它还支持** 参数DataFrame的索引 **跟** 调用者DataFrame的某个列 **之间的连接，同样也是通过on参数实现
```python
left1=pd.DataFrame({'key':list('aabbcc'),'value':range(6)},index=list('gghhjj'))
right1=pd.DataFrame({'key':list('def'),'value':range(3)},index=list('abc'))

print left1,'\n',right1

>>   key  value
g   a      0
g   a      1
h   b      2
h   b      3
j   c      4
j   c      5 
  key  value
a   d      0
b   e      1
c   f      2

print left1.join(right1,on='key',lsuffix='_left',rsuffix='_right')

>>  key_left  value_left key_right  value_right
g        a           0         d            0
g        a           1         d            0
h        b           2         e            1
h        b           3         e            1
j        c           4         f            2
j        c           5         f            2
```
可以发现，`left1`的连接键是'key'，而`right1`的连接键是索引。

我们还可以向`join`函数传入一组DataFrame以实现** 多个DataFrame的合并 **，这组DataFrame常用** 列表 **表示。

### 轴向连接

##### 关于NumPy数组的合并
另一种数据合并运算也被称为连接（concatenation），绑定（binding），或堆叠（stacking）。NumPy有一个用于** 合并原始NumPy数组 **的** concatenation函数 **：
```python
arr = np.arange(12).reshape((3,4))
print arr

>>[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]

print np.concatenate([arr,arr],axis=1)

>>[[ 0  1  2  3  0  1  2  3]
 [ 4  5  6  7  4  5  6  7]
 [ 8  9 10 11  8  9 10 11]]
```

##### 关于pandas对象的合并

对于pandas对象，带有标签的轴能让我们进一步推广数组的连接运算。

pandas提供** `concat`函数 **来让我们对pands对象进行连接操作。
假设我们有三个没有重叠索引的Series：
```python
s1=pd.Series([0,1],index=['a','b'])
s2=pd.Series([2,3,4],index=['c','d','e'])
s3=pd.Series([5,6],index=['f','g'])

print pd.concat([s1,s2,s3])

>>a    0
b    1
c    2
d    3
e    4
f    5
g    6
dtype: int64
```
默认情况下，`concat`在`axis=0`上工作，最终产生一个新的Series。如果传入`axis=1`，则结果就会变成一个DataFrame（`axis=1`表示列）：
```python
s1=pd.Series([0,1],index=['a','b'])
s2=pd.Series([2,3,4],index=['c','d','e'])
s3=pd.Series([5,6],index=['f','g'])

print pd.concat([s1,s2,s3],axis=1)

>>     0    1    2
a  0.0  NaN  NaN
b  1.0  NaN  NaN
c  NaN  2.0  NaN
d  NaN  3.0  NaN
e  NaN  4.0  NaN
f  NaN  NaN  5.0
g  NaN  NaN  6.0
```
从这里我们可以看出，不同于join或者merge，它默认的合并方式是"outer"，在这里，我们可以通过传入参数** `join='inner'` **来得到它们的交集：
```python
s4=pd.concat([s1 * 5,s3])
print s4

>>a    0
b    5
f    5
g    6
dtype: int64

print pd.concat([s1,s4],axis=1) 
print pd.concat([s1,s4],axis=1,join='inner')
>>   
   0    1
a  0.0  0
b  1.0  5
f  NaN  5
g  NaN  6
>>
   0  1
a  0  0
b  1  5
```
我们还可以通过** `join_axes` **指定要在其它轴上使用的索引：
```python
print s1,'\n',s4

>>a    0
b    1
dtype: int64 
a    0
b    5
f    5
g    6
dtype: int64

print pd.concat([s1,s4],axis=1,join_axes=[list('acbg')])

>>     0    1
a  0.0  0.0
c  NaN  NaN
b  1.0  5.0
g  NaN  6.0
```

我们可以使用** keys **参数在连接轴上创建一个层次化索引，以区分参与连接的片段：
```python
print s1,'\n',s3

>>a    0
b    1
dtype: int64 
f    5
g    6
dtype: int64

print pd.concat([s1,s1,s3], keys=['s1','s1(2)','s3'],axis=0)

>>s1     a    0
       b    1
s1(2)  a    0
       b    1
s3     f    5
       g    6
dtype: int64
```

若是沿着`axis=1`使用进行连接，那么keys变回成为DataFrame的列头：
```python
print s1,'\n',s2,'\n',s3
>>a    0
b    1
dtype: int64 
c    2
d    3
e    4
dtype: int64 
f    5
g    6
dtype: int64

print pd.concat([s1,s2,s3], keys=['s1','s2','s3'],axis=1)
>>    s1   s2   s3
a  0.0  NaN  NaN
b  1.0  NaN  NaN
c  NaN  2.0  NaN
d  NaN  3.0  NaN
e  NaN  4.0  NaN
f  NaN  NaN  5.0
g  NaN  NaN  6.0
```
同样的，对DataFrame也有相同的效果：
```python
df1=pd.DataFrame(np.arange(6).reshape(3,2),index=list('abc'),columns=['one','two'])
df2=pd.DataFrame(5+np.arange(4).reshape(2,2),index=list('ac'),columns=['three','four'])

print df1,'\n',df2
>>   one  two
a    0    1
b    2    3
c    4    5 
   three  four
a      5     6
c      7     8

print pd.concat([df1,df2], keys=['df1','df2','df3'],axis=1)
>>  df1       df2     
  one two three four
a   0   1   5.0  6.0
b   2   3   NaN  NaN
c   4   5   7.0  8.0
```
可以发现，在keys参数就算传入了多个列头，也只有对应数量的列头会被使用，"df3"在上面的例子中就被省略掉了。

如果往concat里面传入的是一个** 字典 **，那么** 字典的键 **就会被当作keys选项的值：
```python
print pd.concat({'level1':df1,'level2':df2},axis=1)
>>  level1     level2     
     one two  three four
a      0   1    5.0  6.0
b      2   3    NaN  NaN
c      4   5    7.0  8.0
```
此外，还可以传入** names参数 **可以为列头编名：
```python
print pd.concat({'level1':df1,'level2':df2},axis=1,names=['line1','line2'])
>>line1 level1     level2     
line2    one two  three four
a          0   1    5.0  6.0
b          2   3    NaN  NaN
c          4   5    7.0  8.0
```
如果DataFrame行索引与分析工作无关，我们可以传入** `ignore_index=True` **来使其无效化:
```python
print df1,'\n',df2
>>   one  two
a    0    1
b    2    3
c    4    5 
   three  four
a      5     6
c      7     8

print pd.concat({'level1':df1,'level2':df2},axis=0,names=['line1','line2'])
print pd.concat({'level1':df1,'level2':df2},axis=0,names=['line1','line2'],ignore_index=True)
>>line1  line2                       
level1 a       NaN  0.0    NaN  1.0
       b       NaN  2.0    NaN  3.0
       c       NaN  4.0    NaN  5.0
level2 a       6.0  NaN    5.0  NaN
       c       8.0  NaN    7.0  NaN
       
>>   four  one  three  two
0   NaN  0.0    NaN  1.0
1   NaN  2.0    NaN  3.0
2   NaN  4.0    NaN  5.0
3   6.0  NaN    5.0  NaN
4   8.0  NaN    7.0  NaN
```

concat函数参数一览表（详细内容可查阅《利用python进行数据分析》p198）

| 参数 | 说明 |
|--------|--------|
|    objs    |    参与连接的pandas对象的列表或字典。唯一必须参数    |
|axis|指明连接的轴向，默认为0|
|join|选项为“inner”，“outer”其中之一，默认“outer”。指明其它轴向上的索引是按交集（inner）还是并集（outer）进行合并|
|join_axes|指明用于其它n-1条轴的索引，不执行并集/交集运算|
|keys|与连接对象有关的值，用于形成连接轴上的层次化索引。可以是任意的列表或者数组，元组数组，数组列表（如果将levels设置成多级数组的话）|
|levels|指定用作层次化索引各级别上的索引，如果设置了keys的话|
|names|用于创建分层级别的名称，如果设置了keys和（或）levels的话|
|verify_integrity|检查结果对象新轴上的重复情况，如果发现则引发异常。默认（False）允许重复（但实际上我在编写的时候发现，它的值貌似默认为True）|
|ignore_index|不保留连接轴上的索引，产生一组新索引range（total_range）|

### 合并重叠数据

当我们有索引全部或者部分重叠的两个数据集的时候，使用merge或者concatenation就难以进行处理了。

一个方法是用NumPy提供的`where`函数：
```python
a=pd.Series([np.nan,2.5,np.nan,3.5,4.5,np.nan],index=list('fedcba'))
b=pd.Series(np.arange(len(a),dtype=np.float64),index=list('fedcba'))
b[-1]=np.nan

print a,'\n',b
>>f    NaN
e    2.5
d    NaN
c    3.5
b    4.5
a    NaN
dtype: float64 
f    0.0
e    1.0
d    2.0
c    3.0
b    4.0
a    NaN
dtype: float64

print np.where(pd.isnull(a),b,a)
>>[ 0.   2.5  2.   3.5  4.5  nan]
```
例子中的`np.where(pd.isnull(a),b,a)`表示构建一个从a和b中取值的ndarray，当a中的值为NaN时，取b中的值，否则取a中的值。

Series有一个combine_first方法，实现的也是一样的功能，并且会进行数据对齐：
```python
print a,'\n',b
>>f    NaN
e    2.5
d    NaN
c    3.5
b    4.5
a    NaN
dtype: float64 
f    0.0
e    1.0
d    2.0
c    3.0
b    4.0
a    NaN
dtype: float64

print b[:-2].combine_first(a[2:])
>>a    NaN
b    4.5
c    3.0
d    2.0
e    1.0
f    0.0
dtype: float64
```
在上面的例子中，我们可以看到，combine_first表示以b[:-2]为主构建一个Series，然后对于其中缺失的对象，用a[2:]中的值来弥补。

对于DataFrame，combine_first自然也会在列上做同样的事情，因此我们可以将其看作：用参数对象中的数据为调用者对象的缺失数据“打补丁”：
```python
df1=pd.DataFrame({'a':[1,np.nan,2,np.nan,3],'b':['a','b',np.nan,'c','d']})
df2=pd.DataFrame({'a':[3,4,5,np.nan,6],'b':[np.nan,'g','e','c','d']})

print df1,'\n',df2
>>     a    b
0  1.0    a
1  NaN    b
2  2.0  NaN
3  NaN    c
4  3.0    d 
     a    b
0  3.0  NaN
1  4.0    g
2  5.0    e
3  NaN    c
4  6.0    d

print df1.combine_first(df2)
>>     a  b
0  1.0  a
1  4.0  b
2  2.0  e
3  NaN  c
4  3.0  d
```
