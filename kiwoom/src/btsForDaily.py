# -*- coding: utf-8 -*-
import bts
import requests
from bs4 import BeautifulSoup
import datetime


class daily(bts.mbts):
    
    def source(self,page,code):
        self.url = 'http://finance.daum.net/item/quote_yyyymmdd_sub.daum?page=1&code=035720&modify=1'   #한페이지에 30일치 나옴. 
        
        
    def parse(self):
        self.source('1','323')
        
        self.dailyData = {}
        content = requests.get(self.url).text
        bs4     = BeautifulSoup(content,'lxml')
        price   = bs4.find_all("td",class_="datetime2")
        
        for daily in price:
            
            datePrice       =   daily
            datePrice       =   datePrice.contents[0]
            year_month_day  =   datePrice.split('.')
            year            =   year_month_day[0]
            month           =   year_month_day[1]
            day             =   year_month_day[2]
            
            start_price     =   daily.next_sibling.next_sibling
            high_price      =   start_price.next_sibling.next_sibling
            low_price       =   high_price.next_sibling.next_sibling
            end_price       =   low_price.next_sibling.next_sibling
            
            start_price     =   start_price.contents[0]
            high_price      =   high_price.contents[0]
            low_price       =   low_price.contents[0]
            end_price       =   end_price.contents[0]
            
            self.dailyData[str(year)+str(month)+str(day)]=end_price
#             print(year,month,day,start_price,high_price,low_price,end_price)
#         print(self.dailyData)
        return self.dailyData
        

if __name__=='__main__':
    
    dd = daily()
    dd.parse()