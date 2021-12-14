import xml.sax
from xml.sax.handler import ContentHandler
from xml.sax import parse

doc = open('out.txt', 'w',encoding='UTF-8')


class article(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.author = ""
        self.title = ""
        self.pages = ""
        self.journal = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "article" or tag == "inproceedings" or tag=="phdthesis":
            mdate = attributes["mdate"]
            key = attributes["key"]
            print("-----------这是一条分割线--------------", file=doc)

    # 元素结束事件处理
    def endElement(self, tag):
        if self.CurrentData == "author":
            print("author:", self.author, file=doc)
        # elif self.CurrentData == "title":
        #     print("title:", self.title, file=doc)
        # elif self.CurrentData == "journal":
        #     print("journal:", self.journal, file=doc)

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "author":
            self.author = content
        elif self.CurrentData == "title":
            self.title = content
        elif self.CurrentData == "journal":
            self.journal = content


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(article())
    parser.parse(r'E:\dblp.xml')

doc.close()
