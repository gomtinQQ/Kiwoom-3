# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import requests
import time
import ExcelMake
import code

class btsForRealNaver:
    
    def getCurPrice(self,code):
        
        code = self.addZeroToStockCode(code)
        frame_src = 'http://finance.naver.com/item/main.nhn?code='+str(code)
        self.iframe_content = BeautifulSoup(requests.get(frame_src).text,"lxml",)
        
        cur_today = self.iframe_content.find("div",class_="today")
#         print(BeautifulSoup.original_encoding)
        cur_price=''
        if len(cur_today.span.contents[0])is not None:
            cur_price = cur_today.find("span",class_="blind").contents[0] 
#         cur_price = cur_today.span.contents[0]
        return cur_price
    
    def getName(self,code):
        code = self.addZeroToStockCode(code)
        frame_src = 'http://finance.naver.com/item/main.nhn?code='+str(code)
        self.iframe_content = BeautifulSoup(requests.get(frame_src).text,"lxml")
        
        name = self.iframe_content.find("div",class_="wrap_company")
#         name = name.find("a",href_="#")
        print(name.h2.a.contents[0])
        
            
    def addZeroToStockCode(self,str):
        str=str.strip()
    
        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
                
        return str        
        
        
        
if __name__=="__main__":
    
    bts = btsForRealNaver()
    print(bts.getCurPrice('021080'))
    bts.getName('021080')