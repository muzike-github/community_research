#
# import networkx as nx
# from lxml import etree
# import xml.etree.cElementTree as ET
# tree=etree.iterparse(r'E:\dblp2015.xml')
# for t in tree:
#     for e in t[1]:
#         print(e.text)
# print("结束")
import xml.sax
from xml.sax.handler import ContentHandler
from xml.sax import parse

doc = open('author.txt', 'w', encoding='UTF-8')
nodeList=[]
i=0
class article(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.author = ""
        self.title = ""
        self.pages = ""
        self.journal = ""
        self.year = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "article" or tag == "inproceedings" or tag=="phdthesis" or tag=="www" or tag=="incollection":
            mdate = attributes["mdate"]
            key = attributes["key"]
            #print(len(nodeList))
            if len(nodeList)!=0:
                print(nodeList,file=doc)
            #print("-----------这是一条分割线--------------",file=doc)
            #print(nodeList)
            # print("-----------这是一条分割线--------------", file=doc)
            nodeList.clear()


    # 元素结束事件处理
    def endElement(self, tag):
        if self.CurrentData == "author":
            nodeList.append(self.author)
        # elif self.CurrentData=="year":
            # print("author:", self.author, file=doc)
        # elif self.CurrentData == "title":
        #     print("title:", self.title, file=doc)
        # elif self.CurrentData == "pages":
        #     print("pages:", self.pages, file=doc)
        # elif self.CurrentData == "year":
        #     print("year:", self.year, file=doc)
        #global i
        #i=i+1
        #print("第",i,"轮")
        #print(nodeList)

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "author":
            self.author = content
        elif self.CurrentData == "title":
            self.title = content
        elif self.CurrentData == "pages":
            self.pages = content
        elif self.CurrentData == "year":
            self.year = content


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(article())
    parser.parse(r'E:\dblp.xml')
    #print(len(nodeList))


doc.close()
