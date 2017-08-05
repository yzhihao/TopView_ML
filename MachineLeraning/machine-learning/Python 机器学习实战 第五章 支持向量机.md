# Python 机器学习实战 第五章 支持向量机

资料参考来源：

人民邮电出版社 Peter Harrington《机器学习实战》第六章

清华大学出版社 周志华 《机器学习》 第六章

清华大学出版社 李航 《统计学习方法》 第二章 感知机，第七章 支持向量机

[我的博客 机器学习 八~十一章 支持向量机](https://zyzypeter.github.io/2017/07/31/machine-learning-ch8-SVM1/)

[数据集来源 Github:Peter Harrington](https://github.com/pbharrin/machinelearninginaction)

本章数据集来源：[UCI Machine Learning Repository plrx](http://archive.ics.uci.edu/ml/datasets/Planning+Relax#)

## 提取与观察数据集

支持向量机与我们之前的模型相比要复杂得多，但也相应的，它的功能也比我们之前的模型要强大。尽管我们之前做的模型也有能给非线性数据分类的（kd树，决策树），但相比之下，SVM所应用到的核技巧会更加强大。（但这并不是说kd树或者决策树就不好，它们也有更深层的应用方式如集成学习算法中的随机森林）

在开始之前，我们还是按惯例先观察一下我们的数据集（这次我们用的数据集是来自UCI的一份有关脑电波（？）的研究数据，属性是不同波段的信号频率,共12个，属于二元分类问题，类别标签有两个，值为1和2分别代表大脑紧张思考状态（？）和放松状态，数据连接为[UCI Machine Learning Repository plrx](http://archive.ics.uci.edu/ml/datasets/Planning+Relax#)）：

![](img\mla5-1.png)

![](img\mla5-2.png)

显然，与前面我们用过的数据不同，这次的数据会比较具有挑战性，(换句话说，我不太能保证自己做的模型的精度...)。

但我们终归还是要做的，在观察完数据集之后，我们就应该有了提取数据集的思路了：

```python
from numpy import *
from matplotlib import pyplot as plt
import pandas as pd

def loadDataSet(path):
    # 数据集读取函数
    fr = open(path, 'r')
    dataSet = []
    for line in fr.readlines():
        lineArr = line.strip().split()
        data = []
        i = 0
        for attr in lineArr:
            lineArr[i] = float(lineArr[i])
            data.append(lineArr[i])
            i += 1
        if data[-1] == 2:
            data[-1] = -1
        dataSet.append(data)
    dataSet = mat(dataSet)
    return dataSet

dataSet = loadDataSet(r'data\plrx\plrx.txt')
```

因为支持向量机的基本模型是由感知机演变而来的，所以我们需要将样本的类别值从1，2转换成1，-1（正负类）。

然后，我们可以粗略地绘制一下数据集的可能图像，当然，由于它这里是多维数据集，我这里只能一次挑两个属性作为横纵轴来勉强观测一下数据集：

![](img\mla5-3.png)

```python
def plotDataSet(dataSet):
    fig,axes=plt.subplots(2,3,sharex=True,sharey=True)
    plt.subplots_adjust(wspace=0,hspace=0)
    i=0
    j=0
    attrNum=0
    while attrNum < 12:
        for data in dataSet:
            if data[0,-1]==1:
                axes[i, j].scatter(data[0, attrNum], data[0, attrNum + 1], color='g')
            else:
                axes[i, j].scatter(data[0, attrNum], data[0, attrNum + 1], color='b')
        if j<2:
            j+=1
        else:
            j=0
            i+=1
        attrNum+=2
    plt.show()
```

虽然料到了不太可能看出什么来，但看到果然是一团乱麻还是蛮难受的，不过我们依然可以将其认为是服从多元高斯分布的，一般来说，对于这种难以观察分布状况的连续值，我们可以先试一试高斯分布，如果效果不佳可以再做其他考虑（例如泊松分布）。

## 核函数

既然认定高斯分布，那么我们就需要先写出用于分类高斯分布的高斯径向核函数：

```python
def kernel(xi, xj):
    # 高斯径向核函数
    """
    :type theta: int
    :type xj: numpy.matrixlib.defmatrix.matrix
    :type xi: numpy.matrixlib.defmatrix.matrix
    """
    theta = sqrt(2)
    vector = xi - xj
    output=exp(-float((vector * vector.transpose())[0, 0]) / (2 * theta * theta))
    return output
```

接受的两个参数`xi,xj`分别是我们希望带入核函数`K(x,z)`中的`x`和`z`向量。

## SMO算法

序列最小最优化（SMO）算法在支持向量机中较为常用，这种算法于1998年由Platt提出。

由于它的辅助函数比较多，并且包含很多内容，我们可以先把它的结构用图片表示出来：

### SMO算法结构示意图

![](img\mla5-4.png)

接下来，就让我们沿着结构流程一步一步往下做：

### 变量类

首先我们构建一个关于变量的类，方便我们后面使用：

```python
class alphaClass(object):
    def __init__(self):
        self.alpha = 0
        self.num = 0
```

### 主体函数

正式开始前，我们可以先根据整体结构构建一个主体函数：

```python
def SMO(dataSet, accuracy, C, iterNum, diminution):
    # 序列最小最优化算法主函数
    """
    :type acurracy: float
    :type dataSet: numpy.matrixlib.defmatrix.matrix
    """
    alphaExceptionNumSet = set()
    # 初始化变量排除集合
    m, n = shape(dataSet)
    alphas = zeros(m)
    i = 0
    EList = zeros(m)
    b = bCalc(alphas, dataSet, C)
    count = 0
    for E in EList:
        ECalc(count, dataSet, EList, alphas, b)
        count += 1
    flag = 0
    k = 0
    while (flag != 1 and k <= iterNum):
        valueOfTargetFunction = calcTargetFunction(alphas, dataSet)
        # 计算当前目标函数值
        alphaBlockOne = searchAlphaOne(alphas, dataSet, C, b, alphaExceptionNumSet)
        # 搜索变量一
        alphaBlockTwo = searchAlphaTwo(alphaBlockOne, EList, alphas, dataSet)
        # 一般法搜索变量二
        alphaBlockOne, alphaBlockTwo = alphaSolver(alphaBlockOne, alphaBlockTwo, EList, alphas, dataSet, C)
        # 求解两个变量的二次规划
        alphasTestMat = alphasTest(alphaBlockOne, alphaBlockTwo, alphas, alphaExceptionNumSet)
        # 构建实验变量集合
        if valueOfTargetFunction - calcTargetFunction(alphasTestMat, dataSet) < diminution:
            # 如果精度提升幅度小于预设最小缩小量后启用启发式选择变量法
            alphaBlockOne, alphaBlockTwo = heuristicSelection(alphaBlockOne, alphaBlockTwo, EList, alphas, b, C,
                                                              dataSet, diminution, alphaExceptionNumSet,
                                                              valueOfTargetFunction)
            # 启发式搜索变量二
            if alphaBlockOne is None:
                # 启发式搜索未达到目标，将已搜索变量一编号加入变量排除集合，重新搜索变量一
                k += 1
                print "支持向量机已迭代", k, "次，启发式搜索未匹配到合适的变量一，重新迭代"
                continue
        alphaExceptionNumSet.clear()
        # 清空排除alpha编号集合
        b = bUpdater(alphaBlockOne, alphaBlockTwo, alphas, dataSet, EList, b, C)
        # 更新阈值b
        alphasUpdate(alphaBlockOne, alphaBlockTwo, alphas)
        # 更新变量集合
        EUpdater(EList, alphas, b, dataSet, C)
        # 更新误差列表
        flag = terminateCondition(alphas, dataSet, b, C, accuracy)
        # 测试是否满足停机条件
        k += 1
        # 迭代次数加1
        print "支持向量机已迭代", k, "次"
    print "支持向量机学习完毕"
    return alphas, b

alphas, b = SMO(dataSet, 0.96, 0.1, 500, 0.01)
# 调用示例
```

这个函数的功能就是作为整体负责整个流程各个函数的调用和各个阶段的运行。

这里我们还初始化了各个我们需要用到的对象，一般来说α变量集合的内容我们会将其初始化为0.

### 阈值b和误差E

然后我们可以先写有关计算、更新阈值b和误差E的函数,公式这里就不赘述了，可以在我的博客里面找到：

```python
def bCalc(alphas, dataSet, C):
    # 阈值b计算函数
    b = 0
    count = 0
    for alphaPre in alphas:
        if alphaPre > 0 and alphaPre < C:
            sumResult = 0
            i = 0
            for data in dataSet:
                sumResult += dataSet[i, -1] * alphas[i] * kernel(data, dataSet[count])
                i += 1
            b = dataSet[count, -1] - sumResult
            return b
        count += 1
    return b

def ECalc(num, dataSet, EList, alphas, b):
    # 误差E计算函数
    E = hypothesis(dataSet[num], dataSet, alphas, b) - dataSet[num, -1]
    EList[num] = E
    return E

def bUpdater(alphaBlockOne, alphaBlockTwo, alphas, dataSet, EList, bOld, C):
    # 阈值b更新函数
    num1 = alphaBlockOne.num
    alpha1 = alphaBlockOne.alpha
    num2 = alphaBlockTwo.num
    alpha2 = alphaBlockTwo.alpha
    bnew1 = -EList[num1] - dataSet[num1, -1] * kernel(dataSet[num1], dataSet[num1]) * (alpha1 - alphas[num1]) \
            - dataSet[num2, -1] * kernel(dataSet[num2], dataSet[num1]) * (alpha2 - alphas[num2]) + bOld
    bnew2 = -EList[num2] - dataSet[num1, -1] * kernel(dataSet[num1], dataSet[num2]) * (alpha1 - alphas[num1]) \
            - dataSet[num2, -1] * kernel(dataSet[num2], dataSet[num2]) * (alpha2 - alphas[num2]) + bOld
    if (alpha1 > 0 and alpha1 < C) and (alpha2 > 0 and alpha2 < C):
        return bnew1
    if (alpha1 == 0 or alpha1 == C) or (alpha2 == 0 or alpha2 == C):
        return float(bnew1 + bnew2) / 2
    print "出现异常变量"
    return None

def EUpdater(EList, alphas, bnew, dataSet, C):
    # 误差E更新函数
    count = 0
    for data in dataSet:
        j = 0
        sumResult = 0.0
        for alpha in alphas:
            if alpha > 0 and alpha < C:
                sumResult += data[0, -1] * alpha * kernel(data, dataSet[j])
            j += 1
        EList[count] = sumResult + bnew - data[0, -1]
        count += 1
```

阈值b是一个标量，误差E有很多个，每个训练样本都对应一个误差E，我们可以用一个矩阵或者列表将这些误差保存起来，方便我们随时更新和调用。

注意到我们的结构图中更新两者的顺序，因为阈值b的更新同时需要优化后的新变量和优化前的旧变量，所以要注意不能提前把旧变量用新变量给覆盖了。

### 输出函数和符号函数

输出函数`hypothesis`和符号函数`signFunction`也比较简单，并且涉及的参数和内容不多，我们也可以先把这两个函数写出来：

```python
def hypothesis(xi, dataSet, alphas, b):
    # 输出函数
    sumResult = 0
    j = 0
    for data in dataSet:
        sumResult += float(alphas[j]) * data[0, -1] * kernel(xi, data)
        j += 1
    return b + sumResult

def signFunction(x, dataSet, alphas, b):
    # 决策符号函数
    result = hypothesis(x, dataSet, alphas, b)
    if result > 0:
        return 1
    else:
        return -1
```

### 搜索变量一

搞定这几个小函数之后，我们就可以开始搭建算法流程的第一步，搜索变量一的函数：

```python
def searchAlphaOne(alphas, dataSet, C, b, alphaExceptionNumSet):
    # 搜寻第一个变量的外层循环函数
    alphaBlock = alphaClass()
    alpha = 0
    alphaNum = 0
    count = 0
    deviation = 0
    for alphaPre in alphas:
        if alphaPre in alphaExceptionNumSet:
            count += 1
            continue
        g = hypothesis(dataSet[count], dataSet, alphas, b)
        condition = dataSet[count, -1] * g
        if alphaPre == 0:
            if condition < 1:
                if deviation < abs(condition - 1):
                    deviation = abs(condition - 1)
                    alpha = alphaPre
                    alphaNum = count
        elif alphaPre > 0 and alphaPre < C:
            if condition != 1:
                if deviation < abs(condition - 1):
                    deviation = abs(condition - 1)
                    alpha = alphaPre
                    alphaNum = count
        elif alphaPre == C:
            if condition > 1:
                if deviation < abs(condition - 1):
                    deviation = abs(condition - 1)
                    alpha = alphaPre
                    alphaNum = count
        elif alphaPre > C:
            print "alphas中出现了异常变量，该变量大于C"
            return
        elif alphaPre < 0:
            print "alphas中出现了异常变量，该变量小于0"
            return
        count += 1
    alphaBlock.alpha = alpha
    alphaBlock.num = alphaNum
    return alphaBlock
```

尽管看起来很长，但其实内容并不复杂，这个函数的目的就是为了从所有的变量中找到一个违反KKT条件最严重的变量。

需要注意的是，`alphaExceptionNumSet`中保存了我们希望不去搜索的变量在变量集合中的序号，这些被排除的变量序号来自启发式搜索。

### 变量二的一般搜索

```python
def searchAlphaTwo(alphaBlockOne, EList, alphas, dataSet):
    # 搜寻第二个变量的内层循环函数
    """
    :type dataSet: numpy.matrixlib.defmatrix.matrix
    :type alphas: numpy.matrixlib.defmatrix.matrix
    :type: EList: list
    :type alphaBlockOne: alphaClass
    """
    alphaBlock = alphaClass()
    alpha = 0.0
    count = 0
    alphaNum = 0
    weight = 0
    for alphaPre in alphas:
        if count == alphaBlockOne.num:
            count += 1
            continue
        weightPre = abs(EList[count] - EList[alphaBlockOne.num])
        if weight < weightPre:
            weight = weightPre
            alpha = alphaPre
            alphaNum = count
        count += 1
    alphaBlock.num = alphaNum
    alphaBlock.alpha = alpha
    return alphaBlock
```

这是一般情况下用于搜索变量二的函数，这个函数搜索变量二的条件就是找到一个能让二次规划求解时计算速度最快的变量二，但这也就导致我们往往会找到一些不太能够对整体达到优化效果的变量，我们可以将这个地方类比为梯度下降中的随机梯度，即为了速度牺牲了精度（仅是做一个类比，二者的运作方式还是有很大区别的），当效果表现得非常差（目标函数下降量小于预设值）时，我们就需要转入启发式搜索。

不过在那之前，我们还需要先解决二次规划的问题：

### 二次规划求解

#### 求解函数

顺着《统计学习方法》一书中的习惯，为了不造成过多的麻烦，我们在二次规划求解的时候也先求解变量二。

```python
def alphaSolver(alphaBlockOne, alphaBlockTwo, EList, alphas, dataSet, C):
    # 两个变量的凸二次规划问题优化函数
    alphaBlockNew1 = alphaClass()
    alphaBlockNew2 = alphaClass()
    num1 = alphaBlockOne.num
    num2 = alphaBlockTwo.num
    eta = kernel(dataSet[num1], dataSet[num1]) + kernel(dataSet[num2], dataSet[num2]) \
          - 2 * kernel(dataSet[num1], dataSet[num2])
    alpha2 = alphaBlockTwo.alpha + dataSet[num2, -1] * (EList[num1] - EList[num2]) / eta
    alpha2 = alphaCutter(alpha2, alphaBlockTwo, alphaBlockOne, alphas, C, dataSet)
    # 剪辑alpha2
    alpha1 = alphaBlockOne.alpha + dataSet[num1, -1] * dataSet[num2, -1] * (alphaBlockTwo.alpha - alpha2)
    alphaBlockNew1.alpha = alpha1
    alphaBlockNew1.num = num1
    alphaBlockNew2.alpha = alpha2
    alphaBlockNew2.num = num2
    return alphaBlockNew1, alphaBlockNew2
```

#### 剪辑函数

一个用于在二次规划求解时辅助计算第一个欲求解变量的函数：

```python
def alphaCutter(alpha2, alphaBlockTwo, alphaBlockOne, alphas, C, dataSet):
    num1 = alphaBlockOne.num
    num2 = alphaBlockTwo.num
    L = 0
    H = C
    if dataSet[num1, -1] != dataSet[num2, -1]:
        L = max(0, alphas[num2] - alphas[num1])
        H = min(C, C + alphas[num2] - alphas[num1])
    else:
        L = max(0, alphas[num2] + alphas[num1] - C)
        H = min(C, alphas[num2] + alphas[num1])
    if alpha2 > H:
        return H
    elif alpha2 < L:
        return L
    else:
        return alpha2
```

### 目标函数值计算函数

要判断是否启用启发式搜索，我们还需要知道目标函数值更新后与更新前是否有区别，所以要先构建一个计算原始问题中目标函数值的函数：

```python
def calcTargetFunction(alphas, dataSet):
    # 计算目标函数
    i = 0
    m, n = shape(dataSet)
    sumResult1 = 0
    alphaSum = 0
    while i < m:
        sumResult2 = 0
        j = 0
        while j < m:
            sumResult2 += alphas[i] * alphas[j] * dataSet[i, -1] * dataSet[j, -1] * kernel(dataSet[i], dataSet[j])
            j += 1
        sumResult1 += sumResult2
        alphaSum += alphas[i]
        i += 1
    return 0.5 * sumResult1 - alphaSum
```

通过这个计算函数，我们可以用优化前的目标函数值和优化后的目标函数值做比较，然后做出是否需要启用启发式搜索的判断。

### 测试用变量集构建函数

因为numpy结构的索引和调用默认都是直接操作原结构，也即是说我们每次使用变量集的时候做出的所有操作都是在原变量集上，这就意味着我们如果要比较新旧目标函数值，我们就需要将一个搭载了新变量的“临时测试变量集”与旧变量集分别放入目标函数值计算函数来做比较。

这个函数的代码构建很简单，重要的是我们构建它的原因：

```python
def alphasTest(alphaBlockOne, alphaBlockTwo, alphas, alphaExceptionNumSet):
    """
    :type alphaExceptionNumSet: set
    """
    alphasTestMat = alphas.copy()
    alphasTestMat[alphaBlockOne.num] = alphaBlockOne.alpha
    alphasTestMat[alphaBlockTwo.num] = alphaBlockTwo.alpha
    return alphasTestMat
```

### 启发式搜索

一切就绪之后就是我们的启发式搜索函数：

```python
def heuristicSelection(alphaBlockOne, alphaBlockTwo, EList, alphas, b, C, dataSet, diminution, alphaExceptionNumSet,
                       valueOfTargetFunction):
    # 启发式选择变量
    count = 0
    alpha1 = alphas[alphaBlockOne.num]
    diminutionTest = 0
    alphaTestMat = alphas.copy()
    for alpha in alphas:
        if count == alphaBlockOne.num:
            count += 1
            continue
        alphaBlockNewTestTwo = alphaClass()
        alphaBlockNewTestTwo.alpha = alpha
        alphaBlockNewTestTwo.num = count
        alphaBlockNewTestOne, alphaBlockNewTestTwo = alphaSolver(alphaBlockOne, alphaBlockNewTestTwo, EList, alphas,
                                                                 dataSet, C)
        alphaTestMat[count] = alphaBlockNewTestTwo.alpha
        alphaTestMat[alphaBlockNewTestOne.num] = alphaBlockNewTestOne.alpha
        diminutionTest = valueOfTargetFunction - calcTargetFunction(alphaTestMat, dataSet)
        if diminutionTest >= diminution:
            return alphaBlockNewTestOne, alphaBlockNewTestTwo
        count += 1
    alphaExceptionNumSet.add(alphaBlockOne.num)
    return None
```

通过这个函数我们就可以在目标函数值无法再下降的时候优化搜索其它的变量。

### 停机条件判断

然后就是一个用于判断我们何时达到停机条件的函数：

```python
def terminateCondition(alphas, dataSet, b, C, accuracy):
    # 停机条件判断函数
    flag = 1
    i = 0
    for alpha in alphas:
        condition = dataSet[i, -1] * hypothesis(dataSet[i], dataSet, alphas, b)
        if alpha == 0:
            if condition < 1:
                flag = 0
                continue
        elif alpha > 0 and alpha < C:
            if condition != 1:
                flag = 0
                continue
        elif alpha == C:
            if condition > 1:
                flag = 0
                continue
        elif alpha > C:
            print "alphas中出现了异常变量，该变量大于C"
            flag = 0
        elif alpha < 0:
            print "alphas中出现了异常变量，该变量小于0"
            flag = 0
        i += 1
    if flag == 1:
        return 1
    # 此时flag=0
    rate = {"correct": 0, "total": 0}
    i = 0
    for data in dataSet:
        rate['total'] += 1
        result = data[0, -1] * signFunction(data, dataSet, alphas, b)
        if result > 0:
            rate['correct'] += 1
        i += 1
    correctRate = float(rate['correct']) / rate['total']
    print "在训练集中检测了", str(rate['total']), "个样本，模型在训练集中的正确率为", str(correctRate * 100), "%"
    if correctRate > accuracy:
        flag = 1
    return flag
```

我们设置的停机条件有三个：
1. 达到最大迭代次数
2. 达到指定精确度
3. 全部变量与对应样本满足KKT条件

至此，我们就完成了SMO算法的构建。

## 测试模型

我们最后来写一个简单的测试函数用于测试我们的模型在测试集中的效果：

```python
def test(alphas, b, dataSet, path):
    print "支持向量机开始测试"
    testSet = loadDataSet(path)
    rate = {"correct": 0, "total": 0}
    i = 0
    for data in testSet:
        rate['total'] += 1
        result = data[0, -1] * signFunction(data, dataSet, alphas, b)
        if result > 0:
            rate['correct'] += 1
        i += 1
    correctRate = float(rate['correct']) / rate['total']
    print "在测试集中检测了", str(rate['total']), "个样本，模型在测试集中的正确率为", str(correctRate * 100), "%"
```

然后试着调用一下：

```python
dataSet = loadDataSet(r'data\plrx\plrx.txt')
alphas, b = SMO(dataSet, 0.9, 0.1, 500, 0.01)
test(alphas, b, dataSet, r'data\plrx\plrxTest.txt')
```

```
在训练集中检测了 110 个样本，模型在训练集中的正确率为 93.6363636364 %
支持向量机已迭代 1 次
支持向量机学习完毕
支持向量机开始测试
在测试集中检测了 72 个样本，模型在测试集中的正确率为 98.6111111111 %
```

老样子，我们将UCI的数据集分成了两个部分，一部分用作训练集，一部分用作测试集。

样本数量很少的情况下我们可以使用交叉验证，避免我们得到太过片面的效果，有兴趣的可以以后再尝试一下。

源代码可以在我的github中找到：

[Machine-Learning-in-action](https://github.com/ZyzyPeter/Machine-Learning-in-action)