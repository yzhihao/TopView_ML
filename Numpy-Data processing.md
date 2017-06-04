#Python 数据分析 NumPy数据处理

###将条件逻辑表述为数组运算
numpy.where函数是三元表达式x if contidition else y的矢量化版本，假设我们有三个数组
```
x=np.array([1,2,3,4,5])
y=np.array([-1,-2,-3,-4,-5])
cond=np.array([True,False,True,True,False])
print np.where(cond,x,y)
```
我们设置一个条件，即将x与y与cond相比较，当cond为true值的时候取x值，否则取y值，为了达成这个条件，我们就可以使用where方法，结果如下：
```
>>[ 1 -2  3  4 -5]
```
where中填x与y的地方事实上不一定非要填数组，填标量也是可以的，它表示与cond数组相同维度的全标量数组,甚至是拿来生成一些全某值数组
```
print np.where(np.zeros(10)==0, 2, 2)
>>[2 2 2 2 2 2 2 2 2 2]
```
它可以将一些数组循环简化。

###数学和统计方法
其实就是利用函数实现的统计方法，包括：

sum	对数组中全部或某轴向元素求和
mean 算数平均数
std, var 分别是标准差和方差
min， max 求最小最大值
argmin， argmax 最小最大元素的索引
cumsum 所有元素的累计和
sumprod 所有元素的累计积

mean和sum这类函数称为聚合运算，结果会生成一个少一维的数组，而cumsum，cumprod这类方法则不聚合，产生一个有中间结果组成的数组。

###用于布尔型数组的方法

布尔值在上面这些统计方法中往往会被强制转换为1和0，因此，sum也可以用来统计布尔型数组中的True的数量。

另外还有any和all，any用于测试数组是否存在一个或多个True，all用于检查数组中的值是不是全部为True.它们也可以用于非布尔型数组，所有的非0元素会被当作True

###排序

与python内置列表一样，ndarray也可以通过sort方法进行排序，而对于多维数组，将轴编号传给sort方法即可。使用np.sort()会产生一个数组已排序后的副本，直接调用数组的sort方法这会该变原数组。

###唯一化以及其它的集合逻辑

这是一些针对一维ndarray的基本集合运算。最常用的是np.unique，用于找出数组中的唯一值，并返回已排序的结果，实际上就是去除重复的值。
```
array=np.array([1,1,1,2,3,2,3])
print np.unique(array)
>>[1 2 3]
```
np.in1d则用于测试一个数组另一个数组中的成员资格，返回一个布尔型数组
```
array=np.array([1,1,1,2,3,2,3])
print np.in1d(array,[1,2])
>>[ True  True  True  True False  True False]
```

###将数组以二进制格式保存到磁盘
np.save,np.load分别用于写读磁盘数组数据。默认情况下，数组以未压缩的原始二进制格式保存在扩展名为.npy的文件中。
```
arr=np.arange(10)
np.save('array_file',arr)
```
文件名末尾若是没有带扩展名.npy则会被自动加上。
使用np.savez可以将多个数组保存到一个压缩文件中，只需要将数组以关键字形式传入。
```
np.savez('multiarray_file',a=arr,b=arr2)
```
然后读的时候就像字典一样调用关键字
```
arr=np.load('multiarray_file')
print arr['a']
```

###存取文本文件

np.loadtext和np.genfromtxt能够将数据加载到numoy数组中
```
arr=np.loadtext('array.txt',delimiter=',')
```
表示读取时元素之间的分隔为逗号。
np.savetxt则相反，genfromtxt与loadtext差不多，关于他们之间的区别暂时还没有学到。

###线性代数

说白了，其实就是numpy提供的用于线性代数运算层面的一些方法。
dot函数用于计算矩阵点积。
还有一些其它的线性代数运算方法，这里不再赘述。

###随机数生成
除了randn函数，还有不同类型的随机数生成方法，用到的时候再进行查阅即可。

