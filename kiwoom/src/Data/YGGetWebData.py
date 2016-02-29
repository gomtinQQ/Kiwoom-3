# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import btsForDaily
import datetime
import pandas as pd


def getForeignerAndCompanyPureBuy(code,day=""):
    '''외국인,기관 데이타 가져옴.'''
    '''day 는 최대 30일치까지밖에못가져옴. 추후수정예정'''
    
    date_fmt='%Y-%m-%d'
    Data = btsForDaily.daily().getForeignerBuyDaum(code,day)
    yy = []
    for index in Data:
        DateTime= Data[index][0]
        Foreign = Data[index][1]
        Company = Data[index][2]
        
        PdArr = DateTime,Foreign,Company
        yy.append(PdArr)
    
    dd = pd.DataFrame(yy,columns=['DateTime','Foreign','Company'])
    dd = dd.iloc[::-1]
    
    return dd


def getStockPriceData(code,date,TIMEOUT="",DATE_FMT=""):
    '''date 이후부터 값을가져옴'''
    '''TIMEOUT default = 5, DATE_FORMAT default = %Y-%m-%d'''
    '''return Date,open,high,low,close,volume,DataIndex'''
    TimeOut=5
    if TimeOut !="":
        Timeout=TIMEOUT
        
    Data = btsForDaily.daily().getDataFromDaum(str(code),str(date),TimeOut)
    date_fmt = '%Y-%m-%d'
    if DATE_FMT !="":
        date_fmt=DATE_FMT
    
    yy = []
    for index in Data:
        raw_x = datetime.datetime.strptime(str(Data[index][0]),date_fmt)
        Date=raw_x
        open=Data[index][1]
        high=Data[index][2]
        low=Data[index][3]
        close=Data[index][4]
        volume=Data[index][5]
        DateIndex = [Data[index][0]]
        
        PdArr =Date,open,high,low,close,volume,DateIndex
        yy.append(PdArr)
        
    dd = pd.DataFrame(yy,columns=['Date','open','high','low','close','volume','DateIndex'])
    dd = dd.iloc[::-1]  #reverse data frame
    
    return dd
def getStockPriceAndFCInfo(code,date):
    '''FC Pure Buy volume is default 5'''
    
if __name__ == '__main__':
    
    print(getForeignerAndCompanyPureBuy('126700'))
    print(getStockPriceData('126700', '2014-09-1'))