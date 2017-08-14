# Python 机器学习实战 第六章 AdaBoost

## 算法简介

这次我们做一个AdaBoost方法中以单层决策树（决策树桩）作为基学习器的提升方法（起初我以为这是提升树，而后发现提升树与以单层决策树为基学习器的AdaBoost是有区别的），AdaBoost的算法流程如下：

### 算法结构

![](img\ml12-19.png)

### 利弊分析

AdaBoost的优点在于它的泛化错误率低，计算开销也不会比一般的单学习器大，容易编码并且可以应用在大部分分类器上。

AdaBoost的缺点就是对于离群值比较敏感。

和大多数集成学习方法一样，AdaBoost同时适用于连续值和离散值。

## 处理数据

我们这次采用的数据是UCI提供的一份数据，不过有之前写支持向量机的教训在先，我们先用一份比较简单的数据进行代替：

```
1 2.1 1
1.5 1.6 1
1.3 1 -1
1 1 -1
2 1 1
```

这个简单的数据集主要是为了方便我们在写代码的过程中进行绘图和观察，因为它是二维的，并且它的排列也确保AdaBoost需要多个基学习器重合才能完成分类（这个我们等会儿再讲）

### 数据类型

```python
class Data():
    total = None  # 样本总数
    featureNum = None  # 特征数量

    def __init__(self, weight, num, feature, label):
        self.weight = weight  # 权值
        self.num = num  # 序号
        self.feature = feature  # 输入特征
        self.label = label  # 类别标签
        self.tempWeight = None
```

我们先给我们的数据创建一个类型用于保存，事实证明，操作一个包含数据所需信息的对象比直接操作这些信息要方便多了。

数据的类并没有什么固定的格式，事实上我也经常是在一边写的时候一边添加一些我可能需要但开始的时候没有加进去的属性或方法。

### 读取数据函数

```python
def loadDataSet(path):
    fr = open(path, 'r')
    dataSet = []
    labelSet = []
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataSet.append(lineArr[0:-1])
        labelSet.append(lineArr[-1])
    dataMat = mat(dataSet, float)
    labelMat = mat(labelSet, float)
    count = 0
    m, n = shape(dataMat)
    Data.featureNum = n
    Data.total = m
    dataSet = []
    weight = float(1.0 / m)
    # 初始化权值分布
    for count in range(m):
        if labelMat[0, count] != 1:
            labelMat[0, count] = -1
        feature = dataMat[count, :]
        data = Data(weight, count, feature, labelMat[0, count])
        dataSet.append(data)
        count += 1
    dataSet = mat(dataSet)
    return dataSet
    # dataSet是一个 1*（训练样本数）的矩阵
```

注意我们在读取数据时还顺便初始化了各样本数据的权值分布。

与之前不同的是，我们把路径作为一个参数提出来了，这样子会方便我们修改读取数据的对象：

```python
def loadSimpleData():
    return loadDataSet(r'data/plrx/simpleTest.txt')
```

于是可以用这个小函数来先调用我们之前说的简单的训练数据。

### 绘图观察数据

```python
def draw(dataSet, classifier):
    # 绘图函数
    fig, ax = plt.subplots(1, 1)
    i = 0
    for i in range(Data.total):
        data = dataSet[0, i]
        if data.label != 1:
            ax.scatter(data.feature[0, 0], data.feature[0, 1], s=200, marker='_', c='g')
        else:
            ax.scatter(data.feature[0, 0], data.feature[0, 1], s=200, marker='+', c='b')
        i += 1
    plt.show()

dataSet=loadSimpleData()
draw(dataSet)
```

对于二维或是三维的简单数据，我们可以用matplotlib绘制出来观察一下：

![](img\mla6-1.png)


决策树桩一次只能绘制出一条与坐标轴平行的线，但这幅图里面的数据集显然是不能用决策树桩分开的（因为决策树桩在二维平面上就相当于一条与坐标轴平行的直线），所以我们在前面才说这是适合用于测试AdaBoost的训练集。

