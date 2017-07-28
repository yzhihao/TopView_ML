# Python机器学习实战 第四章 kd树

资料来源参考：

人民邮电出版社 Peter Harrington《机器学习实战》第二章

清华大学出版社 周志华 《机器学习》 第十章 降维与度量学习

清华大学出版社 李航 《统计学习方法》 第三章 k近邻法

[我的博客 机器学习 第七章 k近邻](https://zyzypeter.github.io/2017/07/27/machine-learning-ch7-kNN/)

[数据集来源 Github:Peter Harrington](https://github.com/pbharrin/machinelearninginaction)

本章数据集来源：Ch2

## 读取数据集

### 数据集内容

经过了三章，我想我们在开始建立模型之前的第一步都会习惯是读取数据集了。

首先我们先观察一下我们的数据集（我们这里用的是Peter Harrington 《机器学习实战》第二章提供的约会信息）：

![](img\mla4-1.png)

Windows的记事本不是很兼容Peter Harrington 提供的数据集，尤其体现在一些空白字符。所以我们还是在这里说明一下，数据集提供的内容：

该数据集给了我们1000条约会相关的数据，一条信息内容如下：

```
40920	8.326976	0.953952	largeDoses
```

从左到右依次为，该名人员：
1. 每年获得的飞行常客里程数（特征1）
2. 玩视频游戏所耗时间百分比（特征2）
3. 每周消费的冰淇淋公升数（特征3）
4. 对该人员的偏好程度（类别）

这里我用的书上的原话，但显然不是很好理解，我们直接将其简单地理解为括号里面的内容就好。

那么很显然，这次我们写的kd树的用处就是当我们有一个测试样本时，可以通过该样本的三个特征（里程数，百分比，公升数）来推断出这个样本的类别（偏好程度）。

### 读取训练样本集

在直到数据集的构成内容后，我们就可以着手编写代码读取数据集的内容了：

```python
def loadDataSet():
    fr = open(r'data\mlia\Ch02\datingTestSet.txt')
    dataSet = []
    for line in fr.readlines():
        lineArr = line.strip().split()
        data = Data(lineArr)
        dataSet.append(data)
    return dataSet
```

这次我们就用简单的列表来保存这些数据，当然，喜欢的话也可以用我们上一章用过的pandas的DataFrame。

`Data`是我们自己需要编写的一个类：

```python
class Data(object):
    def __init__(self, attributeList):
        """
        :type attributeList: list
        """
        self.attributeList = []
        for attribute in attributeList:
            if attribute is not attributeList[-1]:
                attribute = float(attribute)
            self.attributeList.append(attribute)
```

将一条数据实例化为一个对象会更方便我们之后的操作。另外，这里我们还将得到的信息中的三个特征值保存为了`float`格式，这方便我们之后用他们进行运算。

## 构造kd树

读取完数据后，我们就需要着手构建kd树了。

### 基本流程

虽然我们应该已经看过构造kd树的基本流程了，但我觉得我们还是再在这儿了解一遍会更加清晰：

1. 构造根节点，根节点对应于包含T的k维空间的超矩形区域
2. 用超平面划分根节点为两部分，一部分作为根节点的左子节点，一部分作为根节点的右子节点，并将落在超平面上的样本保存在根节点。
3. 算法移动到子节点，用超平面划分该节点的左右子节点，并将落在超平面上的样本点保存
4. 递归第三步，直到所有的同类样本都被划分完毕

### 节点类

因为kd树本身的特性，我们这一次不能像决策树那样简单地用词典代替树形结构，因此，我们这次需要先写一个节点的类：

```python
class Node(object):
    def __init__(self, axis, depth):
        self.father = None #指向父节点
        self.leftSub = None #指向左子节点
        self.rightSub = None #指向右子节点
        self.axis = axis #与超平面垂直的轴
        self.dataInNode = set()# 用于存放保存在该节点的样本
        self.depth = depth #节点的深度
        self.label = None #节点中样本最多的类别（不仅仅是保存在该节点的样本，还包括保存在该节点的子节点的样本）
        self.mid = 0 #切分节点时的轴上坐标
        self.flag = 0 #标记该节点有没有被搜索过
```

### 构造树

有了节点的类后，我们可以开始着手写构造树的函数

#### 主函数

我们先写一个构造树的主函数：

```python
def createTree():
    dataSet = loadDataSet()
    root = Node(0, 1)
    root = treeGenerate(dataSet, root, None)
    return root
```

初始化根节点，并表示根节点的划分超平面为第一个特征轴，深度为1.

`treeGenerate`就是我们用来递归构造节点以建立一棵完整的树的函数。

#### 递归构造节点

这一步是我们构造树的关键,不过在此之前我们先写一个计算中位数的函数用来计算超平面与特征轴垂直相交的位置：

```python
def midCount(midCountList):
    midCountList.sort()
    length = len(midCountList)
    if length % 2 == 0:
        mid = float(midCountList[length / 2 - 1] + midCountList[length / 2]) / 2
    else:
        mid = midCountList[(length - 1) / 2]
    return mid
```

函数接收由该特征轴上的所有特征值组成的列表`midCountList`。

有了计算中位数的函数后，我们就可以写出递归构造节点的函数：

```python
def treeGenerate(dataSet, currentNode, fatherNode):
    currentNode.father = fatherNode
    # 将当前节点与父节点连接
    if dataSet is None:
        # 如果传入样本集为空
        return None
    length = len(dataSet)
    # 获得样本集中的样本数目
    labelCountDict = {}
    for data in dataSet:
        if data.attributeList[-1] not in labelCountDict.keys():
            labelCountDict[data.attributeList[-1]] = 1
        else:
            labelCountDict[data.attributeList[-1]] += 1
    # 对样本集中的样本类别计数
    if len(labelCountDict) == 1:
        # 如果样本集中所有样本都是同一类别，则将样本保存到该节点，将该节点设为叶节点并返还
        for data in dataSet:
            currentNode.dataInNode.add(data)
        currentNode.label = max(labelCountDict)
        # 设定叶节点的类别
        return currentNode
    if length >= 2:
        # 如果有不少于两个不同类别的样本在样本集中
        axis = currentNode.axis
        # 获得切分的维度
        midCountList = []
        for data in dataSet:
            midCountList.append(data.attributeList[axis])
        mid = midCount(midCountList)
        currentNode.mid = mid
        # 计算该维度上的特征值的中位数,并将其保存到节点
        leftDataSet = []
        rightDataSet = []
        labelCountDict = {}
        for data in dataSet:
            if data.attributeList[axis] == mid:
                currentNode.dataInNode.add(data)
                if data.attributeList[-1] not in labelCountDict:
                    labelCountDict[data.attributeList[-1]] = 1
                else:
                    labelCountDict[data.attributeList[-1]] += 1
            elif data.attributeList[axis] < mid:
                leftDataSet.append(data)
            else:
                rightDataSet.append(data)
        # 切分样本集，落在超平面上的样本保存在本节点，小于的划分到左子节点，大于的划分到右子节点
        if len(labelCountDict) != 0:
            currentNode.label = max(labelCountDict)
        # 设定当前节点的类别为样本集中最多的类别
        axis = currentNode.depth % (len(dataSet[0].attributeList) - 1)
        # 结算下一个切分维度 下一个切分维度=当前节点深度（mod 样本属性总数）+1
        leftNode = Node(axis, currentNode.depth + 1)
        rightNode = Node(axis, currentNode.depth + 1)
        currentNode.leftSub = treeGenerate(leftDataSet, leftNode, currentNode)
        currentNode.rightSub = treeGenerate(rightDataSet, rightNode, currentNode)
        # 递归生成左右子节点
        return currentNode
```

这里我们需要明确的是，计算当前节点的切分特征轴的公式为：

$$
l=j(mod k)+1
$$

l表示切分哪一个特征轴，j表示节点深度，k表示特征总数（在这个例子中就是里程数，百分比，公升数，共三个特征）。当然，代码中因为一些计数以及索引从零开始数之类的原因，需要进行一些小小的修改。这个计算方式仅是为了能够在划分时轮流用到所有的特征，想优化的话还可以用方差或者信息增益之类的方法来选特征轴，不过在这里我们就暂且用最原始简单的方法吧。

至此，我们就完成了kd树的构建。我们可以调用一下`createTree`函数，然后打印一些信息或者plot出我们kd树的图像来看看内容如何。也可以剪枝或者用一些其它的方式优化一下我们的kd树。

## 搜索kd树

构建完成之后，我们还需要直到如何使用kd树，这里我们暂且用最简单地“最近邻法”搜索kd树，更复杂的方法我们可以在以后尝试。

### 基本流程

k-d树查询算法的简要说明：
1. 从root节点开始，DFS搜索直到叶子节点，同时在stack中顺序存储已经访问的节点。
2. 如果搜索到叶子节点，当前的叶子节点被设为最近邻节点。
3. 然后通过stack回溯:
如果当前点的距离比最近邻点距离近，更新最近邻节点.
然后检查以最近距离为半径的圆是否和父节点的超平面相交.
如果相交，则必须到父节点的另外一侧，用同样的DFS搜索法，开始检查最近邻节点。
如果不相交，则继续往上回溯，而父节点的另一侧子节点都被淘汰，不再考虑的范围中.
4. 当搜索回到root节点时，搜索完成，得到最近邻节点。

资料参考来源：[Losteng的博客](http://blog.csdn.net/losteng/article/details/50893739)

### 测试样本类

我这里将测试样本类与训练样本类分写，主要是方便我自己的辨认，但事实上，如果喜欢的话也可以将两者合二为一，因为我们这里用到的测试样本和训练样本并没有多大的区别：

```python
class TestData(object):
    def __init__(self, attributeList):
        """
        :type attributeList: list
        """
        self.distance = None
        self.attributeList = []
        for attribute in attributeList:
            if attribute is not attributeList[-1]:
                attribute = float(attribute)
            self.attributeList.append(attribute)
        self.label = None

    def distanceCount(self, data):
        dataAttributeMat = mat(data.attributeList[:-1])
        targetMat = mat(self.attributeList[:-1])
        # 用样本点的属性值生成特征向量
        distance = sqrt(float(sum((dataAttributeMat - targetMat).transpose() * (dataAttributeMat - targetMat))))
        # 计算该测试样本点与训练样本点data的欧氏距离
        return distance

    def distanceToHyperPlane(self, axis, mid):
        targetMat = mat(self.attributeList[:-1])
        m, n = shape(targetMat)
        planeVector = zeros(n)
        planeVector = mat(planeVector)
        planeVector[0, axis] = 1
        distance = abs(planeVector * targetMat.transpose() - mid)
        return distance[0, 0]
```

实例属性添加了一个`label`和一个`distance`分别表示与这个测试样本匹配的最近样本点的类别和与该点的距离。

下面添加的两个实例方法`distanceCount`和`distanceToHyperPlane`分别用来计算测试样本点到给定样本点`data`的欧氏距离，和测试样本点到给定超平面的距离。

超平面的方程：

$$
w*x+b=0
$$

其中w为超平面的法向量，计算点到超平面的欧氏距离的公式：

$$
d=\frac{1}{\mid\mid w\mid\mid}\mid w·x+b \mid
$$

### 向下搜索叶节点

接着我们需要构建向下搜索判断测试样本点所在叶节点的函数：

```python
def searchLeaf(target, node):
    """
    :type node: Node
    :type target: TestData
    """
    if target is None:
        return
    if node.leftSub is None and node.rightSub is None:
        target.label = node.label
        return node
    # 如果当前节点左右子节点为空，则返还当前节点
    axis = node.axis
    # 获取当前节点的切分轴
    mid = node.mid
    # 获得当前节点的切分中位数
    if target.attributeList[axis] < mid:
        leafNode = searchLeaf(target, node.leftSub)
        return leafNode
    else:
        leafNode = searchLeaf(target, node.rightSub)
        return leafNode
```

这只是搜索一个测试样本，但测试集一般都不止一个测试样本，因此我们还需要将他们整合：

```python
def searchLeaves(targetSet, root):
    """
    :type root: Node
    :type targetSet: List
    """
    leafNodes = {}
    for target in targetSet:
        leafNodes[target] = searchLeaf(target, root)
    return leafNodes
```

### 回溯函数

在确定测试样本所在的叶节点后，我们就可以用回溯函数来向上搜索与测试样本最近的训练样本点了：

```python
def searchData(target, node):
    """
    :type node: Node
    :type target: TestData
    """
    if target is None or node is None:
        return
    node.flag = 1
    # 标记该节点已被搜寻过
    distanceCount = {}
    for data in node.dataInNode:
        distance = target.distanceCount(data)
        distanceCount[data] = distance
        # 计算测试样本点与节点中每个样本点的距离
    if target.distance is None:
        data = min(distanceCount)
        target.label = data.attributeList[-1]
        target.distance = target.distanceCount(data)
        # 如果测试样本点尚未匹配当前最近点，则匹配最近样本点，并将该样本点的距离和类别存入测试样本点
    else:
        if len(distanceCount) != 0:
            if target.distance > min(distanceCount):
                data = min(distanceCount)
                target.label = data.attributeList[-1]
                target.distance = target.distanceCount(data)
                # 如果找到比当前最近点更近的样本点，则将该样本点设为当前最近点
    father = node.father
    # 进入父节点
    if father is None:
        # 如果搜索到了根节点
        return target
    axis = father.axis
    mid = father.mid
    distance = target.distanceToHyperPlane(axis, mid)
    # 计算当前样本点到父节点超平面距离
    if distance > target.distance or (father.leftSub.flag != 0 and father.rightSub.flag != 0):
        # 如果样本点到当前最近点的距离比到超平面的距离小,或者该父节点的所有子节点已经被搜索过
        target = searchData(target, father)
        # 搜索父节点
        return target
    else:
        # 如果样本点到当前最近点的距离比到超平面的距离大
        if father.leftSub.flag == 0:
            # 锁定父节点的另一个非当前节点的子节点
            leafNode = searchLeaf(target, father.leftSub)
            # 向下搜索该节点直到叶节点
            target = searchData(target, leafNode)
            # 从搜索到的叶节点向上搜索
            return target
        elif father.rightSub.flag == 0:
            leafNode = searchLeaf(target, father.rightSub)
            # 向下搜索该节点直到叶节点
            target = searchData(target, leafNode)
            # 从搜索到的叶节点向上搜索
            return target
```

### 试验测试集

最后我们可以用测试集试一下我们训练的模型。

我的做法是将原本 Peter Harrington 提供的数据集分成两部分，一部分（90%）作为训练集，一部分（10%）作为测试集，然后我们写一下调用模型的函数：

```python
def test():
    root = createTree()
    targetSet = loadTarget()
    leafNodes = searchLeaves(targetSet, root)
    resultCount = {'right': 0, 'wrong': 0}
    for target, node in leafNodes.items():
        target = searchData(target, node)
        if target.label == target.attributeList[-1]:
            resultCount['right'] += 1
        else:
            resultCount['wrong'] += 1
    print '正确率为:', str(float(resultCount['right']) / (resultCount['right'] + resultCount['wrong'])*100)+"%"

test()
```

输出

```
正确率为: 86.4406779661%
```

嗯，看来效果还不算太坏。