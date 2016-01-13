# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import requests
import time

class mbts:

# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=Q")
# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=P") #코스피

    def IframeUrl(self):
        '''
        this is  example
        '''
        code='069110'   #코스온
#         code='021080'  #에이티넘
        self.total=0
        self.end=True
        self.page=1
        self.eachPercent=[]
        self.timePerDic={}
        start_time=time.time()
        while self.end:
            
            iframe_src='http://finance.daum.net/item/quote_hhmm_sub.daum?page='+str(self.page)+'&code='+str(code)
            self.iframeParse(iframe_src)
            self.page+=1
            
        print("총 갯수 :"+str(self.total))
        print("총 페이지 :"+str(self.page))
        
        print("show PercentList : "+str(self.eachPercent))
        print("show PercentTotal "+str(self.eachPercent.__len__()))
        
        
    def IframeUrlWithCode(self,Code):

        print('코드 프레임 호출')
#         code='021080'  #에이티넘
        self.total=0
        self.end=True
        self.page=1
        self.eachPercent=[]
        self.timePerDic={}
        start_time=time.time()
        while self.end:
            
            iframe_src='http://finance.daum.net/item/quote_hhmm_sub.daum?page='+str(self.page)+'&code='+str(Code)
            self.iframeParse(iframe_src)
            self.page+=1
            
        end_time=time.time()
        print('1종목  파싱완료 ('+str(end_time-start_time)+')')


    def iframeParse(self,IframeAddress):
        self.iframe_content=BeautifulSoup(requests.get(IframeAddress).text,"lxml")
        eachTime = self.iframe_content.findAll("td",class_="datetime2")
        
        
        for i in range(0,eachTime.__len__()):
            
            self.eachPercent.append(eachTime[i].next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.contents[0])
            self.timePerDic[eachTime[i].contents[0]]=eachTime[i].next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.contents[0]
            
            if eachTime[i].contents[0]=='09:00':          #실전에서 수정필요
                self.end=False
                break
            self.total+=1

        
    def printTimeResult(self):
        eachTime = self.iframe_content.findAll("td",class_="datetime2")
        print(eachTime)
        
        for a in eachTime:
            print("time : %s"%a.contents[0])
            if a.contents[0]=='09:00':          #실전에서 수정필요
                self.end=False
                break
            self.total+=1
            
    def showEachPercent(self):
        for i in range(0,self.eachPercent.__len__()):
            print(self.eachPercent[i])
            
    def getEachPercent(self):
        return self.eachPercent
    
    def getTimePerDic(self):
#         print(self.timePerDic.__len__())
        return self.timePerDic

if __name__ == "__main__":
    bttest = mbts()
    
    bttest.IframeUrlWithCode('000660')
#     bttest.showEachPercent()
    
    bttp = bttest.getTimePerDic()
    
    for a in bttp:
        print(a)
#     print(bttp['09:05'])