## 主体函数

```python
def adaBoost(dataSet, iterNum, minErr):
    # AdaBoost主体函数
    count = 0
    classifier = None
    treeSet = set()
    flag = True
    # 运行条件初始化为真
    while (count < iterNum and flag is True):
        tree = treeGenerate(dataSet)
        # 训练一个决策树桩
        dataSet = updateWeight(dataSet, tree)
        # 更新权值分布
        treeSet.add(tree)
        # 添加一棵树进树集合
        classifier = Classifier(treeSet)
        # 构造分类器
        flag = terminate(classifier, dataSet, minErr)
        # 检测停机条件
        count += 1
    if flag is True:
        print "迭代超过最大次数，终止迭代并返回分类器"
    return classifier
```

首先构造函数主体，让我们对程序的整体架构有一个比较清楚的认知，这样方便我们一步一步完成整个程序。

该函数接受3个参数，数据集，最大迭代次数和最小错误率，并返还一个集成分类器对象`classifier`。

### 分类器对象

```python
class Classifier():
    def __init__(self, treeSet):
        self.treeSet = treeSet

    def classify(self, feature):
        sumResult = 0
        for tree in self.treeSet:
            value = tree.classifier(feature)
            sumResult += tree.weight * value
        return sumResult
```

对象属性是一个存储基学习器的集合，因为暂时没有对基学习器排序的要求，所以我们用一个`set`来存放基学习器，可以在主体函数`adaBoost()`中找到我们初始化这个集合的语句。（如果想作图的时候按顺序作出每一条基学习器的图像，那么还是建议用`list`来存放）

而后提供的实例方法实际上就是一个调用所有基学习器进行集成输出的函数，接受唯一的一个参数是数据的特征组成的矩阵`feature`

我们可以看到，这个方法还调用了一个基学习器`tree`的实例方法，这个对象的内容在下面：

## 基学习器对象

我们使用的基学习器是一颗决策树桩，并且叶节点没有回溯父节点的需求，所以直接设置成类别标签就可以了：

```python
class Tree():
    def __init__(self):
        self.leftLabel = None
        self.rightLabel = None
        # 左右标签
        self.weight = None
        # 分类器权重
        self.splitFeatureValue = None
        # 用于划分的值
        self.splitFeatureOrder = None
        # 用于划分的属性序号
        self.err = None
        # 基学习器在训练数据集上的分类误差率

    def classifier(self, feature):
        # 基学习器的分类器
        """
        :type feature: matrix
        """
        value = feature[0, self.splitFeatureOrder]
        if value > self.splitFeatureValue:
            return self.rightLabel
        else:
            return self.leftLabel
```

函数`classifier`就是这个基学习器提供的分类方法，也可以看作是输出函数。

## 生成单个树桩

### 生成树

顺着主体函数的内容，我们一步一步往下编写，首先就是如何生成一棵决策树桩，我们用函数`treeGenerate`来完成这个功能：

```python
def treeGenerate(dataSet):
    # 生成决策树
    tree = Tree()
    featureInf = chooseFeature(dataSet)
    print featureInf
    labelList = featureInf['labelList']
    tree.leftLabel = labelList[0]
    tree.rightLabel = labelList[1]
    if featureInf['err'] != 0:
        tree.weight = 0.5 * math.log((1.0 - featureInf['err']) / featureInf['err'])
    else:
        tree.weight = 1
    tree.splitFeatureOrder = featureInf['order']
    tree.splitFeatureValue = featureInf['value']
    tree.err = featureInf['err']
    return tree
```

函数`chooseFeature`就是一个决定如何划分叶节点的函数，它返还一个字典`featureInf`包含我们需要用到的所有有关划分属性的信息（我们下面再讲这个地方的内容）。

