# Numpy

<br />

## ndarray

* [组成](#组成)
* [基本属性](#基本属性)
* [创建方法](#创建方法)
* [对数组的操作](#对数组的操作)
	* [轴变换](#轴变换)
	* [切片](#切片)
	* [索引](#索引)
	* [ufunc](#ufunc)

<br/>

- ### 组成

	- 一个指向数组的**指针**
	- 数据类型或dtype
	- 表示形状（shape）的元组
	- 一个**跨度元组**（stride）

<br/>

- ### 基本属性

	1. shape
		- 表示ndarray的形状，再用reshape时必须要保证**ndarray大小一致**
	2. dtype
	 	- 表示ndarray的数据类型(下面是**dtype体系**)
	 		- **generic**
	 			- **number**
	 				- **integer**
	 					- **unsigned int**
	 					- **signed int**
	 				- **inexact**
	 					- **floating**
	 					- **complex**
	 			- **charcter**
	 				- **string_**
	 				- **unicode_**
	 			- **bool**
	 			- **object**

	3. **秩**（rank）
		- 表示ndarray的**维数**
	4. **轴**（axes）
		- **数值上等于维数**，Numpy中每一个线性的数组称为是一个轴

<br/>

- ### 创建方法

	- 用numpy的函数创建

		|  函数名  |  				简介   |
		|--------|--------|
        |array|从列表、元祖、字典或其他数组中创建|
		|    ones/zeros    |   根据给定的形状（传入shape元祖）创建一个全1/0的数组     |
        |ones\_like/zeros\_like|根据给定的数组创建一个全1/0的数组（**dtype为float**）    |
        |arange|与range相似|
		|eye/identity|创建一个对角线为1的矩阵**（eye创建的矩阵可以不为方）**|
        |empty/empty\_like|根据给定的形状（数组）创建一个空数组**（元素随机无意义）**|

	```python
	 In[2: arr1 = np.arange(2,20,2).reshape((3,3))
     """用arange创建一维数组通过用reshape改变数组形状"""
	In[3]: arr1
	Out[3]:
    array([[ 2,  4,  6],
     		[ 8, 10, 12],
   		  [14, 16, 18]])
    In[4]: arr2  = np.ones((2,2))
    """传入一个表示shape的元组即可"""
	In[5]: arr2
	Out[5]:
	array([[ 1.,  1.],
       	  [ 1.,  1.]])
	In[6]: arr3 = np.ones\_like(arr2)
    """传入一个数组，按照该数组形状创建"""
	In[7]: arr3
	Out[7]:
	array([[ 1.,  1.],
    	     [ 1.,  1.]])
	"""np.eye(N,M,K,dtype)参数分别是 行，列，1的初始位置，类型"""
    """np.identity(N,dtype)参数只有维度和类型"""

	```
<br/>

-  ### 对数组的操作

	- #### 轴变换

		1. 简单转置可以直接**ndarray.T**实现（默认按 **axis = 0** 进行轴变换,在transpos（）参数中相当于各轴的位置向前一位，第一位到最后，即transpose（0，1，2）变为transpose（1，2，0））
        2. ndarray.transpose()接受由**轴编号组成的元组**(各个轴按你所给的顺序排列）,**Ps:元素轴编号默认为（0，1，2..,n-1）n为维数)**
        	- 例如对三维数组 **ndarray.transpose(2,1,0)**其结果为:设某元素的索引**[x,y,z]**转置后该元素的索引变为**[z,y,x]**
    	3. ndarray.swapaxes(axis1, axis2) 交换两个轴的元素
    	 	- 个人觉得，这个和上一个本质是一样的，但是不用考虑所有的轴的顺序，在数组维度较高，转置情况不是很复杂的情况下会比较便利吧

    - #### 切片

    	- 个人觉得这个没什么好说的，切片的方法和Python列表切片是一样的

    - #### 索引

    	1. 可以用ndarray[x][y]或ndarray[x,y]的形式（后者相当于传入一个元组）
    	2. 用布尔数组作为索引，即ndarray[boolArray]选取元素
    	3. 用逻辑运算作索引，ndarray[condition],还有一个**np.where(condition,x,y)**这个与三目运算符 condition？x:y很像，也可以**嵌套使用**
		4. 传入**整数**列表或数组索引特定行子集，例：ndarray[[0,1]]，结果为第0行和第1行
		5. take/put函数
			- np.take(ndarray,indices,axis = None)
			- np.put(indices,replace)该函数只能用于一维C顺序进行索引，不接受axis参数，replace可以是一个数或者列表、数组，可用于替换索引的目标的值

    - #### ufunc
    	| 一元函数 | 简介 |
		|--------|--------|
		|abs/fabs|计算绝对值，对于非复数值，fabs会更快|
        |sqrt | 计算每个元素的平方根，相当于 ndarray \*\* 0.5 |
        |square| 计算每个元素的平方|
        |exp|计算以每个元素为幂e为底的指数值|
        |log/log10/log1p|计算以e/10/1+x底数的对数值|
        |sign|符号函数|
        |ceil|取大于等于该元素的最小整数|
        |floor|取小于等于该元素的最大整数|
        |rint|四舍五入到最接近的整数，保留dtype|
        |modf|将数组的小数和整数部分以两个独立数组的形式返回|
        |isnan|返回一个表示“哪些值为NaN”的布尔型数组|
        |isfinite/isinf|分别返回一个表示“哪些元素是有穷的”/“哪些元素是无穷的”的布尔数组|
        |cos/cosh/sin/sinh/tan/tanh|三角函数和双曲三角函数|
        |arccos/arccosh/arcsin...略|反三角函数|
        |logical\_not|计算各元素 not x 的真值。|

        | 二元函数 | 简介 |
        |--------|--------|
        |  add |  将数组对应元素相加 |
        |subtract|前减后（对应元素相减）|
        |multiply|对应元素相乘|
        |divide/floor\_divide|对应元素除法/地板除法运算|
        |power|第一个数组的元素A作为底数，第二个素组的元素B作为幂，**求A^B^**|
        |maximum/fmax|取对应元素中的最大值，fmax忽略NAN|
        |minimum/fmin|取对应元素中的最小值，fmin忽略NAN|
        |mod|对应元素求模运算|
        |copysign|将第二个数组的符号赋给第一个数组(**变为浮点数**)|
        |greater/greater\_equal|相当于>/>=**(结果为布尔数组)**|
		|less/less\_equal|相当于</<=**(结果为布尔数组)**|
        |equal/not\_equal|相当于=/!=**(结果为布尔数组)**|
        |logical\_and/logical\_or/logical\_xor|对应元素进行真值逻辑运算,相当于&/｜/^**(结果为布尔数组)**|

        | 统计函数 | 简介 |
        |--------|--------|
        |   sum   |    按某一轴进行求和，若不给出哪条轴，则对整个数组元素求和 **（零长度的数组sum = 0）**  |
        |mean|算术平均数。**（零长度的数组 mean = 0）**|
        |std/var|分别为标准差和方差，**自由度默认为n**|
        |min/max|求最小值/最大值|
        |argmin/argmax|求最小值/最大值的**索引**|
        |cumsum|求所有元素的累计和**(若不输入轴参数，则返回的是一维数组)**|
        |cumprod|求所有元素的累计积**(若不输入轴参数，则返回的是一维数组)**

        对于布尔数组来说，在使用以上的函数时会强制把**True变为1**，**False变为0**.
	- 还有两个检查数组真值的函数all()和any()(可以用于非布尔数组)

		|基本集合运算|简介|
    	|-------|------|
    	|unique(x)|计算x中的唯一元素，并返回有序结果|
   	 |intersect1d(x,y)|计算x和y中的公共元素，并返回有序结果|
   		|union1d(x,y)|计算x和y的并集，并返回有序结果|
        |in1d(x,y)|得到“x中的元素是否包含于y”的布尔型数组|
        |setdiff1d(x,y)|集合的差运算|
        |setxor1d(x,y)|集合的对称差|
