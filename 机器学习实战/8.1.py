from numpy import  *
import matplotlib.pyplot as plt
def loadDataSet(fileName):
    numFeat = len((open(fileName)).readline().split('\t')) - 1

    dataMat =[]
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')

        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
 #           print(lineArr)
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def standRegres(xArr,yArr):
    xMat = mat(xArr);
    yMat = mat(yArr).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0:
        print("this matrix is singular,cannot do inverse")
        return
    ws =xTx.I*(xMat.T*yMat)
    return  ws

fileName = '/Users/Chok-John/Desktop/machinelearninginaction-master/Ch08/ex0.txt'
X,Y = loadDataSet(fileName)
ws = standRegres(X,Y)
c = ws.A[1,0]
b = ws.A[0,0]

X = array(X)[:,1]
x_1 = linspace(0, 2, 100)


file = '/Users/Chok-John/Desktop/machinelearninginaction-master/Ch08/ex1.txt'
i,o = loadDataSet(file)

y_1 = [ c*x +b for x in x_1 ]
plt.figure(figsize=(20,10))
plt.plot(x_1,y_1)
i_1 = array(i)[:,1]


plt.scatter(X, Y, label="线性回归$",s=50, color="red", marker=".")
plt.scatter(i_1, o, label="线性回归2$",s=50, color="g", marker=".")
plt.show()

