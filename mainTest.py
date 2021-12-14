import main as m

# 缩减规则测试
# 要更改main文件中的Glist
# C = [3, 4, 5, 6]
# R = [0, 1, 2, 7, 8, 9]
# R = m.reduce1(C, R, 7, 2)
# R = m.reduce2(C, R, 7, 2)
# C = m.reduce3(C, R, 7, 2)
# print(C)

# 度的上界技术测试（测试用图和分支技术是一个图）
# 基于度的上界 Ud
# C = [2, 3, 5, 6, 7]
# R = [0, 1, 4, 8, 9, 10]
# print("Ud=",m.degreeUperBound(C, R, 8))
# # 基于邻域重构的上界 Unr
# C = [2, 3, 5, 6, 7]
# R = [0, 1, 4, 8, 9, 10]
# print("Ud=",m.degreeNeighborReconstruct(C, R, 8))
# # 基于度的分类的上界
# C = [2, 3, 5, 6, 7]
# R = [0, 1, 4, 8, 9, 10]
# print("Ud=",m.degreeClassfication(C, R, 8))

# 分支技术测试用例

# C = [2, 3, 5, 6, 7]
# R = [0, 1, 4, 8, 9, 10]
# # C = [3, 4, 5, 6]
# # R = [0, 1, 2, 7, 8, 9]
# v=max(m.ConnectScore(C,R),key=m.ConnectScore(C,R).get)
# print(v,'的支配节点为：',m.dominationNodes(C,R,v))

from xml.dom.minidom import parse
domTree=parse(r"E:\test.xml")
type(domTree)
content=domTree.documentElement
print(content.toxml())
print("结束")







