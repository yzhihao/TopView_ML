#Python数据分析 层次化索引
层次化索引是pandas中用于使我们能在一个轴上拥有多个索引级别的功能。
```
fr=pd.Series(np.random.randn(10),index=[list('aaabbbccdd'),[1,2,3,1,2,3,1,2,2,3]])
print fr
>>a  1   -0.157751
   2    0.778736
   3    1.120575
b  1    1.748541
   2   -0.217136
   3   -0.946823
c  1   -0.608329
   2   -0.954161
d  2    0.208304
   3   -0.982254
dtype: float64
print fr.index
>>MultiIndex(levels=[[u'a', u'b', u'c', u'd'], [1, 2, 3]],
           labels=[[0, 0, 0, 1, 1, 1, 2, 2, 3, 3], [0, 1, 2, 0, 1, 2, 0, 1, 1, 2]])
```
选取外层索引的子集操作和一般Series没有什么不同，选取内层索引，则只需用逗号隔开各层索引
```
fr=pd.Series(np.random.randn(10),index=[list('aaabbbccdd'),[1,2,3,1,2,3,1,2,2,3]])
print fr[:,2]
print fr[:,2]['b']
>>a   -0.523473
b    0.511955
c   -2.083303
d    1.804689
dtype: float64
0.511955479469
```
选取的方式相当灵活，但是貌似不支持['a':'c',2]这样子的切片选取方法

pandas还提供unstack方法，可以将两层索引的Series重排进一个DataFrame里面

同样，也存在stack方法，将DataFrame转换成多层索引的Series

对于DataFrame，行索引和列索引也都可以多层嵌套，创建方式和Series差不多，各层也否可以拥有name属性,不过多层嵌套的索引拥有的name属性是以names属性表现的
```
fr=pd.DataFrame(np.random.randn(20).reshape(4,5),index=[list('aabb'),[1,2,1,2]],columns=[list('cccdd'),list('abcab')])
fr.index.names=['key1','key2']
print fr
>>                  c                             d
                  a         b         c         a         b
key1 key2
a    1    -1.207696  1.260584 -0.284607 -1.204646 -0.244008
     2     0.854973 -1.727643 -0.877260  0.728352 -0.016798
b    1    -0.200260 -0.458197  1.183761 -0.739128 -1.800985
     2     0.075847  0.839821  0.120497  2.317037 -1.064695
```

###重排分级顺序
swaplevel接受两个级别编号或者名称（name），并且会返回一个互换了级别的新对象
```
fr=pd.DataFrame(np.random.randn(20).reshape(4,5),index=[list('aabb'),[1,2,1,2]],columns=[list('cccdd'),list('abcab')])
fr.index.names=['key1','key2']
print fr.swaplevel('key1','key2')
>>                  c                             d 
                  a         b         c         a         b
key2 key1 
1    a    -1.075107  0.997531  2.004566 -2.646746 -0.012401
2    a    -0.165994  1.440311 -0.171438 -0.822785  2.345702
1    b     0.556042 -0.721212 -0.769366  1.188816  1.275480
2    b    -0.136807  0.763399 -0.762648  0.323841 -0.603887
```
用sortlevel方法可以根据单个级别中的值对数据进行稳定排序，通过传入要排序的那一层索引的编号，来决定以哪一层索引为基准进行排序。
```
fr=pd.DataFrame(np.random.randn(20).reshape(4,5),index=[list('aabb'),[1,2,1,2]],columns=[list('cccdd'),list('abcab')])
fr.index.names=['key1','key2']
print fr.swaplevel('key1','key2').sortlevel(0)
>>                  c                             d          
                  a         b         c         a         b
key2 key1                                                  
1    a    -1.522876  0.721193  1.056498 -0.536550  0.765929
     b    -0.208658 -0.695901  1.619974 -0.700645  0.831490
2    a     1.699870  0.801962  0.439141  0.318605  0.621213
     b    -0.616935  0.839226 -1.111081 -0.798160  1.139739

```

###根据级别汇总统计
其实就是指前面的sum方法中level选项的用途，在这里就很明晰了，通过指定一个数值给level选项，使sum方法明白自己要统计哪一层索引的值。

###使用DataFrame的列
pandas提供set_index方法将DataFrame的部分列索引转换成行索引
```
fr=pd.DataFrame({
    'a':list('abcdefg'),
    'b':range(7,0,-1),
    'c':list('aaabbbb'),
    'd':[0,1,2,0,1,2,3]
})
print fr
print fr.set_index(['c','d'])
>> a  b  c  d
0  a  7  a  0
1  b  6  a  1
2  c  5  a  2
3  d  4  b  0
4  e  3  b  1
5  f  2  b  2
6  g  1  b  3
>>   a  b
c d
a 0  a  7
  1  b  6
  2  c  5
b 0  d  4
  1  e  3
  2  f  2
  3  g  1
```
它会返还一个新的DataFrame而不是在原来的DataFrame上进行修改，默认情况下，被修改为行索引的那些列会在新的DataFrame中被移除，但也可以通过drop=False选项，来保留他们

reset_index的功能则恰好相反，它会把层次化索引变回列索引