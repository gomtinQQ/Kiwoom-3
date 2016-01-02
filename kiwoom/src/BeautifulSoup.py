# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import requests

class bts:
# 가져올 URL
# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=Q")
# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=P") #코스피

    def IframeUrl(self):
#         html = requests.get("http://finance.daum.net/item/hhmm.daum?code=069110")
#         html = requests.get(urladdress)
#         bt = BeautifulSoup(html.text,"lxml")
#         forchild = bt.find('iframe')
#         iframe_src=forchild.attrs['src']
#         iframe_src='http://finance.daum.net'+iframe_src
        code='069110'   #하이비젼
#         code='021080'  #에이티넘
        self.total=0
        self.end=True
        self.page=1
        while self.end:
            
            iframe_src='http://finance.daum.net/item/quote_hhmm_sub.daum?page='+str(self.page)+'&code='+str(code)
            print('you requested src is : %s'%iframe_src)
            self.iframeParse(iframe_src)
            self.page+=1
        print("총 갯수 :"+str(self.total))
        print("총 페이지 :"+str(self.page))
        
    def iframeParse(self,IframeAddress):
        self.iframe_content=BeautifulSoup(requests.get(IframeAddress).text,"lxml")
        self.printTimeResult()
        self.printPercentResult()

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
#     def printPercentResult(self):
#         eachPercent = self.iframe_content.findAll("td",class_="num cUp")
#         for a in range(self.total):
#             print("eachPercent : %s"%a.contents[0])
#             self.total+=1
                




if __name__ == "__main__":
    bttest = bts()
    stockcode='069110'
    bttest.IframeUrl()
    