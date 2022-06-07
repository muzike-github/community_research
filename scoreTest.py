import networkx as nx
import heapq
import matplotlib.pyplot as plt

# 缩减规则测试图
Glist = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 4), (2, 3), (2, 5), (2, 7), (3, 4), (4, 5), (4, 6), (4, 9),
         (5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8), (8, 9)]
G = nx.Graph() # 得到测试用图
G.add_edges_from(Glist)
nx.draw(G,with_labels=True)
plt.show()

# 计算节点的连接分数，返回连接分数最大的节点
# 此处不能对C进行remove操作，否则C会改变
def ConnectScore(C, R):
    Ccopy = C.copy()  # 用Ccopy 代替C的所有操作,否则求完连接分数后C会改变
    scoreDict = {}  # 字典保存R中每个节点的连接分数
    for v in R:
        graphC = nx.subgraph(G, Ccopy)  # 得到图C
        Ccopy.append(v)
        Gtemp = nx.subgraph(G, Ccopy)  # 得到节点集C∪{v}的在G中的子图
        Nblist = []  # 列表保存每个v的所有邻居
        score = 0
        # 此处判断v是否在C∪{v}中是否有邻居，没有邻居，分数为0
        if len(list(nx.neighbors(Gtemp, v))) != 0:
            # 有邻居但邻居在C中度为0，则设置score为0
            for i in nx.neighbors(Gtemp, v):  # 得到v(v∈R)在C∪{v}所有的邻居节点
                # print(Gtemp.nodes)
                # print("i在C中的度为", graphC.degree(i))
                if graphC.degree(i) != 0:
                    # print(graphC.degree(i))
                    score += 1 / graphC.degree(i);
                else:
                    score = 0
        # 如果v没有邻居，则直接分数为0
        else:
            score = 0
        # print(Nblist, score)
        scoreDict[v] = score  # 将对应节点的连接分数存储
        Ccopy.remove(v)
    # print(scoreDict)
    scoreMaxNode = max(scoreDict, key=scoreDict.get)
    # print("连接分数最大的节点",scoreMaxNode)
    return scoreDict

C=[3,4,5,6]
R=[0,1,2,7,8,9]
scoreDict=ConnectScore(C,R)
scoreMaxNode = max(scoreDict, key=scoreDict.get)
print(scoreDict)
print(scoreMaxNode)