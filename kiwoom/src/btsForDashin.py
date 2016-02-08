# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import requests
import time

import ExcelMake

class btsForReal:

    def  UrlParsing(self):

#         _start=time.time()
        frame_src = 'http://www.daishin.co.kr/ctx_kr/sc_stock/sg_stock_info/svc_kosdaq_total/KosdaqKsSise.shtml'
#         print(requests.get(frame_src).content)
        self.iframe_content=BeautifulSoup(requests.get(frame_src).content,"lxml")
#         print(self.iframe_content)
        
        print(self.iframe_content)
        self.td = self.iframe_content.find_all("td")
#         self.td = self.iframe_content.find_all("td",class_="B")
#         self.td = self.iframe_content.find_all("td",class_="R")
#         self.td = self.iframe_content.find_all("td",class_="N")
        
        
        self.codeNameCoast={}
        for a in self.td:
            if a.a is not None:
                if str(a.find("a").contents[0]).startswith('A') ==True:
                    self.inerNameCoast={}
                    coast =a.a.parent.next_sibling.next_sibling.contents[0]
                    change=a.a.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.contents[0]
                    changePercent=a.a.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.contents[0]
                    code = str(a.find("a").contents[0])[1:7]
                    name = str(a.find("a").contents[0])[8:]
                    
                    self.inerNameCoast[name]=coast
#                     print('['+name+'('+code+')] : '+str(coast)+'('+str(change)+') '+str(changePercent))
                    self.codeNameCoast[code]=self.inerNameCoast
                    del(self.inerNameCoast)
        self.total = 0
        self.dictions={}
        
#         self.getCodeNameCoast()
        
        
    def getCodeNameCoast(self):
        
        inde = 0
#         print(self.codeNameCoast)
        for a in self.codeNameCoast:
            for b in self.codeNameCoast[a]:
                inde+=1
                print(self.codeNameCoast[a])
                print(b)
                print(self.codeNameCoast[a][b])
                
        print(inde)
        
    def setCodeNameDic(self):
        
        for a in self.td :
            if a.find("a") !=None :
                if str(a.find("a").contents[0]).startswith('A') ==True:
                    self.total+=1
                    code = str(a.find("a").contents[0])[1:7]
                    name = str(a.find("a").contents[0])[8:]
                    self.dictions[code]=name
                    print(code+':'+name)
        
        print(len(self.dictions))
        
    def addZeroToStockCode(self,str):
        str=str.strip()

        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
        return str    
    
        
if __name__=="__main__":

    bfd = btsForReal()
    bfd.UrlParsing()
    
