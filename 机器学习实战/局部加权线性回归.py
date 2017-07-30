from numpy import  *
import matplotlib.pyplot as plt
def loadDataSet(fileName):      #general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t')) - 1 #get number of fields
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def lwlr(testPoint,xArr,yArr,k=1.0):
    xMat = mat(xArr); yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    for j in range(m):                      #next 2 lines create weights matrix
        diffMat = testPoint - xMat[j,:]     #

        weights[j,j] = exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * ws


def lwlrTest (testArr,xArr,yArr,k=1.0):
    m = shape(testArr)[0]
    yHat =  zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i],xArr,yArr,k)
    return yHat

dataMat,labelMat = loadDataSet('/Users/Chok-John/Desktop/machinelearninginaction-master/Ch08/ex0.txt')
testPoint = loadDataSet('/Users/Chok-John/Desktop/machinelearninginaction-master/Ch08/ex1.txt')
y = lwlrTest(dataMat,dataMat,labelMat,k=0.1)
fig = plt.figure()
ax = fig.add_subplot(111)
xMat = mat(dataMat)
srtInd = xMat[:,1].argsort(0)
xSort = xMat[srtInd][:,0,:]



ax.plot(xSort[:,1],y[srtInd])
ax.scatter(xMat[:,1].flatten().A[0],mat(labelMat).T.flatten().A[0],s=2,c = 'red')
plt.show()
