import numpy as np
import math
import matplotlib.pyplot as plt

class Node(object):

    def __init__(self):
        self.data = None
        self.name = None
        self.left = None
        self.right = None
        self.LeftSon = None
        self.RightSon = None
        self.Father = None
        self.depth = None
        self.dim = None

    @property
    def getLeftChild(self):
        return  self.LeftSon.data

    @property
    def getRightChild(self):
        return  self.RightSon.data

    def has_leftChild(self):
        return self.LeftSon != None

    def has_rightChild(self):
        return self.RightSon != None

    def __traversal__(self):
        if not self.has_leftChild():

            return self.data

        left = self.LeftSon.__traversal__()
        if not self.has_rightChild():

            return [self.data,[left,None]]
        else:
            right = self.RightSon.__traversal__()

            return [self.data,[left,right]]


    def KNN_findClosest(self,node):

        if self.dim == None:
            return self

        if node[self.dim] > self.name[self.dim] and self.right != []:
            return self.RightSon.KNN_findClosest(node)
        elif node[self.dim] < self.name[self.dim] and self.left != []:
            return self.LeftSon.KNN_findClosest(node)
        else:
            return self.LeftSon


    @classmethod
    def distance(self,node1,node2):
        #输入两点坐标，求两点的距离，返回距离
        d = 0
        for i in range(len(node1)):
            detal = (node1[i] - node2[i])**2
            d += detal
        return math.sqrt(d)

    @classmethod
    def minDistance(self,data,node):
        #输入一组数据和一个点，求最小距离，并返回最小值和索引
        d = []
        for i in data:
            d.append(self.distance(i,node))
        return min(d),data[np.argmin(d)]

    def KNN_CheakCloest(self,node):
        curNode = self.Father
        minDistance,minPoint = self.minDistance(self.data,node)
        curMinDistacne,curMinPoint = self.minDistance(curNode.data,node)
        if minDistance > curMinDistacne:
            return False
        else:
            return True

    def KNN(self,node):

        pass
    def KNN_main(self,node):
        curNode = self.KNN_findClosest(node)
        closest = curNode
        closestDistance = []
        print(closest.name)
        while(curNode.Father != None):
            if not curNode.KNN_CheakCloest(node):
                #如果不是最近则移动到当前最近点
                curNode = curNode.Father
                closest = curNode

            curDistance,curPoint = self.minDistance(curNode.data,node)
            print(closest.name)
            if curNode.Father == None:
                return closest

            if curNode.Father == curNode.Father.LeftSon:
                osMinDistance ,osMinPoint = self.minDistance(curNode.Father.right,node)

            else:
                osMinDistance ,osMinPoint = self.minDistance(curNode.Father.left,node)

            if osMinDistance < curDistance:
                closest = curNode.Father.KNN_findClosest(osMinPoint)
            curNode = curNode.Father
        return closest












class KDTree(Node):
    def __init__(self,data):
        self.k = np.shape(np.array(data))[1]
        super(Node).__init__()
        self.depth = 0
        self.dim = self.depth % self.k
        self.Father  = None
        self.data,self.left,self.right = self.splitData(data,self.dim)
        self.name = self.data[0]


        self.LeftSon,self.RightSon = self.CreateTree(self.left,self.right,self.depth +1 ,self.dim,self)




    def splitData(self,ndarray,dim):
        length = len(ndarray)
        ndarray = np.array(ndarray)
        if length == 0:

            return None,None,None
        order = np.argsort(ndarray[:,dim])
        sortedArray = ndarray[order]
        nodeData = []
        mid = sortedArray[(length)//2]
        nodeData.append(mid)

        leftData = list(sortedArray[:(length)//2][::-1])
        rightData = list(sortedArray[(length)//2+1:])
        for i in range(len(leftData)):
            if leftData[i][dim] == mid[dim]:
                nodeData.append(leftData.pop(i))
            else:
                break

        leftData = leftData[::-1]

        for i in range(len(rightData)):
            if rightData[i][dim] == mid[dim]:
                nodeData.append(rightData.pop(i))
            else:
                break

        return nodeData,leftData,rightData

    def CreateTree(self,left,right,depth,dim,father):
        if len(left) == 1:
            rleaf = None
            if len(right) == 1:
                rleaf = Node()
                rleaf.depth = depth
                rleaf.Father = father
                rleaf.name = tuple(right[0])
                rleaf.data = right
                #rleaf.dim = depth % self.k

            lleaf = Node()
            lleaf.depth = depth
            lleaf.Father = father
            lleaf.name = tuple(left[0])
            lleaf.data = left
            #8lleaf.dim = depth % self.k
            return lleaf,rleaf
        if len(left) == 0 :
            return None,None

        leftSon = Node()
        leftSon.dim = depth % self.k
        leftSon.depth = depth

        leftSon.data , leftSon.left , leftSon.right = self.splitData(left,leftSon.dim)
        leftSon.name = leftSon.data[0]

        leftSon.Father = father
        leftSon.LeftSon , leftSon.RightSon = self.CreateTree(leftSon.left,leftSon.right,depth + 1,leftSon.dim ,leftSon)

        rightSon = Node()
        rightSon.dim = depth % self.k
        rightSon.depth = depth

        rightSon.data, rightSon.left, rightSon.right = self.splitData(right, rightSon.dim)
        rightSon.name = rightSon.data[0]
        rightSon.Father = father
        rightSon.LeftSon, rightSon.RightSon = self.CreateTree(rightSon.left, rightSon.right, depth + 1, rightSon.dim, rightSon)



        return leftSon,rightSon

test = [
    [7,2],#26
   [7,3],#17
    [5,4],#18
    [2,3],#54
    [4,7],#16
    [8,1],#36
    [9,2]#26
]

tree = KDTree(test)
testPoint = (8,7)
a = tree.KNN_main(testPoint)



x = []
y = []
for  i in test:
    x.append(i[0])
    y.append(i[1])

plt.scatter(x,y,color="red", marker=".")
plt.scatter(testPoint[0],testPoint[1],color="g", marker=".")
plt.scatter(a.name[0],a.name[1],color="g", marker=".")
plt .show()