import networkx as nx
import heapq
import matplotlib.pyplot as plt
import dataHandle as dh
import txthandle as th
import fileHandle as fh


# 用于画图的函数
def paint(GList, H):
    # 添加加权边
    G = nx.Graph()
    G.add_weighted_edges_from(GList)
    if len(H) != 0:
        G = G.subgraph(H)
    # 生成节点位置序列（）
    pos = nx.circular_layout(G)
    # 重新获取权重序列
    weights = nx.get_edge_attributes(G, "weight")
    # 画节点图
    nx.draw_networkx(G, pos, with_labels=True)
    # 画权重图
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    plt.title("BRB")
    plt.show()


# 求图G的最小权重（）
def minWeight(G):
    weights = []
    for i in G:
        weight = 0
        for j in nx.neighbors(G, i):  # 遍历节点的所有邻居
            weight += G.get_edge_data(i, j)['weight']
        weights.append(weight)
    return min(weights)


# 求图G的最大权重（）
def maxWeight(G):
    weights = []
    for i in G:
        weight = 0
        for j in nx.neighbors(G, i):  # 遍历节点的所有邻居
            weight += G.get_edge_data(i, j)['weight']
        weights.append(weight)
    return max(weights)


# 根据度数和权重将其归1并计算分数
def getScore(degree, weight):
    degreeScore = degree / degreeMax
    weightScore = weight / weightMax
    return degreeScore + weightScore


# 求图G的最小度
def minDegree(G):
    degrees = []
    for i in G:
        degrees.append(G.degree(i))
    return min(degrees)


# 求图G的最大度数
def maxDegree(G):
    degrees = []
    for i in G:
        degrees.append(G.degree(i))
    return max(degrees)


# 求出给定社区的凝聚力分数
def cohesiveScore(H):
    degree = MinDegree(nx.subgraph(G, H))
    weight = minWeight(nx.subgraph(G, H))
    score = getScore(degree, weight)
    score = round(score, 4)  # 保留两位小数
    return score


# 自我网络（ego-network）提取算法
def Getego(G, q):
    egoGraph = nx.ego_graph(G, q, 1)  # 得到节点q在图G中的自我网络图
    # print(egoGraph.nodes)
    return egoGraph.nodes  # 返回自我网络的所有节点


# 得到图的最小度
def MinDegree(G):
    temp = []
    for i in G:
        temp.append(G.degree[i])
    return min(temp)


# 得到图的最大度
def MaxDegree(G):
    temp = []
    for i in G:
        temp.append(G.degree[i])
    return max(temp)


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


# 缩减规则，对实例（C，R）进行缩减
# 先把与C中每个节点都不相连的顶点从R中删除
def reduce0(C, R):
    # print("调用reduce0")
    for v in C:
        for u in R:
            if not G.has_edge(u, v):
                R.remove(u)
    return R


# 缩减规则1
def reduce1(C, R, h, k1):
    # print("调用缩减规则1")
    for v in R:
        CAndR = list(set(C).union(set(R)))  # C∪R
        CAndv = list(set(C).union([v]))  # C∪{v}
        CAndRGraph = nx.subgraph(G, CAndR)
        CAndvGraph = nx.subgraph(G, CAndv)
        Cgraph = nx.subgraph(G, C)
        lengthC = len(Cgraph.nodes)
        if min(CAndRGraph.degree(v), CAndvGraph.degree(v) + h - lengthC - 1) <= k1:
            # print("根据reduce1移除节点", v)
            R.remove(v)
    # print("调用缩减规则1结束")
    return R


# 缩减规则2中的n公式
def rule2Lemma(K, D):
    if 1 <= D <= 2 or K == 1:
        n = K + D
    else:
        n = K + D + 1 + ((int)(D / 3)) * (K - 2)
    return n


def reduce2(C, R, h, k1):
    # print("调用缩减规则2")
    CAndR = list(set(C).union(set(R)))
    CAndRGraph = nx.subgraph(G, CAndR)
    # nx.draw(CAndRGraph,with_labels=True)
    # plt.show()
    K = MinDegree(CAndRGraph)  # C∪R子图的最小度
    # D = nx.diameter(CAndRGraph)  # C∪R子图的直径
    for v in R:
        for u in C:
            # 这里需要判断删减后的图是否还连通
            # 如果不连通直接删除v
            if not nx.has_path(CAndRGraph, u, v):
                R.remove(v)
                break
            else:
                # 根据两点之间的最短线路来求两点之间的距离
                dist = len(nx.shortest_path(CAndRGraph, u, v)) - 1
                # print(u,":",v,"之间的距离为",dist)
                if rule2Lemma(k1 + 1, dist) > h:
                    R.remove(v)
                    # print("根据reduce2移除节点", v)
                    break
    # print("调用缩减规则2结束")
    return R


