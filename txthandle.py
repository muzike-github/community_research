# 解析peer-to-peer.txt文档中的图
import matplotlib.pyplot as plt
import networkx as nx


def graphGenerate():
    f = open('peer-to-peer.txt')
    line = f.readline()
    Glist = []
    t = 0
    while line:
        line = line.strip('\n')
        node = line.split('\t')
        print(node)
        nodeturple = tuple(node)
        Glist.append(nodeturple)
        line = f.readline()
        t = t + 1
        if t > 2000:
            break
    f.close()
    print(Glist)
    G = nx.Graph()
    G.add_edges_from(Glist)
    return G

G=graphGenerate()
# nx.draw(G, with_labels=True)
# plt.show()
