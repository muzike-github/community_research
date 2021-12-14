# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:10:12 2017
@author: Administrator
"""
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import xml.sax
import sys
import io
import traceback
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
class MovieHandler( xml.sax.ContentHandler ):
   res=''
   def __init__(self):
      self.CurrentData = ""
      self.author = ""
      self.title = ""
      self.pages = ""
      self.year = ""
      self.volume = ""
      self.journal = ""
      self.number = ""
      self.url = ""
      self.ee = ""
   # 元素开始事件处理
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "article":
         print("self.__class__.res=",self.__class__.res)
         try:
           ww.write(self.__class__.res+'\n')#数据集中有不良数据，捕获一下
         except:
             traceback.print_exc()
         self.__class__.res=''
        # print ("*****article*****")
         mdate = attributes["mdate"]
         #print ("mdate:", mdate)
         key=attributes["key"]
         #print ("key:",key)
         self.__class__.res=self.__class__.res+mdate+';,;'+key+';,;'
         #print ('res_init:',self.__class__.res)

   # 元素结束事件处理
   def endElement(self, tag):
      if self.CurrentData == "author":
         #print ("author:", self.author)
         self.__class__.res=self.__class__.res+self.author+';,;'
      elif self.CurrentData == "title":
         #print ("title:", self.title)
         self.__class__.res=self.__class__.res+self.title+';,;'
      elif self.CurrentData == "pages":
         #print ("pages:", self.pages)
         self.__class__.res=self.__class__.res+self.pages+';,;'
      elif self.CurrentData == "year":
         #print ("year:", self.year)
         self.__class__.res=self.__class__.res+self.year+';,;'
      elif self.CurrentData == "volume":
         #print ("volume:", self.volume)
         self.__class__.res=self.__class__.res+self.volume+';,;'
      elif self.CurrentData == "journal":
         #print ("journal:", self.journal)
         self.__class__.res=self.__class__.res+self.journal+';,;'
      elif self.CurrentData == "number":
         #print ("number:", self.number)
         self.__class__.res=self.__class__.res+self.number+';,;'
      elif self.CurrentData == "url":
         #print ("url:", self.url)
         self.__class__.res=self.__class__.res+self.url+';,;'
      elif self.CurrentData == "ee":
         #print ("ee:", self.ee)
         self.__class__.res=self.__class__.res+self.ee+';,;'
      self.CurrentData = ""


   # 内容事件处理
   def characters(self, content):
      if self.CurrentData == "author":
         self.author = content+'####'
      elif self.CurrentData == "title":
         self.title = content
      elif self.CurrentData == "pages":
         self.pages = content
      elif self.CurrentData == "year":
         self.year = content
      elif self.CurrentData == "volume":
         self.volume = content
      elif self.CurrentData == "journal":
         self.journal = content
      elif self.CurrentData == "number":
         self.number = content
      elif self.CurrentData == "url":
         self.url = content
      elif self.CurrentData == "ee":
         self.ee = content
if ( __name__ == "__main__"):

   parser = xml.sax.make_parser()
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
   Handler = MovieHandler()
   parser.setContentHandler( Handler )
   ww=open('dblp_parse_result.txt','w+')
   parser.parse(r'E:\dblp2015.xml')
   ww.close()