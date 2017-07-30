from numpy import *
import matplotlib.pyplot as plt
import copy
x = [
    [1,2],
    [1,1],
    [1,3],
    [4.6,3],
    [4,7],
    [3, 2],
    [4, 5],
    [2, 3],
    [5.3, 2],
    [6, 7],
    [2.5, 3.5],
    [2, 7],
    [4, 2],
    [5, 5],
    [6, 9],
    [4,7]]
z =copy.deepcopy(x)
y = \
    [-1,
     -1,
     -1,
     1,
     1,
     -1,
     1,
     -1,
     1,
     1,
     -1,
    -1,
     -1,
     1,
     1,
     1]
def sign(w,x):
    if (w.T*x) >= 0:
        return 1
    return -1

def classfiy(x,y,eta):
    for j in x:

        j.append(1)

    m,n = shape(x)
    w = ones(n)
    # print(w,n,m)
    x = mat(x)
    w = mat(w)

    i = 0
    while i < m :
        # print(w)
        if y[i]*(w*x[i].T) <= 0 :
            w = w + eta*y[i]*x[i]
            # w_next = w - 2*eta*w
            # while y[i]*(w_next*x[i].T) <= 0 and ww(w) > ww(w_next):
            #     w = w_next
            #     w_next = w - 2*eta*w
            #     print(w)

            i = 0
        i = i + 1
    return w

def ww(w):
    m,n = shape(w)
    sum = 0
    for i in range(m):
        for j in range(n):
            t = w[i,j] * w[i,j]
            sum += t
    return sqrt(sum)

def d(x,y,w):


    p = 1.0 / sqrt(w[0, 0] * w[0, 0] + w[0, 1] * w[0, 1] + w[0, 2] * w[0, 2])
    x = mat(x)
    d = []
    for i in range(len(x)):
        e = y[i]*(w*x[i].T)*p
        d.append(e[0,0])

    return d
def loadDataSet():
    with open('/Users/Chok-John/Desktop/logisticTest.txt') as f:
        data = f.readlines()
        x = []
        y = []
        for i in data:
            x.append([float(j) for j in i.strip().split(",")[0:2]])
            y.append(int(i.strip().split(",")[-1]))

    return x,y

#q,e = loadDataSet()

w = classfiy(x,y,0.1)
print(w)
a = []
b = []
aL = []
bL = []
for i in range(len(x)):
    if y[i] == 1:
        a.append(x[i])
        aL.append(y[i])
    else:
        b.append(x[i])
        bL.append(y[i])



print(min(d(a,aL,w))+min(d(b,bL,w)))
def return1():
    pass





X0 = []
Y0 = []
X1 = []

Y1 = []

for i in range(len(x)):
    if y[i] == 1:
        X0.append(x[i][0])
        Y0.append(x[i][1])
    else:
        X1.append(x[i][0])
        Y1.append(x[i][1])




g = [i for i in range(7)]


z = [-w[0,0]/w[0,1] * x - w[0,2]/w[0,1] for x in g]

plt.plot(g,z)
plt.scatter(X0, Y0, label="线性回归$",s=50, color="red", marker=".")
plt.scatter(X1, Y1, label="线性回归$",s=50, color="g", marker=".")

plt.show()
