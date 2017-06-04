#Python数据分析 pandas函数应用和映射
NumPy的unfuncs也可以用于操作pandas对象（ufuncs表示元素级数组方法，它包括很多方法，而不是一个名为‘unfuncs’的方法）

DataFrame对象具有一个apply方法，可以将函数应用到各行或者各列所形成的一维数组上（类似于map（）函数，只不过一是apply是针对DataFrame对象的，二是用作apply的参数的函数只能有一个参数，这个参数代表的是DataFrame里的整个行或者整个列）
```
def func(x):
    return x*2
def func2(x):
    return x.max()
ar1=np.arange(20).reshape((4,5))
frame=pd.DataFrame(ar1,columns=list('abcde'))
print frame.apply(func)
print frame.apply(func2)
>>    a   b   c   d   e
0   0   2   4   6   8
1  10  12  14  16  18
2  20  22  24  26  28
3  30  32  34  36  38
>>a    15
b    16
c    17
d    18
e    19
```
而要使apply应用于列，只需要传入axis参数指定要应用于的轴就好

除了标量值，传递给apply的函数也可以返回有多个值组成的Series
```
def func(x):
    return pd.Series([x.max(),x.min()],index=list('ab'))
ar1=np.arange(20).reshape((4,5))
frame=pd.DataFrame(ar1,columns=list('abcde'))
print frame.apply(func)
>>    a   b   c   d   e
a  15  16  17  18  19
b   0   1   2   3   4
```

DataFrame还提供一个applymap函数，往applymap函数里传递一个函数，则可以让这个函数作用于DataFrame里的所有元素，例如传入一个`return x*x`的函数，DataFrame里面的所有元素就会进行平方运算。

此外，DataFrame还提供一个map函数，往它传入一个函数可以对DataFrame的某一列进行遍历
```
def func(x):
    return x*x
ar1=np.arange(20).reshape((4,5))
frame=pd.DataFrame(ar1,columns=list('abcde'))
print frame['b'].map(func)
>>0      1
1     36
2    121
3    256
Name: b, dtype: int64
```
不过这个地方把map换成apply结果也是一样的



