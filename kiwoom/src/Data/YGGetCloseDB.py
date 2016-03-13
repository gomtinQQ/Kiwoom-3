# -*- coding: utf-8 -*-
import sqlite3
import sys,os
from _sqlite3 import OperationalError
from sqlalchemy.orm.relationships import foreign
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
            
    def getPrice(self,db,table,code):
        
        sql = 'select * from '+table+' where StockCode = "'+str(code)+'";'

        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            cursor.execute(sql)
            dd = cursor.fetchall()
            
            pArr =[]
            
#             print(len(dd[0]))
            for index in range(2,len(dd[0])):
                price = dd[0][index]
                pArr.append(price)
                
            return pd.DataFrame(pArr,columns=['Close'])
            
        except OperationalError:
            self.PrintException()
            
    def getColumns(self,db,table):
        sql = 'select sql from sqlite_master where name="'+table+'"'
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            
            cursor.execute(sql)
            dd = cursor.fetchall()
            str = dd[0][0]
            YMDDate =[]
            while(str.find(']')!=-1):
                YMDDate.append(str[str.find('[')+1:str.find(']')])
                str = str[str.find(']')+1:]
                
            return pd.DataFrame(YMDDate,columns=['Date'])
                
        except OperationalError:
            self.PrintException()
        
    def getClosePriceFromDB(self,code):
#         self.initConfigSet()
        CloseData = self.getPrice(self.ClosePriceDB,self.ClosePriceTable,code)
        date_fmt = '%Y-%m-%d'
        Date = self.getColumns(self.ClosePriceDB,self.ClosePriceTable)
        
        if len(CloseData) != len(Date):
            raise "CloseData And Date is not match"
        
        yArr = []
        for index in range(len(CloseData)):
            close = CloseData['Close'][index]
            date = datetime.datetime.strptime(Date['Date'][index],date_fmt) 
            DateIndex = Date['Date'][index]
            
            pData = close,date,DateIndex
            yArr.append(pData)
        dd = pd.DataFrame(yArr,columns=['Close','Date','DateIndex'])
        dd = dd.sort_values(by='DateIndex')
        dd = dd.iloc[::-1] #리버스시킴
        dd = dd.reset_index(drop=True)
        
#         dd = dd.sort_values(by="DateIndex")
#         dd = dd.iloc[::-1]
        
        Arc = self.getVolumeAndForeignAndCompany(code)
#         Arc = Arc.iloc[::-1]
        
        dd['Volume'] = Arc['Volume']
        dd['Foreign'] = Arc['Foreign']
        dd['Company']= Arc['Company']
        
        dd = dd.sort_values(by="DateIndex")
        return dd
    
    def getVolumeAndForeignAndCompany(self,code):
        Volumesql = "select * from "+self.VolumeTable+" where StockCode = "+code
        Companysql = "select * from "+self.CompanyTable+" where StockCode = "+code
        Foreignsql = "select * from "+self.ForeignerTable+" where StockCode = "+code
        
        
        dbName = self.ForeignerDB
        
        
#         print(self.ForeignerTable,self.ForeignerDB)
        Date = self.getColumns(self.ForeignerDB,self.ForeignerTable)
        
        
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        cursor.execute(Volumesql)
        Volume = cursor.fetchall()
        
        cursor.execute(Companysql)
        Company = cursor.fetchall()
        
        cursor.execute(Foreignsql)
        Foreign = cursor.fetchall()
        
#         print(len(Volume[0]),len(Company[0]),len(Foreign[0]),len(Date['Date']))
        if len(Volume[0]) != len(Company[0]) != len(Foreign[0]) is not len(Date):
            raise print("Volume and Company length Error")
        yArr = []
        for i in range(2,len(Volume[0])):
            
            vo = Volume[0][i]
            fo = Foreign[0][i]
            co = Company[0][i]
            date = Date['Date'][i-2]
            pdArr = vo,fo,co,date
            yArr.append(pdArr)
        dd = pd.DataFrame(yArr,columns=['Volume','Foreign','Company','DateIndex'])
#         dd = dd.iloc[::-1]
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
    bld.initConfigSet()
#     print(bld.getVolumeAndForeignAndCompany('126700'))
    print(bld.getClosePriceFromDB('126700'))
#     dd = bld.getPrice('126700')
#     print(dd['Close'])
#     dd = bld.getColumns()
#     print(dd['Date'])
#     dd = bld.getClosePriceFromDB('126700')
#     print(dd)
#     041140
#     bld.togleCode('127710')
#     dd = bld.getCodeNameCoast()
#     print(dd['Code'])