# Python 机器学习实战 第二章 朴素贝叶斯

资料来源参考：
人民邮电出版社 Peter Harrington《机器学习实战》第四章
[数据集来源 Github:Peter Harrington](https://github.com/pbharrin/machinelearninginaction)
本章数据集来源：Ch4
[机器学习 第五章 朴素贝叶斯算法](https://zyzypeter.github.io/2017/07/22/machine-learning-ch5-Naive-Bayes/)

## 文本分类问题

现在，我们要做一个垃圾邮件分类器。

我们知道，我们收到的邮件可以粗略地分为两类，“垃圾”（spam）或者“非垃圾”（ham），而体现一个邮件是否垃圾的特征不像是我们逻辑回归所遇见的那样，只有少量的特征值。事实上，邮件中的每一个词都会是这封邮件的特征（当然我们可以排除掉一些没有实际内涵的词），如果我们还是使用逻辑回归，那么我们可能就需要非常非常多的参数，这会导致计算机的开销过大。因此，对于这种特殊的**文本分类问题**，我们需要有比逻辑回归模型更合适的分类器。

## 朴素贝叶斯算法

朴素贝叶斯算法便是用于文本分类的一个比较好的模型，不同于**判别学习算法**（像是逻辑回归）它是一种**生成学习算法**（这在我的机器学习理论笔记中有记述，这里就不再赘述），它的原理是先分别对possitive class和negative class建立模型，然后再通过这两个模型对测试集中的未知邮件进行判断。

### 词汇表

首先，我们需要有一个**词典**，它的内容是这些所有邮件可能包含的词汇，有时候我们可以从网上或者别的什么地方获得，但最常见的方法是遍历训练集然后将训练集中的每一个词加入词典：

```python
import os
import re

def loadVocabulary():
    pattern=re.compile(r"[^a-zA-Z]")
    filePath=r"data\mlia\Ch04"
    spamHamSwitcher=[r"\ham", r"\spam"]
    vocabulary=set()
    for i in range(2):
        for file in os.listdir(filePath+spamHamSwitcher[i]):# 遍历训练集中邮件所在的文件夹中的所有文件
            fr=open(filePath+spamHamSwitcher[i]+r"/"+file,"r")# 以只读模式打开一个样本
            for line in fr.readlines():
                wordArr=line.strip().split()
                for word in wordArr:
                    word=re.sub(pattern,"",word)
                    if word is not "":
                        if word not in vocabulary:
                            vocabulary.append(word)# 扩充词典
    return vocabulary
print loadVocabulary()
```
```
>>set(['all', 'code', 'focus', 'Superb', 'prices', 'Does', 'Take', 'go', '...
```

我们这里遍历了每个样本采集词汇，然后通过正则去除掉词语中的特殊字符，例如“，”或者“.”，因为很显然这些词语没有什么用，并且会干扰到我们收集的词汇。举个例子，像是"school?"和"school"，我们如果不用正则合理匹配，那么他们就会被当成两个不同的词放在词汇表中，这是相当不合理的。并且，每个词汇都在词汇表中都必须保证是唯一有序的，因此我们加了判断条件并用list类保存。

形象的说，词典就是一个包含所有邮件中可能出现的词汇的有序序列。

### 模型建立

#### 读取数据

模型建立的第一步是读取数据：

```python
def loadDataSet(vocabulary):
    pattern=re.compile(r"[^a-zA-Z]")
    filePath=r"data\mlia\Ch04"
    spamHamSwitcher=[r"\ham", r"\spam"]
    hamMat=[]
    spamMat=[]
    for i in range(2):
        for file in os.listdir(filePath+spamHamSwitcher[i]):
            fr=open(filePath+spamHamSwitcher[i]+r"/"+file,"r")
            hamVoc=zeros(len(vocabulary))
            spamVoc=zeros(len(vocabulary))
            for line in fr.readlines():
                lineArr=line.strip().split()
                word = re.sub(pattern, "", word)
                for word in lineArr:
                    if word in vocabulary:
                        if i==0:
                            hamVoc[vocabulary.index(word)]=1
                        else:
                            spamVoc[vocabulary.index(word)]=1
            if i==0:
                hamMat.append(hamVoc)
            else:
                spamMat.append(spamVoc)
    return hamMat,spamMat
```

操作与取词汇表类似，但是我们不能将两个函数整合，因为在读取训练集样本时我们还要让每一个样本内的词汇与词汇集中的词比对，因此在拥有词汇表之前我们是无法读取数据的。

#### 极大似然估计函数

然后我们可以根据得到的两个表建立计算参数极大似然估计的模型：

```python
def naiveBayes(hamMat, spamMat):
    hamCount, n1 = shape(hamMat)  # 获取正常邮件数量
    spamCount, n2 = shape(spamMat)  # 获取垃圾邮件数量
    totalCount = hamCount + spamCount  # 获取邮件总数
    weights = zeros((len(hamMat[0]), len(spamMat[0]), 1))  # 创建参数向量组
    for j in range(len(hamMat[0])):  # 对于词典中的每一个词
        for i in range(hamCount):  # 对于每一个正常邮件
            weights[0][j] = weights[0][j] + hamMat[i][j]
        weights[0][j] = (float(weights[0][j]) + 1) / (hamCount + 2)  # 计算参数Φ1
        for i in range(spamCount):
            weights[1][j] = weights[1][j] + spamMat[i][j]
        weights[1][j] = (float(weights[1][j]) + 1) / (spamCount + 2)  # 计算参数Φ0
    weights[2][0] = float(spamCount) / totalCount  # 计算参数Φy
    return weights
```

计算参数的公式如下：

![](img\mla2-1.png)

不过我们可以看到，与这个公式相比，我们做了一点小小的改动：在分子加上1，分母加上2。这是因为我们还应用了拉普拉斯平滑（可以在我记录的关于朴素贝叶斯的同一章笔记中找到关于拉普拉斯平滑的内容，这里就不再赘述），因此，改动后的极大似然估计应为：

![](img\mla2-2.png)

#### 构造分类器

藉由这个函数得到参数之后，我们就可以进一步构造分类器，分类器的公式：

![](img\mla2-3.png)

因此我们有：

```python
def classification(weights, target, vocabulary):
    hamRate = 1
    spamRate = 1
    pattern = re.compile(r"[^a-zA-Z]")
    length = len(vocabulary)  # 获取词典长度
    fileVoc = zeros(length)
    for line in target.readlines():  # 将测试邮件内容解析为特征向量
        wordArr = line.strip().split()
        for word in wordArr:
            word = re.sub(pattern, "", word)
            if word in vocabulary:
                fileVoc[vocabulary.index(word)] = 1
    for i in range(length):# 计算如果该邮件是正常邮件，那么它的特征为正常邮件特征的概率
        temp = float(weights[0][i] * fileVoc[i])
        if temp != 0:
            hamRate = float(hamRate * temp)
    for i in range(length):# 计算如果该邮件是垃圾邮件，那么它的特征为垃圾邮件特征的概率
        temp = float(weights[1][i] * fileVoc[i])
        if temp != 0:
            spamRate = float(spamRate * temp)
    result = (spamRate * weights[2][0]) / (hamRate * (1 - weights[2][0]) + spamRate * weights[2][0])
    # 计算得到该邮件是垃圾邮件的概率
    return result
```

参数`target`接受一个'file'类对象，这个对象便可以是任意的一个测试邮件。

#### 测试

分类器构造完成后，我们可以让它在我们自己的训练集中遍历一遍，测试误差：

```python
def test(classification, weights, vocabulary):
    pattern = re.compile(r"[^a-zA-Z]")
    filePath = r"data\mlia\Ch04"
    spamHamSwitcher = [r"\ham", r"\spam"]
    error = 0
    for i in range(2):
        for file in os.listdir(filePath + spamHamSwitcher[i]):
            fr = open(filePath + spamHamSwitcher[i] + r"/" + file, "r")
            error = error + square(float(i - classification(weights, fr, vocabulary)))
    return error
    
error = test(classification,weights,vocabulary)
print error
```

```
>>1.03048629097e-05
```

不过当然了，在自己的训练集上如果误差都很大，那肯定是出问题的情况。所以我们还可以用一些简单地方法加入测试集测试一下。

这是我自己的邮箱中的一封邮件，他没有包含在训练集中：

```
The page build completed successfully, but returned the following warning for the `master` branch:

You are attempting to use a Jekyll theme, "minimal-mistakes-jekyll", which is not supported by GitHub Pages. Please visit https://pages.github.com/themes/ for a list of supported themes. If you are using the "theme" configuration variable for something other than a Jekyll theme, we recommend you rename this variable throughout your site. For more information, see https://help.github.com/articles/adding-a-jekyll-theme-to-your-github-pages-site/.

For information on troubleshooting Jekyll see:

  https://help.github.com/articles/troubleshooting-jekyll-builds

If you have any questions you can contact us by replying to this email.
```

我们把它放入'test.txt'文件中，然后用代码测试：

```python
fr=open(r'test.txt')
result=classification(weights,fr,vocabulary)
if result>0.5:
    print "spam"
else:
    print "ham"
```

```
>> ham
```

当然，有兴趣的话还可以用其它的邮件试一试，不过这里当然是仅限英文邮件，若是中文邮件我们还需要应用对中文分词的功能，那又会有一些区别了。

不过你在看了训练集中的一些邮件之后，或许会觉得这个模型的计算还是不够严谨，这是自然的。毕竟这只是一个较为简单粗糙的模型，而且训练集的内容也很少（事实上，我们用的训练集可能不到实际可能会用的训练集的大小的百分之一），有很多词汇词汇表也都是不包含的（像上述例子，就由“github”，“jekyll”等等），还有对一些特殊句子的处理（像是url链接），这些都会对我们的模型造成很严重的影响。