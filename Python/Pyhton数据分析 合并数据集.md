#Python数据分析 合并数据集
pandas对象中的数据可以通过一些内置的方式进行合并：
`pandas.merge`可以根据一个或多个键将不同DataFrame中的行连接起来。
`pandas.concat`可以沿着一条轴将多个对象堆叠到一起
实例方法`combine_first`可以将重复数据编接在一起，用一个对象中的值填充另一个对象中的缺失值。

###数据库风格的DataFrame合并
数据集的合并(merge)或连接（join）运算是通过一个或多个键将行连接起来的。

先来看merge，在不传入参数的情况下，它会默认将重叠的列名作为键来合并两个DataFrame，而在这个列名下，两个DataFrame的不同值会被抛弃
```
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

有关merge的更多信息，查阅《利用Python进行数据分析》p190

###索引上的合并

