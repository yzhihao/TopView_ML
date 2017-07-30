from numpy import  *
from math import *
def loadDataSet(fileName):
    with open(fileName,'r') as file:
        data = file.readlines()
        dataMat = []
        labelMat = []
        for line in data:
            currLine = line.strip().split(',')
            labelMat.append(currLine[-1])
            print(currLine)
            currLine[2] = 1.0
            dataMat.append(currLine[0:3])

    return dataMat,labelMat

def sigmoid(inX):
    try:
        result = 1.0 / (1 + exp(-inX))
    except:
        return 0
    return result


def training (X, Y, numIter=150):
    m,n = shape(X)
    weights  = ones(n)
    weights = mat(weights)
    for i in range(numIter):
        dataIndex = range(m)
        for j in range(m):
            alpha = 0.1/(1.0+j+i) + 0.0001
            randomIndex = int(random.uniform(0,m))
            h = sigmoid(weights*X[randomIndex].T)
            error = Y[randomIndex] - h
            weights = weights + alpha * error * X[randomIndex]
    return weights

def classfiy(inX,weights):

    y = sigmoid(weights * inX.T)
    if y > 0.5:
        return 1
    else:
        return 0



def main():
    trainingSet = '/Users/Chok-John/Downloads/ex2data1.txt'
    testSet = '/Users/Chok-John/Desktop/logisticTest.txt'
    dataMat,labelMat = loadDataSet(trainingSet)
    X = mat(dataMat,dtype= float64)
    Y = array(labelMat,dtype=float64)

    weights = training(X,Y,numIter=2500)
    testX,testY = loadDataSet(testSet)
    testX = mat(testX,dtype=float64)
    testY = array(testY,dtype=float64)
    right = 0
    error = 0
    for i in range(len(testX)):
        if int(testY[i]) == classfiy(testX[i],weights):
            right = right + 1
        else:
            error = error + 1
    print(1.0*right/(right +error))

main()