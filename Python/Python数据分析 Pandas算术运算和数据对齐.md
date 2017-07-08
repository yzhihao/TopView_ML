#Python数据分析 pandas算术运算和数据对齐

pandas对象相互之间可以实现算术运算，进行算术运算的时候，如果索引相同，会在相同索引对应的值之间进行算术运算，有不同索引时，不同的索引会被并入结果集，它们的值会编程NaN。

而对于DataFrame，算术运算时，行和列都会进行对齐操作

###在算术方法中填充值
如果，我们不希望在pandas对象进行算术运算时，出现NaN，就可以使用这些数据结构自带的方法来代替算术运算符，并通过在这些方法中多传入一个fill_value参数来指定填充NaN的值。
```
se1=pd.Series(np.arange(5))
se2=pd.Series([4,4,4])
print se1+se2
print se1.add(se2,fill_value=0)
>>
0    4.0
1    5.0
2    6.0
3    NaN
4    NaN
dtype: float64
0    4.0
1    5.0
2    6.0
3    3.0
4    4.0
dtype: float64
```
此外，还有sub（减法）div（除法）mul（乘法）

###DataFrame和Series之间的运算
首先我们来看一下简单的'广播'
```
ar1=np.arange(20).reshape((4,5))
print ar1
print ar1[0]
print ar1-ar1[0]
>>[[ 0  1  2  3  4]
 [ 5  6  7  8  9]
 [10 11 12 13 14]
 [15 16 17 18 19]]
>>[0 1 2 3 4]
>>[[ 0  0  0  0  0]
 [ 5  5  5  5  5]
 [10 10 10 10 10]
 [15 15 15 15 15]]
```
这种情况就叫做广播，目前作者还没有详细讲解，这里引入只是为了启发DataFrame和Series之间是如何进行算术运算的。

首先，在进行运算时，Series的索引对应的是DataFrame的columns，如果想让Series的索引对应DataFrame的行，则需要调用运算方法add/sub等等，并在其中传入axis参数，表示在算术运算时希望二者相互匹配的轴，当axis=0时，对应的就会是行。

