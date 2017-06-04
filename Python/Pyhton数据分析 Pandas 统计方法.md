#Python数据分析 pandas 汇总和计算描述统计简述
pandas拥有很多用于约简和统计学的方法

例如sum或者mean
```
fr=pd.DataFrame(np.arange(20).reshape(4,5),index=list('abcd'))
print fr.sum()
print fr.sum(axis=1)
>>0    30
1    34
2    38
3    42
4    46
dtype: int64
a    10
b    35
c    60
d    85
dtype: int64
```
axis选项依然适用

如果对象中有NaN值，它会在计算过程中被忽略，除非整个切片都是NaN或者我们在方法中调用skipna选项使其等于False，后者会让存在NaN值的列或者行进行统计运算后的结果变为NaN
另外，这些方法还拥有一个level选项。当对象的轴为层次化索引（MultiIndex，就是有多个索引轴相互嵌套）时，可以根据level进行分组约简

有些方法返回的是间接统计（比如idxmin表示达到最小值的索引）
```
fr=pd.DataFrame(np.arange(20).reshape(4,5),index=list('abcd'))
print fr.idxmax()
>>0    d
1    d
2    d
3    d
4    d
dtype: object
```

还有一些方法是累计型的
```
fr=pd.DataFrame(np.arange(20).reshape(4,5),index=list('abcd'))
print fr.cumsum()
>>    0   1   2   3   4
a   0   1   2   3   4
b   5   7   9  11  13
c  15  18  21  24  27
d  30  34  38  42  46
```

甚至还有既不是约简型，也不是累计型的，例如describe方法,用于产生多个汇总统计
```
fr=pd.DataFrame(np.arange(20).reshape(4,5),index=list('abcd'))
print fr.describe()
>>               0          1          2          3          4
count   4.000000   4.000000   4.000000   4.000000   4.000000
mean    7.500000   8.500000   9.500000  10.500000  11.500000
std     6.454972   6.454972   6.454972   6.454972   6.454972
min     0.000000   1.000000   2.000000   3.000000   4.000000
25%     3.750000   4.750000   5.750000   6.750000   7.750000
50%     7.500000   8.500000   9.500000  10.500000  11.500000
75%    11.250000  12.250000  13.250000  14.250000  15.250000
max    15.000000  16.000000  17.000000  18.000000  19.000000
```
对于非数值型数据，describe方法还会产生另外一种汇总统计

关于各类统计方法的详细信息，可以查阅《利用Pyhton进行数据分析》p144