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

        self.td = self.iframe_content.find_all("td")
        for a in self.td:
            print(a)
            
        
        self.total = 0
        self.dictions={}
        
        
        
        
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
    
