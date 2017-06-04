#Python数据分析 Pandas处理缺失数据
numpy.nan对象，即NaN值，是pandas用于表示其数据结构中的缺失值的对象。在pandas的数据结构中，所有的缺失数值以及python内置的None值都会被当作NaN处理。

可以参考《利用Python进行数据分析》p149来详细了解NaN的处理方法

###滤除缺失数据
要去除一个Series中的缺失数据，dropna方法和布尔型索引series.notnull()都可以达到相同的目的
```
fr=pd.Series([1,3,3,np.nan,5,np.nan])
print fr
print fr.dropna()
print fr[fr.notnull()]
>>0    1.0
1    3.0
2    3.0
3    NaN
4    5.0
5    NaN
dtype: float64
0    1.0
1    3.0
2    3.0
4    5.0
dtype: float64
0    1.0
1    3.0
2    3.0
4    5.0
dtype: float64
```

但是对于DataFrame，则会比较复杂。
直接使用dropna它会丢弃所有含NA的行，传入选项how='all'则只丢弃全部为NA的行，传入axis选项，则可以指定匹配的轴，如果想留下指定数量的数据则可以通过thresh选项
```
fr=pd.DataFrame({'a':[1,2,np.nan,3,np.nan,4],'b':[2,3,np.nan,3,5,4]})
print fr
print fr.dropna(thresh=2)
>>     a    b
0  1.0  2.0
1  2.0  3.0
2  NaN  NaN
3  3.0  3.0
4  NaN  5.0
5  4.0  4.0
     a    b
0  1.0  2.0
1  2.0  3.0
3  3.0  3.0
5  4.0  4.0
```
thresh后面的数值表示我们希望留下来的数据中非缺失数据的数量，像是例子中，就表示保留具拥有两个数据的行。

###填充缺失数据
若是不想丢弃缺失数据，我们可以使用fillna方法来传入我们希望在缺失数据上填充的数据，它可以接受一个标量或者一个字典来对缺失数据进行填充，并且可以通过inplace选项，来决定是返还新对象还是在原来的对象的基础上进行修改。

具体使用方法可以参考《利用Pyhton进行数据分析》p152


