# 使用贪心算法得到社区
import networkx as nx
import matplotlib.pyplot as plt
G=nx.Graph()
def greedy(C,R):
    for v in C:
        GraphC=nx.subgraph(G,C)
