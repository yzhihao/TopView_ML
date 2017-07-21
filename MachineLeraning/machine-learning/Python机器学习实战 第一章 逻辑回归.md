# Python机器学习实战 第一章 逻辑回归

资料来源参考：
人民邮电出版社 Peter Harrington《机器学习实战》第五章
[数据集来源 Github:Peter Harrington](https://github.com/pbharrin/machinelearninginaction)
本章数据集来源：Ch5

## 步骤

构建一个逻辑回归模型有以下几步：
1. 收集数据：采用任意方法收集数据
2. 准备数据：由于需要进行距离计算，因此我们要求数据类型为**数值型**。若是结构化数据格式更佳
3. 分析数据：采用任意方法对数据进行分析
4. 训练算法：大部分时间将用于训练，训练的目的是为了找到最佳的分类回归系数
5. 测试算法：训练步骤完成后将对算法进行测试
6. 使用算法：首先我们需要输入一些数据，并将其转换成对应的结构化数值；接着，基于训练好的回归系数就可以对这些数值进行简单的回归运算，判定它们属于哪个类别；在这之后，我们就可以在输出的类别上做一些其它的分析工作。

## 逻辑回归的适用范围

逻辑回归适用于二元分类，因此，我们这次的这组数据的预测值仅有0和1（其它类型的数值也没关系，但都以0，1表示会比较方便）分别代表二元分类中的negative class 和 possitive class。

## 算法模型

### 选择输入函数：sigmoid函数

因为我们已经确定是逻辑回归模型（若是未知模型的数据我们还需要从头推导模型），所以作为分类器的输出函数我们选择逻辑函数，又称sigmoid函数：

![](\img\mla1-1.png)

我们将sigmoid函数的输入$$$θ^Tx$$$记为z，z由下面这个公式导出：

$$
z=w_0x_0+w_1x_1+w_2x_2+...+w_nx_n\\
向量写法:z=w^Tx，可以看出sigmoid函数中的θ便是w
$$

显然，x便是我们的输入变量。

### 选择优化算法：梯度上升法

作为第一次训练，我们选择比较简单的参数更新方法：梯度上升法，它细分为两种，一种是精度比较高但消耗比较大的批梯度上升法：

![](\img\mla1-2.png)

还有一种是随机梯度上升法：

![](\img\mla1-3.png)

## 训练算法

首先让我们先观察一下我们的数据集：

![](img\mla1-4.png)

数据集导入和输出代码：

```python
from numpy import *
from matplotlib import pyplot as plt

def loadDataSet():
    dataMat=[]
    labelMat=[]
    fr = open(r'data\mlia\Ch05\testSet.txt')
    for line in fr.readlines():
        lineArr=line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

figure=plt.figure()
ax=figure.add_subplot(111)
data,label=loadDataSet()
dataArr=array(data)

x1cord1=[]
x2cord1=[]
x1cord2=[]
x2cord2=[]
m,n=shape(data)
for i in range(m):
    print i
    if int(label[i])==1:
        x1cord1.append(dataArr[i,1])
        x2cord1.append(dataArr[i,2])
    else:
        x1cord2.append(dataArr[i,1])
        x2cord2.append(dataArr[i,2])
ax.scatter(x1cord1,x2cord1,c='red',marker='s')
ax.scatter(x1cord2,x2cord2,c="green")
plt.xlabel('X1')
plt.ylabel('X2')
plt.show()
```

函数`loadDataSet`将数据集从`testSet.txt`逐行读取并存入两个矩阵中。`testSet`中每一行的数据有三个值，分别是X1，X2和数据对应的类别标签。并且，注意到我们在`dataMat`中的第一个值设置为1，那其实是X0的值，这在这里单纯的数据集输出中没有太大的作用，但是会方便之后我们导入模型时的计算。

`shape`函数读取矩阵的行数m和列数n。

`figure`建立绘图平面，`addsubplot`表示我们要在平面上建立绘制几个图表，`111`说明我们希望绘制一个占整个平面$$$1*1$$$大小的图表，然后选取第一个图表。

`scatter`表示散点图,参数`marker='s'`表示点的形状为方形，它还可以接收一个参数`s=<NUMBER>`来调整点的大小。

### 批梯度上升训练

得知数据集的输出型状后，我们可以着手构建模型了，这一次我们先使用梯度上升模型。

我们先来构筑sigmoid函数：

```python
def sigmoid(inX):
    return 1.0/(1+exp(-inX))
```

表示接收一个输入`inX`可以认为是我们在sigmoid函数中所说的'z'，用sigmoid函数输出。

然后构建梯度上升函数：

```python
def gradAscent(dataMatIn,classLabels):
    dataMat=mat(dataMatIn)
    labelMat=mat(classLabels).transpose()
    m,n=shape(dataMat)
    alpha=0.001
    maxCycles=500
    weights=ones((n,1))
    for k in range(maxCycles):
        h=sigmoid(dataMat*weights)
        error=labelMat-h
        weights=weights+alpha*dataMat.transpose()*error
    return weights
```

第一个参数是全部输入样本组成的二维数组，每一个样本包含3个特征分别是X0,X1,X2，因此，用`mat`函数转换后的`dataMat`是一个3 x 100的输入矩阵。第二个参数是每一个样本的标签组成的矩阵，为了方便计算，我们在转化它为1 x 100的矩阵后还要用`transpose()`将其转置。

变量`alpha`表示梯度上升中的步长，`maxCycles`表示我们将要进行的步数，一般来说我们也可以通过设定条件让程序判断收敛情况来自行决定合适的步长，但这一步我们暂且先简化为这样。`weights`便是我们希望求得的参数，可以看作是上面给出的梯度上升的数学模型中的θ，这里我们先将其初始化为一个 3 x 1的矩阵分别对应数据的3个特征。

然后我们循环更新`weights`值，以找到最合适的`weights`。更新方式便是梯度上升更新：

$$
weights=weights+alpha*dataMat^T(labelMat-h)\\
h=\frac{1}{1+e^{-weights*dataMat}}
$$
我们可以把它与上面的题都更新公式对比一下。

然后通过500步更新得到了目标参数`weights`

我们可以用`print`输出看看我们得到的参数：

```python
data,labels=loadDataSet()
weights=gradAscent(data,labels)
print weights

>>[[ 4.12414349]
 [ 0.48007329]
 [-0.6168482 ]]
```

然后将其绘制到我们一开始做的数据集表示图上。

```python
weights=weights.getA()
x=arange(-3.0,3.0,0.1)
y=(-weights[0]-weights[1]*x)/weights[2]
ax.plot(x,y)
```

![](img\mla1-5.png)

发现效果不错。其中，函数`getA()`表示将矩阵`weights`转换成数组，如果我们不这么做的话，我们可以试着输出一下x和y：

```python
print x
print y

>>[ -3.00000000e+00  -2.90000000e+00  -2.80000000e+00  -2.70000000e+00
  -2.60000000e+00  -2.50000000e+00  -2.40000000e+00  -2.30000000e+00
  ...#这是x
>>[[ 4.35102773  4.42885454  4.50668136  4.58450817  4.66233498  4.7401618
   4.81798861  4.89581542  4.97364223  5.05146905  5.12929586  5.20712267
   ...#这是y
```

我们会发现y的值是被包裹在两个`[]`里面的，实际上可以认为y是一个嵌套了两层的一维矩阵，这也是为什么，我们要用`getA`来将`weights`从矩阵转换回数组。

y的计算方式或许也会给人带来疑问：实际上，我们知道，我们希望得到的是一条将两个数据集分开的直线。因此，我们在给出一串连续的横坐标（代码中就是从-3到3每隔0.1取一个横坐标）组成的向量后，就可以根据直线的方程$$$y=kx+b(转换成-w2X2=w1X1+w0)$$$计算这一连串横坐标对应的y轴坐标，然后将其绘制到散点图上。

### 随机梯度上升训练

因为我们这里的样本比较小，所以我们的批梯度上升可以很快的就得到我们想要的结果，但实际上，很多数据集包含的内容都非常巨大，因此，为了能够快速执行分类任务，我们有时候会牺牲一些精度来换取运算的速度。这便是我们的**随机梯度上升法**，它的原理我在机器学习理论中的笔记有讲，这里就不再赘述:

```python
def stocGradAscent(dataMatIn, classLabels):
    dataMat = mat(dataMatIn)
    labelMat = classLabels  #注意这里没有将classLabels转为矩阵
    m, n = shape(dataMat)
    alpha = 0.01 #学习速度变大是因为我们的循环次数没有前面那么多了，因此需要加大步长
    # maxCycles=500 #这个地方被注释掉是因为循环次数不需要由它控制了
    weights = ones(n) #这里我们生成了一个1 x 3的参数矩阵
    for k in range(m): #以样本数为更新次数
        h = sigmoid(sum(dataMatIn[k] * weights)) #求出的输出函数的值为标量了
        error = labelMat[k] - h
        #误差也是一个值，它与之前不一样，这次表示的是一个样本输出函数造成的误差
        weights = weights + (alpha * error * dataMat[k]).getA()
        # 这里的getA也是为了让weights与后面一项可以相加
    return weights

#------此处无变化
data, labels = loadDataSet()
weights = stocGradAscent(data, labels)

figure = plt.figure()
ax = figure.add_subplot(111)
data, label = loadDataSet()
dataArr = array(data)
x1cord1 = []
x2cord1 = []
x1cord2 = []
x2cord2 = []
m, n = shape(data)
for i in range(m):
    if int(label[i]) == 1:
        x1cord1.append(dataArr[i, 1])
        x2cord1.append(dataArr[i, 2])
    else:
        x1cord2.append(dataArr[i, 1])
        x2cord2.append(dataArr[i, 2])
ax.scatter(x1cord1, x2cord1, s=30, c='red', marker='s')
ax.scatter(x1cord2, x2cord2, c="green")
# ------------

weights = weights[0] 
#因为weights这次是一个嵌套了一层的1 x 3矩阵，因此这里要使用索引来将其从第一层嵌套中取出
x = arange(-3.0, 3.0, 0.1)
y = (-weights[0] - weights[1] * x) / weights[2]
ax.plot(x, y)

plt.show()
```

可以得到我们随机梯度下降的结果：

![](img\mla1-6.png)

发现结果没有之前的准确，这是当然的，因为我们牺牲了精度，随机梯度上升对参数`weights`的每一次更新都只用了一个样本，因此速度上相较批梯度上升会大幅提升。

下面这张图表示每一次更新回归参数X0,X1,X2的值，根据样本次数，我们总共更新了100次：

绘图代码：

```python
def stocGradAscent(dataMatIn, classLabels):
    dataMat = mat(dataMatIn)
    labelMat = classLabels  #
    x0cord=[]
    x1cord=[]
    x2cord=[]
    m, n = shape(dataMat)
    alpha = 0.01
    # maxCycles=500
    weights = ones(n)
    for k in range(m):
        h = sigmoid(sum(dataMatIn[k] * weights))
        error = labelMat[k] - h
        weights = weights + (alpha * error * dataMat[k]).getA()
        x0cord.append(weights[0][0])
        x1cord.append(weights[0][1])
        x2cord.append(weights[0][2])

    return weights,x0cord,x1cord,x2cord

data, labels = loadDataSet()
weights,x0cord,x1cord,x2cord = stocGradAscent(data, labels)

fig,axes=plt.subplots(3,1)
axes[0].plot(arange(100),x0cord)
axes[1].plot(arange(100),x1cord)
axes[2].plot(arange(100),x2cord)

plt.show()
```

![](img\mla1-7.png)

可以看出来，回归参数的上下波动非常巨大，并且时常会往与梯度不同的方向更新，X2在开始的几次更新之后很快达到了稳定，但是X0和X1则没有。

并且，我们可以发现，参数在趋于稳定之后依然会有局部波动，这是因为数据集中并非所有的数据都可以确保正确分类（因为数据集并非线性可分）。