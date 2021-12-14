# 解析dblp数据集
import re
import networkx as nx
import matplotlib.pyplot as plt


def graphGenerate():
    G = nx.Graph()
    Glist = []
    tempList = []
    f = open('author.txt')
    line = f.readline()
    # line="1,2,3,4,5"
    t = 0
    while line:
        # print(line)
        line = line.strip('\n')
        newline = line.replace('[', '').replace(']', '').replace("'", '').replace(" ",'')
        t = t + 1
        # if t<100000:
        #     continue
        if t > 400000:
            break
        # print(newline)
        authorList = newline.split(',')
        # print(authorList)
        # 得到作者列表后开始构建边
        length = len(authorList)
        if length == 1:
            G.add_node(authorList[0])
        else:
            for i in range(0, length):
                for j in range(i + 1, length):
                    tempList.append(authorList[i])
                    tempList.append(authorList[j])
                    tempTurple = tuple(tempList)
                    tempTurpleRe = tuple(reversed(tempTurple))
                    G.add_edge(*tempTurple)
                    # if Glist.count(tempTurple)+Glist.count(tempTurpleRe)>=5:
                    #     G.add_edge(*tempTurple)
                    # Glist.append(tuple(tempList))
                    tempList.clear()
                    # Glist.clear()
        authorList.clear()
        line = f.readline()

    f.close()

    return G
# G=graphGernerate()
# nx.draw(G, with_labels=True)
# plt.show()