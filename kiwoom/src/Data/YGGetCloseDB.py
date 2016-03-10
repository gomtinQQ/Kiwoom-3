# -*- coding: utf-8 -*-
import sqlite3
import sys,os
from _sqlite3 import OperationalError
# sys.path.append('../')
sys.path.append('../DB')
import YGGetWebData
import time
import btsForDashin
import linecache
import MakeDB
import pandas as pd
import datetime

class YGGetCloseDB(MakeDB.DBMake):
    
    def setProperties(self,dbName="",tableName=""):
        DB= '../../Sqlite3/ClosePriceDB.db'
        if dbName !="":
            DbName=dbName
        self.Table='ClosePrice'
        if tableName !="":
            self.Table=tableName
            
        super().setProperties(DB,self.Table)
            
    def getPrice(self,code):
        
        sql = 'select * from '+self.tableName+' where StockCode = "'+str(code)+'";'

        try:
            self.cursor.execute(sql)
            dd = self.cursor.fetchall()
            
            pArr =[]
            
#             print(len(dd[0]))
            for index in range(2,len(dd[0])):
                price = dd[0][index]
                pArr.append(price)
                
            return pd.DataFrame(pArr,columns=['Close'])
            
        except OperationalError:
            self.PrintException()
            
    def getColumns(self):
        sql = 'select sql from sqlite_master where name="'+self.Table+'"'
        try:
            self.cursor.execute(sql)
            dd = self.cursor.fetchall()
            str = dd[0][0]
            YMDDate =[]
            while(str.find(']')!=-1):
                YMDDate.append(str[str.find('[')+1:str.find(']')])
                str = str[str.find(']')+1:]
            
#             for index in range(len(YMDDate)):
#                 print(YMDDate[index])
            return pd.DataFrame(YMDDate,columns=['Date'])
                
        except OperationalError:
            self.PrintException()
        
    def getClosePriceFromDB(self,code):
        CloseData = self.getPrice(code)
        date_fmt = '%Y-%m-%d'
        Date = self.getColumns()
        
        if len(CloseData) != len(Date):
            raise "CloseData And Date is not match"
        
        yArr = []
        for index in range(len(CloseData)):
            close = CloseData['Close'][index]
            date = datetime.datetime.strptime(Date['Date'][index],date_fmt) 
            DateIndex = Date['Date'][index]
            
            pData = close,date,DateIndex
            yArr.append(pData)
        dd = pd.DataFrame(yArr,columns=['close','Date','DateIndex'])
        dd = dd.iloc[::-1]
        return dd
    
    def getCodeNameCoast(self):
        sql = "select StockCode from "+self.tableName
        self.cursor.execute(sql)
        dd = self.cursor.fetchall()
        
        
        yy = []
        for index in range(len(dd)):
            yy.append(dd[index][0])
        return pd.DataFrame(yy,columns=['Code'])
            
        
        
if __name__ == '__main__':
    bld = YGGetCloseDB()
#     bld.createDatabase('../../Sqlite3/BuyList.db','BuyList')
    bld.setProperties()
#     dd = bld.getPrice('126700')
#     print(dd['Close'])
#     dd = bld.getColumns()
#     print(dd['Date'])
#     dd = bld.getClosePriceFromDB('126700')
#     print(dd)
#     041140
#     bld.togleCode('127710')
    dd = bld.getCodeNameCoast()
    print(dd['Code'])