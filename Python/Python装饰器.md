# Pyhon 装饰器
* [从函数参数说起](#从函数参数说起)
* [几个关于函数的基本概念](#几个关于函数的基本概念)
* [闭包](#闭包)
* [装饰器](#装饰器)
* [类装饰器](#类装饰器)
* [内置的装饰器](#内置的装饰器)


## 从函数参数说起
- ### 位置参数（普通参数）

	- 顾名思义，参数的传递与参数的位置有关

```python
In[2]:def fun1(a,b,c):
		print(c)
		print(b)
		print(a)

In[3]:fun1(3,2,1)
1
2
3

```

- ### 默认参数

	- 若没有传入参数则取预先设置好的默认值
	- 默认参数降低了调用函数的难度
	- 默认参数的默认值应该为不可改变对象，否则默认值有可能会被改变

```python
In[3]:def fun2(a=1,b=2,c=3):
    print("a = " + str(a))
    print("b = " + str(b))
    print("c = " + str(c))

In[4]:fun2()
a = 1
b = 2
c = 3

# 若只传入部分参数，则按位置传给相应的变量
In[5]:fun2(5,4)
a = 5
b = 4
c = 3

# 若想直接改变特定的值可以直接把值赋给对应的变量
In[6]:fun2(b=7)
a = 1
b = 7
c = 3

```

- ### 可变参数
	- 可传入若干个参数
	- 实际传进来的是由若干个参数组成的元祖

```python
In[7]:def fun3(*numbers):
		sum = 0
		for i in numbers:
			sum = sum + i
		print(sum)

In[8]:fun3(1,2,3)
6
# 若想把元祖/列表当做参数传进来，只需在元祖/列表前加个 *
In[9]:fun3(*[4,5,6])
15

```


- ### 关键字参数
	- 可传入任意个关键字参数
	- 实际上是传入了由关键字参数组成的字典

```python
In[10]:def fun4(**kw):
    print(kw)

In[11]:fun4(name = 'chok',Age = 19)
{'name': 'chok', 'Age': 19}

# 同理若想传入字典作参数，在字典前加 ** 即可
In[12]:fun4(**{'name':'chok','Age':19})
{'name': 'chok', 'Age': 19}
```

- ### 参数定义的顺序
	- 必选参数、默认参数、可变参数和关键字参数

## 几个关于函数的基本概念

- ### 高阶函数

	- 一个函数就可以接收另一个函数作为参数，这种函数就称之为高阶函数。

<br/>

- ### 嵌套函数

	- 在一个函数内定义另一个另一个函数，里面的函数叫作内层函数

<br/>

- ### 变量解析规则
	- L （Local） 局部作用域
E （Enclosing） 闭包函数外的函数中
G （Global） 全局作用域
B （Built-in） 内建作用域
以 L --> E --> G -->B 的规则查找，即：在局部找不到，便会去局部外的局部找（例如闭包），再找不到就会去全局找，再者去内建中找。


- ### 变量的作用域

	- 每个函数有自己的命名空间，函数会优先在自己的命名空间里寻找变量(所以当函数与外部有同名的变量时会屏蔽了外部变量)
	- 一句话总结，局部变量会屏蔽外部变量

```python
In[13]:x = 10
In[14]:def fun6():
		x = 5
		print(x)
In[15]:fun6()
5

In[16]:var = 10
In[17]:def fun7():
		  var = var + 1
		  return var

In[18]:print fun7()
UnboundLocalError: local variable 'var' referenced before assignment
局部变量引用前没有定义，报错的原因是函数中的var属于局部变量，而局部变量没有定义就直接进行自增操作，若想在函数内使用与外部作用域同名的变量，可以使用 global 关键字

In[19]:def fun7():
    global var
    var = var + 1
    return var
In[20]:print fun()
2
In[21]:print var
2
# 可以看到var可以在函数内被修改，并且全局作用域的 var 的值也被修改（因为 global 关键字让 Python 在全局作用域去找变量 var ），如果在其他函数不加 global 关键字修改 var ，仍然会报错

若想在内部函数修改外部函数的变量用 nonlocal (python 3)
In[22]:x = 10
In[23]:def fun8():
		x = 5
		def fun9():
			nonlocal x
			x = x + 10
			print("inner:", x)
		fun9()
		print("outer:", x)

In[24]:fun8()
inner: 3
outer: 3

python2 没有nonlocal关键字，但可以把 x 放进容器类型就可以有同样的效果

nonlocal 是让 python 在函数的局部作用域之外去寻找变量
global 是让 python 在全局作用域去找变量
```



- ### 变量的生存周期

	-  一般定义在函数内的变量会随着函数调用的结束而被销毁(形成闭包除外)

<br/>



## 闭包

- 闭包是由函数及其相关的引用环境组合而成的实体(即：闭包=函数+引用环境)

```python
In[25]:def fun5(x = 1):
    def fun6(y):
        print(x*y)
        return
    return fun6

# x = 3 （引用环境）与fun6()(函数) 一同组成闭包
In[26]:a = fun5(3)
In[27]:a(3)
9

```

## 装饰器

- 装饰器的原理其实就是闭包，高阶函数利用闭包，把引用环境与传入的函数组成的闭包当作新函数返回
- 装饰器的好处在于增大了代码的重用率，而语法糖避免了再一次赋值操作


```python
例如在你执行完输入操作之后打印时间
import time

def now():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

def print_time(func):
    def newfunc():
        func()
        now()
    return newfunc


@print_time
def input_message():
    text = input()
    print(text)

# 上下两种的效果是等效的 @func 其实就是 newfunc = func(newfunc)

"""
def input_message():
    text = input()
    print(text)

input_message = print_time(input_message)
"""

若有多个语法糖，例如：
@a
@b
@c
def func():
	pass

等价于 func = a(b(c(func)))

装饰器可以带参数（传入参数也可以为类）
def a(arg):
	def add(func):
		def newfunc():
			print(arg)
			func()
		return newfunc
	return add
其实质是先返回装饰器的装饰器，再用来装饰函数

如果要装饰带参数的函数 那么在newfunc(*arg,**kwarg),内层函数调用func(*arg,**kwarg)




```

### 装饰器有副作用

```python
In[28]:input_message.__name__
Out[28]: 'newfunc'
# 上例中函数的命名发生了改变，可以用functools.wraps消除这个影响，wraps可以把原函数的元信息传给新函数

import functools
def print_time(func):
	@functools.wraps(func)
    def newfunc():
        func()
        now()
    return newfunc

```



## 内置的装饰器
- ### @property
	- property把类方法改成类属性，实现存取器

```python
In[29]:class C:
		@property
		def x(self):
			return self.__x
		@x.setter
		def x(self, value):
			self.__x = value
		@x.deleter
		def x(self):
			del self.__x

In[30]:a = C()
In[31]:a.x = 100
In[32]:a.x
Out[32]: 100
In[33]:del a.x

同一属性的名字必须一样，用property实现set的方法较于在 __init__()设置x属性的一个比较显著的优点是，前者可以进行限制输入
```


- ### @classmethon
	- 可以用来定义类方法
	- 类方法是指不用实例就可以掉用的方法

```python
In[34]:class A(object):
    @classmethod
    def printA(cls):
        print("A")

In[35]:A.printA()
A
```

- ### @staticmethod
	- staticmethod 主要是方便将外部函数集成到类体中
	- 用staticmethod包装的方法可以内部调用,也可以通过类访问或类实例化访问

```python
def printB():
	print("B")

class B():
	def func(self):
		printB()
		pass

上面可以写成这样

class B():
	@staticmethod
	def printB():
		print("B")

	def func(self):
		self.printB()
		pass

用 @staticmethod 把printB()写进类里就可以用self.printB(),B.printB(),实例对象.B.printB()直接调用printB()

```