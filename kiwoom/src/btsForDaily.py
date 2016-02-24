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
            self.parse(page,code,self.start)
            page+=1
        
        return self.dailyData
    
    def getForeignerBuy(self,Code,Day=""):
        src = 'http://finance.daum.net//item/foreign_yyyymmdd.daum?page=1&code='+str(Code)
        content = requests.get(src).text
        bs4     = BeautifulSoup(content,'lxml')
        
        volume  =  bs4.find_all("td",class_="datetime2")
        
        DAY=3
        index = 0
        
        PureBuy={}
        
        if Day is not "":
            DAY=int(Day)
        
        for Pure in volume:
            
            date    =   str(Pure.contents[0])
            date    =   date.replace('.','-')
            date    =   '20'+date
            
            date    =   self.getDate(date)
            
            ForeignPurBuy = Pure.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
            CompanyBuy  = ForeignPurBuy.next_sibling.next_sibling
            
            ForeignPurBuy =ForeignPurBuy.contents[0]
            CompanyBuy  =CompanyBuy.contents[0]
            
            print(date,ForeignPurBuy,CompanyBuy)
            index +=1
            
            PureBuy[index]=ForeignPurBuy,CompanyBuy
            
            if index == DAY:
                break
        print(PureBuy)
        
        
    def getVolumn(self,Code,Date=""):
        src = 'http://finance.naver.com/item/sise_day.nhn?code='+str(Code)+'&page=1'
        
        content = requests.get(src).text
        bs4 = BeautifulSoup(content,'lxml')
#         price = bs4.find_all("span",class_="tah p11")
        price = bs4.find_all("td",class_="num")
        
        for i in price:
            
            close = i
            open = close.next_sibling.next_sibling
            print(close.contents[0].contents[0],open)
        
        
    
    def getDate(self,Date):
        '''String Format(2014-02-04) return datetime object'''
        
        dmt_Format='%Y-%m-%d'
        
        Date = str(Date)
        
        if not Date.startswith('20'):
            Date = '20'+Date
        
        return datetime.datetime.strptime(str(Date),dmt_Format)
        
        
        
 

if __name__=='__main__':
    
    dd = daily()
#     gd = dd.getDate('99-02-04')
#     print(gd)
#     dd.getForeignerBuy('126700','5')
    dd.getVolumn('126700')
#     data = dd.getDataFromDaum('021080','2010-2-12')
#     for dd in data:
#         date = data[dd][0]
#         price= data[dd][1]
#         index = dd
#         print(date,price,index)