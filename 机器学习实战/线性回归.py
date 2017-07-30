import numpy as np
import matplotlib.pyplot as plt

file_1 = open(r'/Users/Chok-John/Downloads/ex2Data/ex2x.dat','r')
file_2 = open(r'/Users/Chok-John/Downloads/ex2Data/ex2y.dat','r')
a = file_1.read().replace(" ","").split('\n')
b = file_2.read().replace(" ","").split('\n')
file_2.close()
file_1.close()
x = []
y = []
for i in range(len(a)-1):

     x.append(float(a[i]))
     y.append(float(b[i]))

x = np.array(x)
I = np.array([1 for x in range(50)])

y = np.array(y)
# X = x.reshape((-1,1))
# Y = y.reshape((-1,1))
one = np.mat(I).reshape((-1,1))

X =  np.column_stack((np.mat(x).reshape((-1,1)),one))
print(X)
Y = np.mat(y).reshape((-1,1))
XTX =X.T*X
ws = XTX.I*(X.T*Y)
print(ws)
q = np.linspace(0, 10, 10000)

e = [ws.A[0,0]*w + ws.A[1,0] for w in q]

plt.figure(figsize=(20,10))
plt.plot(q,e)

plt.scatter(x, y, label="线性回归$",s=50, color="red", marker=".")
plt.show()