# 缩减规则3
def reduce3(C, R, h, k1):
    # print("调用缩减规则3")
    CAndR = list(set(C).union(set(R)))  # C∪R
    CAndRGraph = nx.subgraph(G, CAndR)
    for u in C:
        if CAndRGraph.degree(u) == (k1 + 1):
            for i in nx.neighbors(CAndRGraph, u):
                # 找到邻居后判断该节点是否已经在C中
                if i not in C:
                    # print("根据reduce3将节点", i, "移入C中")
                    C.append(i)
    # print("调用缩减规则3结束")
    return C


# 缩减规则测试 用例
# C = [3, 4, 5, 6]
# R = [0, 1, 2, 7, 8, 9]
# R = reduce1(C, R, 7, 2)
# R = reduce2(C, R, 7, 2)
# C = reduce3(C, R, 7, 2)
# print(C)


# 基于度的上界技术
def degreeUperBound(C, R, h):
    # print("调用度的上界技术")
    degreeList = []
    CAndR = list(set(C).union(set(R)))
    CAndRGraph = nx.subgraph(G, CAndR)
    CGraph = nx.subgraph(G, C)
    for u in C:
        degreeList.append(min(CAndRGraph.degree(u), CGraph.degree(u) + h - len(CGraph.nodes)))
    Ud = min(degreeList)
    # print("调用度的上界技术结束")
    return Ud


# 基于邻域重构的上界技术
def degreeNeighborReconstruct(C, R, h):
    # print("调用邻域重构技术")
    CGraph = nx.subgraph(G, C)
    verticeNum = h - len(CGraph.nodes)
    # Rex = []  # R'
    # Cex = []  # C'
    degreeDicvInCAndv = {}  # 记录v在{v}∪C中的度
    # 从R中选取h-|C|个在图C∪{v}中度数最大的点(R')记为Rex
    # 得到v(v∈R)在C∪{v}中的度，保存在字典里
    for v in R:
        CAndv = list(set(C).union([v]))
        CAndvGraph = nx.subgraph(G, CAndv)
        degreeDicvInCAndv[v] = CAndvGraph.degree(v)
    degreeDicvInCAndv2 = degreeDicvInCAndv.copy()  # 深拷贝，用作下面的循环
    # 取h-|C|个具有最大度数的点
    RexDic = dict(heapq.nlargest(verticeNum, degreeDicvInCAndv.items(), key=lambda x: x[1]))
    # print(RexDic)  # 得到R'
    # 记录u(u∈C)在C中的度
    degreeDicu = {}
    for u in C:
        degreeDicu[u] = CGraph.degree(u)  # 将u在C中的度用字典保存
    # 对R'中的每个v,选取x个节点（x是v在{v}∪C中的度数）
    for v in RexDic:
        # 选最小的几个节点
        CexDic = dict(heapq.nsmallest(degreeDicvInCAndv2[v], degreeDicu.items(), key=lambda x: x[1]))
        # print(v, ":度数加一的节点", CexDic)
        for key, values in CexDic.items():
            degreeDicu[key] += 1
        # print(v, ":加完后", degreeDicu)
    node = min(degreeDicu, key=degreeDicu.get)
    Unr = degreeDicu[node]
    # print("调用邻域重构技术结束")
    return Unr


