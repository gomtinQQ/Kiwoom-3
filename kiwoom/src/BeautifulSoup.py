# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import requests


# 가져올 URL
# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=Q")
# html = requests.get("http://finance.daum.net/quote/all.daum?type=U&stype=P") #코스피
html = requests.get("http://finance.daum.net/item/hhmm.daum?code=069110")

bt = BeautifulSoup(html.text,"lxml")


forchild = bt.find_all('div',{'id':'reloadDelayDiv'})

i=0
print(forchild)


for childf in forchild :
    print(childf)
    i+=1
    
print("총 갯수"+str(i))


# iFrames=[] # qucik bs4 example
# iframexx = soup.find_all('iframe')
# for iframe in iframexx:
#     response = urllib2.urlopen(iframe.attrs['src'])
#     iframe_soup = BeautifulSoup(response)
