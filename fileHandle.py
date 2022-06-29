# 解析emailWeight文档中的图
import networkx as nx
import csv


def graphGenerate(filename):
    f = open(filename)
    line = f.readline()
    Glist = []
    t = 0
    while line:
        line = line.strip('\n')
        node = line.split(' ')
        nodeturple = tuple(node)
        Glist.append(nodeturple)
        line = f.readline()
        t = t + 1
        if t > 1000:
            break
    f.close()
    return Glist


# 解析CSV文件
def csvResolve(filename):
    Glist = []
    t = 0
    with open(filename) as f:
        render = csv.reader(f)
        header_row = next(render)  # 取表头
        for row in render:
            t = t + 1
            if t > 1000:
                break
            node1 = int(row[0])
            node2 = int(row[1])
            weight = int(row[2])
            Glist.append((node1, node2, weight + 10))
    # print(Glist)
    return Glist