# 基于度的分类的上界技术
def degreeClassfication(C, R, h):
    # print("调用度的分类技术")
    Udc = float("inf")
    UnrMost = []
    degreeu = {}  # u(u∈CMost)在C中的度
    CGraph = nx.subgraph(G, C)
    degreeMax = MaxDegree(CGraph)
    degreeMin = MinDegree(CGraph)
    for t in range(degreeMin, degreeMax + 1):
        # print("第", t, "轮")
        CMost = {}  # C中度数小于t的节点
        # 选取C中度小于t的节点保存为CMost
        for u in C:
            if CGraph.degree(u) <= t:
                CMost[u] = CGraph.degree(u)
        # 计算每个节点v在{v}∪CMost中的度数
        degreevInvAndCMost = {}
        for v in R:
            vAndCMost = list(set(CMost).union({v}))
            vAndCMostGraph = nx.subgraph(G, vAndCMost)
            degreevInvAndCMost[v] = vAndCMostGraph.degree(v)  # 得到所有节点的度
        # 取h-|C|个节点，利用headpq函数得到R'
        verticeNum = h - len(CGraph.nodes)
        RexDic = dict(heapq.nlargest(verticeNum, degreevInvAndCMost.items(), key=lambda x: x[1]))
        for u in CMost:
            degreeu[u] = CGraph.degree(u)
        for v in RexDic:
            # 求得前n个度最小的,若不加k，默认是根据字典的key值来进行选取
            # 利用headpq函数得到C'
            CexDic = dict(heapq.nsmallest(degreevInvAndCMost[v], degreeu.items(), key=lambda x: x[1]))
            for key, values in CexDic.items():
                degreeu[key] += 1
        UnrMost.append(degreeu[min(degreeu, key=degreeu.get)])
        # print(UnrMost)
        Unr = min(UnrMost)
        # 此时degreeu中各个节点的值已经改变，需要清空字典，下一次循环再生成
        degreeu.clear()
        Udc = min(Unr, Udc)
        # if Udc<=t+1:
        #     break
    # print("调用度的分类技术结束")
    return Udc


# 求连接分数最高的节点v*所支配的所有节点集合
# vx是候选集R中连接分数最高的节点(v*)
def dominationNodes(C, R, vx):
    CAndR = list(set(C).union(set(R)))
    CAndRGraph = nx.subgraph(G, CAndR)
    dominationList = []  # 存放所有被v*支配的节点
    # 求v*的所有邻居
    vxNeighbors = list(nx.neighbors(CAndRGraph, vx))
    vxNeighbors.append(vx)
    # print("v*的邻居为", vxNeighbors)
    templist = []
    for v in R:
        vNeighbors = list(nx.neighbors(CAndRGraph, v))
        # print(v, '的邻居为', vNeighbors)
        for x in vNeighbors:
            if x not in vxNeighbors:
                templist.append(x)
        if len(templist) == 0:
            dominationList.append(v)
        templist.clear()  # 记得把templist清空，不然这一轮的邻居节点会累计到下一个结点
    if vx in dominationList:
        dominationList.remove(vx)  # 将自身移除
    return dominationList


# SC-heu(G,q,l,h)替代贪婪F算法得到一个可行社区H
def ScHeu(G, q, l, h):
    print("查询节点", q, "的度为：", G.degree(q))
    H = []  # 初始为空
    k1 = 0  # 下界
    S = []
    if G.degree[q] >= (h - 1):
        S = Getego(G, q)  # 将q的自我网络节点集赋值给S
        S = list(S)
        Sgraph = nx.subgraph(G, S)
        while len(S) >= l:  # 此处论文中是>=
            # 更新社区
            if len(S) <= h and MinDegree(Sgraph) > k1:
                k1 = MinDegree(Sgraph)
                H.clear()
                H = S[:]
                print("更新，H=", H)
            # 移除S中具有最小度的顶点 此处S是一个列表
            # 先找到S中最小度的顶点，存入nodelist
            nodeList = []
            for i in S:
                if Sgraph.degree[i] == MinDegree(Sgraph):
                    nodeList.append(i)
            # print("待移除的节点：", nodeList)
            # nx.draw(Sgraph,with_labels=True)
            # plt.show()
            # 遍历nodelist，在S中将其移除
            for i in nodeList:
                S.remove(i)
            Sgraph = nx.subgraph(G, S)  # 将S图更新以便下一次循环

    else:
        S.append(q)
        while len(S) < h:
            # 找出G\S中连接分数最大的节点V*
            GexcludeS = list(set(G).difference(set(S)))  # 求G与S的差集
            soreDict = ConnectScore(S, GexcludeS)
            # print(soreDict)
            scoreMaxNode = max(soreDict, key=soreDict.get)
            S.append(scoreMaxNode)  # S=S∪{V*}
            sGraph = nx.subgraph(G, S)
            if len(S) >= l and MinDegree(sGraph) > k1:
                k1 = MinDegree(sGraph)
                H = S
    if len(H) == 0:
        H.append(q)
    print("基线算法结束,得到的可行社区为:", H)
    print("初始可行解的顶点数为：", len(H))
    print("初始可行解的最小度为：", MinDegree(nx.subgraph(G, H)))
    nx.draw(nx.subgraph(G, H), with_labels=True)
    plt.show()
    return H