选择语句`if featureInf['err']!=0`是为了防止某种特殊情况——尽管可能性很低，但有时候一棵决策树就将数据集完美分开的时候我们就需要防止程序出现在这种情况下计算分类器权重时由于除以0而报错的情况。

计算权重的函数这里就不再赘述，在[AdaBoost理论篇](https://zyzypeter.github.io/2017/08/08/machine-learning-ch12-boosting/)的笔记中有。

### 选择划分属性

我们在上面用到的函数`chooseFeature`：

```python
def chooseFeature(dataSet):
    # 挑选划分属性
    stdList = []
    count = 0
    err = inf
    featureInf = None
    for count in range(Data.featureNum):
        featureInfTemp = chooseSplitValue(dataSet, count)
        if featureInfTemp['err'] < err:
            err = featureInfTemp['err']
            featureInf = featureInfTemp
        count += 1
    return featureInf
```

这个函数的主要目的是选出能让分类误差率最小的属性，注意是属性而不是属性的值。为此我们的做法是将每一个属性挑出来放进函数`chooseSplitValue`中轮流计算，以此得到分类误差率最小的那个属性，并将其作为划分属性。

语句`err=inf`将初始错误率设置成正无穷大。

### 决定划分属性值

```python
def chooseSplitValue(dataSet, featureOrder):
    # 选择划分值
    labelList = []
    i = 0
    err = inf
    # 初始化误差为正无穷
    leftLabel = 0
    rightLabel = 0
    # 初始化左标签和右标签
    featureInf = {"err": 0, "order": 0, "value": 0, "labelList": None}
    # 初始化划分值
    for i in range(2):
        # 分别检测左标签为-1右标签为1，左标签为1右标签为-1两种情况
        leftLabelTemp = float(-1 + i * 2)
        rightLabelTemp = -leftLabelTemp
        dataNum = 0
        for dataNum in range(Data.total):
            # 将每个样本的特征值作为划分值计算误差
            count = 0
            left = set()
            right = set()
            for count in range(Data.total):
                # 根据dataNum对应样本在对应属性上的对应值划分左右集合，集合内容为样本序号
                data = dataSet[0, count]
                if data.feature[0, featureOrder] <= dataSet[0, dataNum].feature[0, featureOrder]:
                    left.add(data.num)
                else:
                    right.add(data.num)
                count += 1
            leftErr = 0
            count = 0
            for count in left:
                # 计算左子集误差和
                data = dataSet[0, count]
                if data.label != leftLabelTemp:
                    leftErr += data.weight
                count += 1
            count = 0
            rightErr = 0
            for count in right:
                # 计算右子集误差和
                data = dataSet[0, count]
                if data.label != rightLabelTemp:
                    rightErr += data.weight
                count += 1
            if leftErr + rightErr < err:
                # 如果当前误差小于最小误差
                err = leftErr + rightErr
                leftLabel = leftLabelTemp
                rightLabel = rightLabelTemp
                featureInf['value'] = dataSet[0, dataNum].feature[0, featureOrder]
            dataNum += 1
        i += 1
    labelList.append(leftLabel)
    labelList.append(rightLabel)
    featureInf['err'] = err
    featureInf['order'] = featureOrder
    featureInf['labelList'] = labelList
    return featureInf
```

函数`chooseSplitValue(dataSet, featureOrder)`接受数据集和划分属性（就是在哪条轴上进行划分），我们设定划分值的方式就是将所有样本的属性值都拿来作为划分值，然后从中选出分类误差率最小的那一个。需要注意的是，我们计算分类误差率是用样本数据的权值`data.weight`来计算的，这确保我们的基学习器在每一次分类时都能有差异（关注的样本不一样）。

在这里，我们还能看到我们在生成决策树桩过程中经常使用的对象`featureInf`的具体内容。

## 更新样本权重分布

```python
def updateWeight(dataSet, tree):
    i = 0
    Z = 0
    for i in range(Data.total):
        data = dataSet[0, i]
        Z += data.weight * exp(-tree.weight * data.label * tree.classifier(data.feature))
        i += 1
    i = 0
    for i in range(Data.total):
        data = dataSet[0, i]
        data.weight = data.weight * exp(-tree.weight * data.label * tree.classifier(data.feature)) / Z
        i += 1
    return dataSet
```

利用基分类器更新样本的权值分布，这确保下一轮的基分类器能够关注不同的样本。

## 设置停机条件

```python
def terminate(classifier, dataSet, minErr):
    total = 0
    correctCount = 0
    for i in range(Data.total):
        data = dataSet[0, i]
        value = classifier.classify(data.feature)
        if value >= 0:
            value = 1
        else:
            value = -1
        if value == data.label:
            correctCount += 1
        total += 1
    correctRate = float(correctCount) / total
    print "迭代完成，正确率为", correctRate
    if 1 - correctRate <= minErr:
        return False
    else:
        return True
```

停机函数根据情况可有可无，内容也有很多种，我这里仅是提供一个参考。

至此，我们就完成了一个简单的基于连续值进行分类的AdaBoost算法，结合我们应用的简单数据集，我们可以尝试着绘制出AdaBoost在二维平面上的表现：

## 绘制分类器

```python
def draw(dataSet, classifier):
    # 绘图函数
    fig, ax = plt.subplots(1, 1)
    i = 0
    for i in range(Data.total):
        data = dataSet[0, i]
        if data.label != 1:
            ax.scatter(data.feature[0, 0], data.feature[0, 1], s=200, marker='_', c='g')
        else:
            ax.scatter(data.feature[0, 0], data.feature[0, 1], s=200, marker='+', c='b')
        i += 1
    for tree in classifier.treeSet:
        axis = tree.splitFeatureOrder
        value = tree.splitFeatureValue
        otherAxis = arange(0.5, 2.5, 0.1)
        if axis == 0:
            value = otherAxis * 0 + value + 0.1
            ax.plot(value, otherAxis)
        else:
            value = otherAxis * 0 + value + 0.1
            ax.plot(otherAxis, value)
    plt.show()
```

![](img\mla6-2.png)

图中，一条直线就表示一个基分类器。

发现简单的数据集似乎效果不错后，我们可以将其应用到稍复杂的数据上，例如支持向量机中用过的非线性可分的数据集：

```python
def loadSimpleData():
    path1 = r'data/plrx/simpleTest.txt'
    path2 = r'data/mlia/Ch06/testSetRBF.txt'
    return loadDataSet(path2)
```

稍微修改一下绘图函数后（调整绘图界限，标记样式大小等）再运行程序：

```
...
{'value': 0.39274100000000001, 'order': 1, 'err': 0.31394747236877979, 'labelList': [1.0, -1.0]}
迭代完成，正确率为 0.99
{'value': 0.229465, 'order': 0, 'err': 0.35502806267205234, 'labelList': [1.0, -1.0]}
迭代完成，正确率为 0.99
{'value': 0.957812, 'order': 0, 'err': 0.32121576055989365, 'labelList': [-1.0, 1.0]}
迭代完成，正确率为 1.0
```

![](img\mla6-3.png)

这里我将迭代次数设为了100次，因为担心可能拟合次数不够，但从输出信息来看，它并没有迭代到100次就到了100%的正确率，由此又需要担心是否发生过拟合从而重新调整迭代次数，不过调参本身也是一项不简单，反而可以说是非常麻烦的工作，这里仅是将正确率作为观察对象，迭代次数作为参数来调整模型，但从[模型评估](https://zyzypeter.github.io/2017/08/11/machine-learning-ch14-model-evaluate/)一章的笔记中，我们可以知道，在现实问题中仅考虑正确率是远远不够的，另外，对数据集的训练和应用也是要复杂的多的。

何况，从理论上来说只要迭代次数够大，AdaBoost都是可以在训练集上达到100%的正确率的。