from numpy import *
import matplotlib.pyplot as plt
import copy


def loadDataSet(fileName):
    # 读取数据函数
    dataMat = [];
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
    return dataMat

def RandomPoint(dataMatIn,k):
    # 获取随机点函数，以数据的最值为边界
    xMAX = max(dataMatIn[:,0])
    xMin = min(dataMatIn[:,0])
    yMax = max(dataMatIn[:,1])
    yMin = min(dataMatIn[:,1])
    randomPoint = []
    check = set()
    i = 0
    while(i<k):
        randomX = random.uniform(xMin,xMAX)
        randomY = random.uniform(yMin,yMax)
        check.add((randomX,randomY))
        if len(check)!= i + 1 :
            continue
        randomPoint.append([randomX,randomY])
        i = i +1


    return randomPoint

def calDistance(dataMatIn,randomPoint):
    # 计算距离
    distance = []
    n = shape(dataMatIn)[1]
    for i in range(len(dataMatIn)):
        d = 0
        for j in range(n):
            t = square(dataMatIn[i][j] - randomPoint[j])
            d += t
        distance.append(sqrt(d))
    return distance

def K_means(dataMatIn, k):

    randomPoint = RandomPoint(dataMatIn, 2)

    while(1):
        p = copy.deepcopy(randomPoint)
        label = []
        for i in range(k):
            label.append([])
        distance = []
        for i in randomPoint:
            distance.append(calDistance(dataMatIn,i))
        distance = array(distance)
        index = []
        for i in range(len(dataMatIn)):
            index.append(argmin(distance[:,i]))
        value = []
        for i in range(len(index)):
            label[index[i]].append(dataMatIn[i])
        label = array(label)
        for i in range(k):
          for j in range(len(randomPoint[0])):
              randomPoint[i][j] = mean(array([x[j] for x in label[i]]))
        if p == randomPoint:
            break
        else:
            p = randomPoint


    return label,randomPoint



dataMat = loadDataSet('/Users/Chok-John/Desktop/machinelearninginaction-master/Ch06/testSet.txt')
randomPoint = RandomPoint(array(dataMat),2)

b,r= K_means(array(dataMat),2)

# 下面是画图
r = array(r)
c = array(b[0])
a = array(b[1])

plt.scatter(c[:,0],c[:,1],c = 'red')
plt.scatter(a[:,0],a[:,1],c = 'g')
plt.scatter(r[:,0],r[:,1],c = 'b')
plt.show()