# BRB算法
def BRB(C, R, k1, l, h, H):
    # print(k1)
    # 先用缩减规则对C和R进行处理
    # print("删除前C",C)
    R = reduce1(C, R, h, k1)
    R = reduce2(C, R, h, k1)
    C = reduce3(C, R, h, k1)
    CGraph = nx.subgraph(G, C)
    # 求上界
    UB = min(degreeUperBound(C, R, h), degreeNeighborReconstruct(C, R, h), degreeClassfication(C, R, h))
    # print("删除后", C)
    if l <= len(C) <= h and MinDegree(CGraph) > k1:
        # print("mindegree",MinDegree(CGraph))
        # 如果找到了更优的C，则更新最优社区H和最小度
        k1 = MinDegree(CGraph)
        # print(k1)
        H.clear()
        H = C[:]
        # nx.draw(nx.subgraph(G,H),with_labels=True)
        # plt.show()
        print("更新：H=", H, "最小度为:", k1)
    # print("k1",k1)
    if len(C) < h and len(R) != 0 and UB > k1:
        scoreDict = ConnectScore(C, R)
        vx = max(scoreDict, key=scoreDict.get)  # 得到连接分数最大的节点 v*
        dominationList = dominationNodes(C, R, vx)  # 得到被v*支配的所有节点
        dominationNodesScoreDict = {}  # 将被支配节点的连接分数存储，以便后续排序
        for i in dominationList:
            dominationNodesScoreDict[i] = scoreDict[i]
        # 对字典根据value值(连接分数)排序
        tempDict = sorted(dominationNodesScoreDict.items(), key=lambda x: x[1], reverse=True)
        # 排序后得到的是一个复合列表，我们只需要节点就可
        dominationNodesScoreListSorted = []
        for i in tempDict:
            dominationNodesScoreListSorted.append(i[0])
        # 利用分支原理生成i个分支
        for i in dominationNodesScoreListSorted:
            H, k1 = BRB(list(set(C).union({vx, i})), list(set(R).difference({vx, i})), k1, l, h, H)
        H, k1 = BRB(list(set(C).union({vx})), list(set(R).difference({vx}, dominationNodesScoreListSorted)), k1, l, h,
                    H)
        H, k1 = BRB(C, list(set(R).difference({vx}, dominationNodesScoreListSorted)), k1, l, h, H)
    return H, k1


# 主算法
def ScEnum(G, q, l, h):
    H = ScHeu(G, q, l, h)  # 调用ScHeu算法计算一个可行社区H
    Hgraph = nx.subgraph(G, H)
    k1 = MinDegree(Hgraph)  # 计算最优最小度的下界
    coreNumberDict = nx.core_number(G)  # 得到G中每个节点的核数
    coreNumberMin = coreNumberDict[min(coreNumberDict, key=coreNumberDict.get)]  # min函数得到的是核数最大的值对应的节点
    k2 = min(coreNumberDict[q], h - 1)  # 上界
    print("k1:", k1, "k2:", k2)
    # 开始递归
    R = list(G.nodes)
    R.remove(q)
    # 将初始可行社区H作为递归参数，
    if k1 < k2:
        H, kx = BRB([q], R, k1, l, h, H)  # 初始最优社区就是SCheu算出的可行社区H
    return H


GList = fh.csvResolve('dataset/bitcoinData.csv')  # 得到测试用图
G = nx.Graph()
G.add_weighted_edges_from(GList)
G.remove_edges_from(nx.selfloop_edges(G))
weightMax = maxWeight(G)
degreeMax = maxDegree(G)
print("母图的最大度数", degreeMax)
print("母图的最大权重", weightMax)
# 图，查询节点，社区大小上界，社区大小下界
H = ScEnum(G, 1, 7, 8)
print("最终社区的最小度为",minDegree(nx.subgraph(G,H)))
print("最终社区的最小权重为",minWeight(nx.subgraph(G,H)))
paint(GList,H)
print("搜索结果：", H, "凝聚分数", cohesiveScore(H))
