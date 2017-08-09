from numpy import *
import math
import copy
import matplotlib.pyplot as plt
def loadDataSet():
    with open('data','r') as f:
        data = []
        for i in f.readlines():
            line = i.strip().split(' ')
            data.append(line)
    data = array(data,dtype= float64)

    return data


def RandomPoint(dataMatIn, k):
    xMAX = max(dataMatIn[:, 0])
    xMin = min(dataMatIn[:, 0])
    yMax = max(dataMatIn[:, 1])
    yMin = min(dataMatIn[:, 1])
    randomPoint = []
    check = set()
    i = 0
    while (i < k):
        randomX = random.uniform(xMin, xMAX)
        randomY = random.uniform(yMin, yMax)
        check.add((randomX, randomY))
        if len(check) != i + 1:
            continue
        randomPoint.append([randomX, randomY])
        i = i + 1

    return randomPoint


def calDistance(dataMatIn, randomPoint):
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
    randomPoint = RandomPoint(dataMatIn, k)

    while (1):
        p = copy.deepcopy(randomPoint)
        label = []
        for i in range(k):
            label.append([])

        distance = []
        for i in randomPoint:
            distance.append(calDistance(dataMatIn, i))
        distance = array(distance)
        index = []
        for i in range(len(dataMatIn)):
            index.append(argmin(distance[:, i]))

        value = []
        for i in range(len(index)):
            label[index[i]].append(dataMatIn[i])
        label = array(label)


        for i in range(k):
            if label[i] == []:
                continue
            for j in range(len(randomPoint[0])):
                randomPoint[i][j] = mean(array([x[j] for x in label[i]]))
        if p == randomPoint:
            break
        else:
            p = randomPoint

    return label,randomPoint


# ------------------------------------------------------------#


def draw(label,Mu,Sigma,length):
    x1 = random.normal(Mu[0][0], Sigma[0][0][0, 0]*float(length -1 )/length, 100)
    x2 = random.normal(Mu[1][0], Sigma[1][0][0, 0]*float(length -1 )/length, 100)
    y1 = random.normal(Mu[0][1], Sigma[0][1][0, 1]*float(length -1 )/length, 100)
    y2 = random.normal(Mu[1][1], Sigma[1][1][0, 1]*float(length -1 )/length, 100)
    label[0] = array(label[0])
    label[1] = array(label[1])
    print('X_1 \t',Mu[0][0],Sigma[0][0][0, 0]*float(length -1 )/length)
    print('Y_1\t',Mu[0][1], Sigma[0][1][0, 1]*float(length -1 )/length, 100)
    print('X_2\t',(Mu[1][0], Sigma[1][0][0, 0]*float(length -1 )/length, 100 ))
    print('Y_2\t', Mu[1][1], Sigma[1][1][0, 1]*float(length -1 )/length, 100)
    print('-----------------------------------------')
    plt.scatter(label[0][:,0],label[0][:,1],c = 'r')
    plt.scatter(label[1][:, 0], label[1][:, 1],c = 'b')
    plt.scatter(x1, y1,c='orange')
    plt.scatter(x2, y2,c= 'g')

    plt.show()





def run(k,d,epsilon,iterateTimes):
    data = loadDataSet()
    label,Mu = K_means(data,k) # 获得初始的均值
    label[0] = array(label[0])
    label[1] = array(label[1])
    length = len(data)

    # plt.scatter(label[0][:,0],label[0][:,1],c = 'pink')
    # plt.scatter(label[1][:, 0], label[1][:, 1],c = 'b')
    # plt.show()
    Sigma = [] # 初始化协方差矩阵,类型为ndarray
    Mu = array(RandomPoint(data,k))

    for i in range(len(label)):
        # Sigma.append(mat(cov(mat(label[i]).transpose())))
        Sigma.append(identity(k))
    alphas = [] # 初始化alpha
    for i in range(k):
        # alphas.append(float(len(label[i]))/length)
        alphas.append(1.0/k)
    print(Sigma)
    Gamma = zeros((len(data),d))




    for i in range(iterateTimes):
        Mu_old = copy.deepcopy(Mu)
        alphas_old = copy.deepcopy(alphas)
        Sigma_old = copy.deepcopy(Sigma)
        Gamma = E_Step(data, k, Mu, alphas, Gamma, Sigma)
        Mu,alphas,Sigma = M_Step(data,k,Mu,alphas,Gamma,Sigma)

        Mu_old = array(Mu_old)
        draw(label,Mu,Sigma,length)
        Mu = array(Mu)
        print(judge(data,k,Mu,Sigma,alphas) - judge(data,k,Mu_old,Sigma_old,alphas_old))
        if abs(judge(data,k,Mu,Sigma,alphas) - judge(data,k,Mu_old,Sigma_old,alphas_old)) < epsilon:
            break
    return Mu,Sigma


def E_Step(data,k,Mu,alpha,Gamma,Sigma):


    for j in range(len(data)):
        down = 0
        for i in range(k):

            p = 1.0/( (2*math.pi*linalg.det(Sigma[i]) )**(k/2)) * exp(- 1.0/2 *mat(data[j] - Mu[i]) * mat(Sigma[i]).I *mat(data[j] - Mu[i]).T)
            down += alpha[i] * p[0,0]
        for i in range(k):
            p = 1.0/( (2*math.pi*linalg.det(Sigma[i]) )**(k/2)) * exp(- 1.0/2 *mat(data[j] - Mu[i]) * mat(Sigma[i]).I *mat(data[j] - Mu[i]).T)
            up = alpha[i] * p[0,0]
            # print(type(up/down),j,i)
            #print(up/down,j,i)

            Gamma[j][i] = float(up)/down

    Gamma[isnan(Gamma)] = 0.0
    return Gamma

def M_Step(data,k,Mu,alphas,Gamma,Sigma):
    Gamma_sum = sum(Gamma,axis=0)

    length = len(data)
    for i in range(k):
        up = 0
        for j in range(length):
            up += Gamma[j][i] *mat((data[j] - Mu[i])).T*mat((data[j] - Mu[i]))
        Sigma[i] = up / Gamma_sum



    for i in range(k):
        up = 0
        for j in range(length):
            up += Gamma[j][i] * data[j]
        Mu[i] = up/Gamma_sum[i]

    for i in range(k):
        alphas[i] = Gamma_sum[i]/ len(data)


    return Mu,alphas,Sigma # Mu

def judge(data,k,Mu,Sigma,alphas):
    for i in range(k):
        p = []
        result = 0
        for j in range(len(data)):
            N = 1.0 / ((2 * math.pi * linalg.det(Sigma[i])) ** (k / 2)) * exp(
                - 1.0 / 2 * mat(data[j] - Mu[i]) * mat(Sigma[i]).I * mat(data[j] - Mu[i]).T)
            result += alphas[i]*N[0,0]
        p.append(result)

    p = array(p)

    return cumprod(p[0])[0]

Mu,Sigma = run(2,2,0.1,450)


#
# x1 = random.normal(0.5,1,100)
# x2 = random.normal(3.0 , 0.5,100)
# y1 = random.normal(0.5, 1, 100)
# y2 = random.normal(3.0, 0.5, 100)
# data1 = column_stack((x1,y1))
# data2 = column_stack((x2,y2))
# data = row_stack((data1,data2))
# savetxt('data',data)

