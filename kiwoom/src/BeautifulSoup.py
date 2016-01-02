# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import requests

class bts:

# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=Q")
# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=P") #코스피

    def IframeUrl(self):

        code='069110'   #코스온
#         code='021080'  #에이티넘
        self.total=0
        self.end=True
        self.page=1
        while self.end:
            
            iframe_src='http://finance.daum.net/item/quote_hhmm_sub.daum?page='+str(self.page)+'&code='+str(code)
            self.iframeParse(iframe_src)
            self.page+=1
        print("총 갯수 :"+str(self.total))
        print("총 페이지 :"+str(self.page))
        
    def iframeParse(self,IframeAddress):
        self.iframe_content=BeautifulSoup(requests.get(IframeAddress).text,"lxml")
#         self.printTimeResult()
#         self.printPercentResult()
        self.mergeTimeAndPercent()

    def printTimeResult(self):
        eachTime = self.iframe_content.findAll("td",class_="datetime2")
#         eachPercent = self.iframe_content.findAll("td",class_="num cUp")
        
        print(eachTime)
        
        for a in eachTime:
            print("time : %s"%a.contents[0])
            if a.contents[0]=='09:00':          #실전에서 수정필요
                self.end=False
                break
            self.total+=1
            
    def mergeTimeAndPercent(self):
        eachTime = self.iframe_content.findAll("td",class_="datetime2")
#         eachPercent = self.iframe_content.findAll("td",class_="num cUp")
#         eachPercent = eachTime.next_sibling().next_sibling().next_sibling()
        
        self.dictt={}
        for i in range(0,eachTime.__len__()):
            print('eachTime : '+str(eachTime[i].contents[0]))
            print('eachPercent : '+str(eachTime[i].next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.contents[0]))
            if eachTime[i].contents[0]=='09:00':          #실전에서 수정필요
                self.end=False
                break
#             self.dictt[eachTime[i]]=eachPercent[i]
            self.total+=1
#         print('#######'+str(self.dictt))
            
#     def printPercentResult(self):
#         eachPercent = self.iframe_content.findAll("td",class_="num cUp")
#         for a in range(self.total):
#             print("eachPercent : %s"%a.contents[0])
#             self.total+=1
                

if __name__ == "__main__":
    bttest = bts()
    
    bttest.IframeUrl()
    