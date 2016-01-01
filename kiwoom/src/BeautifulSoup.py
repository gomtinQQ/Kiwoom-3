# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import requests


# 가져올 URL
# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=Q")
# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=P") #코스피
html = requests.get("http://finance.daum.net/item/hhmm.daum?code=069110")

bt = BeautifulSoup(html.text,"lxml")

forchild = bt.find('iframe')

iframe_src=forchild.attrs['src']
iframe_src='http://finance.daum.net'+iframe_src
print(iframe_src)
iframe_content=BeautifulSoup(requests.get(iframe_src).text,"lxml")


# print(iframe_content)

# eachItem = iframe_content.findAll("tr",onmouseout="highlight(this,false)")

eachTime = iframe_content.find("td",class_="datetime2")
eachPercent = iframe_content.find("td",class_="num cUp")

print("time : "+str(eachTime))
print("percent : "+str(eachPercent))

i=0

# for a in eachTime:
#     print("time : "+str(eachTime[i]))
#     print("percent : "+str(eachPercent[i]))


# for a in eachItem:
#     btt = BeautifulSoup(a,"lxml")
#      
#     time=btt.find('td',class_="datetime2")
#     percent=btt.find('td',class_="num cUp")
#     print('time : '+str(time))
#     print('percent : '+str(percent))
#     print(btt)
#     i+=1
    
print("총 갯수"+str(i))

# datetime2.findAll("td",class_="datetime2")
# i=0
# for a in datetime2:
#     bt=BeautifulSoup(a.text,"lxml")
#  
#     print(bt.get_text('num cUp'))
#     i+=1


    
