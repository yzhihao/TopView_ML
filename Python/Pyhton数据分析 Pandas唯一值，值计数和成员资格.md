#Python数据分析 唯一值，值计数和成员资格

###唯一值
要计算一个Series中的唯一值，需要用到unique方法，它会返还一个Series中的唯一值数组
```
fr=pd.DataFrame({'a':[1,2,2,4],'b':[2,3,1,1]})
print fr['a'].unique()
>>[1 2 4]
```

###值计数
value_counts方法用于对Series中的值进行计数，可以通过sort选项来决定是否返还排序后的对象
```
fr=pd.DataFrame({'a':list('adhfuixocjaaaskhdncahdfuioenfalsdpap')})
print fr['a'].value_counts(sort=False)
>>a    7
c    2
e    1
d    4
f    3
i    2
h    3
k    1
j    1
l    1
o    2
n    2
p    2
s    2
u    2
x    1
Name: a, dtype: int64
```

###唯一值
isin方法用于判断矢量化集合的成员资格，简单的说，就是判断对象中的元素是否在指定的列表里面
```
fr=pd.DataFrame({'a':list('facbs')})
print fr.isin(['a','b'])
>>       a
0  False
1   True
2  False
3   True
4  False
```
有关三个方法的具体参考信息，可以查阅《利用Python进行数据分析》p148