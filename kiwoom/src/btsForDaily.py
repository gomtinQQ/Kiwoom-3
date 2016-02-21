# -*- coding: utf-8 -*-
import bts
import requests
from bs4 import BeautifulSoup
import datetime


class daily(bts.mbts):
    
    def __init__(self):
        pass
    
    def source(self,page="",code=""):
        

        self.url = 'http://finance.daum.net/item/quote_yyyymmdd_sub.daum?page='+str(page)+'&code='+str(code)+'&modify=1'   #한페이지에 30일치 나옴. 

        if page=="" or code=="":
            self.url = 'http://finance.daum.net/item/quote_yyyymmdd_sub.daum?page=1&code=035720&modify=1' 
            
        
    def parse(self,page,code,start,end=""):
        self.source(page,code)
        
        
        content = requests.get(self.url).text
        bs4     = BeautifulSoup(content,'lxml')
        price   = bs4.find_all("td",class_="datetime2")
        
        for daily in price:
            
            datePrice       =   daily
            datePrice       =   datePrice.contents[0]
            year_month_day  =   datePrice.split('.')
            datePrice       =   datePrice.replace('.','-')
            datePrice       =   '20'+datePrice
            
            self.dateTime       =   self.getDate(datePrice)
            if self.start > self.dateTime:
                self.Flag=False
                break
            
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
        
            end_price=str(end_price).replace(',','')
            
            self.dailyData[self.index]=str(datePrice),str(end_price)
            self.index+=1
                
    def getDataFromDaum(self,code,start,end=""):
        '''Format = 16-02-04'''
        '''end default = today'''
        self.dailyData = {}
        self.index = 1
        self.end=datetime.datetime.today()
        
        if end != "":
            self.end = self.getDate(end)
            
            
        end_year = self.end.year
        end_month = self.end.month
        end_day = self.end.day
        
        self.start=self.getDate(start)
        
        start_year = self.start.year
        start_Month = self.start.month
        start_Day = self.start.day
        
        
        page=1
        self.Flag = True
        while self.Flag:       
            self.parse(page,code,start)
            page+=1
        
        return self.dailyData
    
    
    def getDate(self,Date):
        '''String Format(2014-02-04) return datetime object'''
        
        Date=str(Date)
        Date_date = Date.split('-')
        Date_date_year =int(Date_date[0]) 
        if len(str(Date_date_year)) ==2:
            Date_date_year = int('20'+str(Date_date_year))
        Date_date_month = int(Date_date[1])
        Date_date_day = int(Date_date[2])
        
        return datetime.datetime(year=Date_date_year,month=Date_date_month,day =Date_date_day)
        
        
        
 

if __name__=='__main__':
    
    dd = daily()
    data = dd.getDataFromDaum('021080','2010-2-12')
    for dd in data:
        date = data[dd][0]
        price= data[dd][1]
        index = dd
        print(date,price,index)