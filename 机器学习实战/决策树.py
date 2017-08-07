from numpy import *
from math import *
import pandas as pd


def loadDataSet():
    with open('决策树训练集.txt','r') as f:
        lines = f.readlines()
        data = []

        for i in lines:
            line = i.strip().split('\t')
            data.append(line)

        return data


def calcShannonEnt(dataSet,feature,label):
    emmm = feature.copy()
    emmm.append(label)
    series = pd.DataFrame(dataSet)[emmm]

    length = series.__len__()



    kind = series[label].value_counts()
    shannonEnt = 0.0
    for i in kind.keys():
        prob = float(kind[i])/length
        shannonEnt -= prob * log(prob,2)
    return shannonEnt




def EntGain(dataSet,feature):
    series = pd.DataFrame(dataSet)
    dataLength,n = series.shape
    EntList = []
    className = [key for key in series[n-1].value_counts().keys()] # 标签的所有取值
    HD = calcShannonEnt(dataSet,feature,n-1)
    print('HD = ', HD)
    for j in range(n-1):
        if j in feature:
            fecture = series[j].value_counts()
        else:
            EntList.append(0)
            continue
        out = 0
        for i in fecture.keys():
            df = series[series[j].isin([i])]
            length = df.__len__()  # 某一个具体特征的数量

            df = df[n-1].value_counts()# 第j个特征对应的标签

            Pi = float(fecture[i]) / dataLength
            inner = 0
            for key in className:


                if key in df.keys():
                    a = float(df[key])/length

                    b = a*log(a,2)
                    inner += b

            out += inner*Pi
        output = HD + out
        EntList.append(output)
    return EntList


def spiltData(dataSet,dim):
    dataSet = pd.DataFrame(dataSet)

    spilt = []

    for key in dataSet[dim].value_counts().keys() :

        data = {key:dataSet[dataSet[dim].isin([key])]}

        spilt.append(data)
    return spilt

def featureKinds(dataSet,dim):
    dataSet = pd.DataFrame(dataSet)
    key = dataSet[dim].keys()
    length = len(key)
    return length


class Node(object):
    def __init__(self):
        self.data = None
        self.son = []
        self.feature = []
        self.spiltFeature = None
        self.ittr = None
        self.flag = 'node'
        self.label = None



class tree(Node):
    def __init__(self,dataSet):
        super(Node).__init__()

        self.flag = 'root'
        self.ittr = None
        self.data = dataSet[:,:-1]
        self.feature = [i for i in range(len(dataSet[0])-1)] # 第几个特征
        EntList = EntGain(dataSet,self.feature) # 信息增益
        print(EntList)
        self.spiltFeature = argmax(EntList) # 信息增益最大的特征
        spilt = spiltData(dataSet,self.spiltFeature) # 按该特征划分数据集
        self.feature.remove(self.spiltFeature) # 移除该特征，该数据要传给叶子
        count = len(spilt)
        i = 0

        sonList = []
        while i < count:
            son = self.CreateTree(spilt[i],self.feature)
            sonList.append(son)
            i = i + 1
        self.son = sonList

    def CreateTree(self,dataSet,feature):
        node = Node()
        node.feature = feature.copy()

        node.ittr = list(dataSet.keys())[0]
        data = list(dataSet.values())[0]
        flag = self.keepOn(data,feature)

        n = shape(data)[1] - 1

        if flag == -1:
            node.flag = 'leaf'

            node.label = str(data[n].value_counts().argmax())

            return node
        if flag == -2:
            node.flag = 'leaf'

            node.label = data[n].value_counts().argmax()

            return node
        if flag == 1:
            EntList = EntGain(data,feature)

            node.spiltFeature = argmax(EntList)  # 信息增益最大的特征

            spilt = spiltData(data, node.spiltFeature)  # 按该特征划分数据集

            node.feature.remove(node.spiltFeature)  # 移除该特征，该数据要传给叶子

            count = len(spilt)
            i = 0
            sonList = []
            while i < count:
                son = self.CreateTree(spilt[i], feature)
                print(node.ittr)
                print(spilt[i])
                print(feature)
                print('------------------------------')
                sonList.append(son)
                i = i + 1
            node.son = sonList
            return node



    def keepOn(self,dataSet,feature):
        n = shape(dataSet)[1] - 1
        if len(dataSet[n].value_counts().keys()) == 1:
            return -1 # 标签只剩下一类
        if len(feature) == 0:
            return -2 # 说明特征集为空

        return 1







class hypothesis(object):
    def __init__(self):
        dataSet = array(loadDataSet())
        self.tree = tree(dataSet)

    def outputFunction(self,x):
        curNode = self.tree
        while curNode.flag != 'leaf':
            feature = x[curNode.spiltFeature]
            for i in curNode.son:
                if feature == i.ittr:
                    curNode = i
                    break
        return curNode.label

h = hypothesis()
x = ['young',	'hyper'	,'yes'	,'normal']
y = h.outputFunction(x)
print(y)
