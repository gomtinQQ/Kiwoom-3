# -*- coding: utf-8 -*-
import sqlite3
import sys,os
sys.path.append('../')
sys.path.append('../DB')
import MakeDB
import time,datetime
import pandas as pd


class YGGetDbData(MakeDB.DBMake):
    
    def getCodeNameForReaReg(self):
        '''초기 실시간데이터받기용 쿼리'''
        query = 'select StockCode,BUYSELL from '+self.tableName
        self.cursor.execute(query)
        dd = self.cursor.fetchall()
        yy=[]
        for index in range(len(dd)) :
            code = dd[index][0]
            buysell=dd[index][1]
            arry = code,buysell
            yy.append(arry)
        return pd.DataFrame(yy,columns=['Code','BuySell'])
    
    def setProperties(self,dbName='../../Sqlite3/BuyList.db',table='BuyList'):
#         print(dbName)
        super().setProperties(dbName,table)
    
    def buyStock(self,code,time,price):
        '''update BuyList set '900'=0 where StockCode = 19210'''
        
        query = 'update '+self.tableName+' set "'+ str(time) +'" ='+str(price)+', "BUYSELL"="Y"  where StockCode = '+str(code)
        self.cursor.execute(query)
        self.conn.commit()
        
    def sellStock(self,code,time,price):
        query = 'update '+self.tableName+' set "'+ str(time) +'" ='+str(price)+', "BUYSELL"="N"  where StockCode = '+str(code)
        self.cursor.execute(query)
        self.conn.commit()
        
    def getEndCode(self):
        query = 'select StockCode from '+self.tableName+' where "BUYSELL"="Y"'
        self.cursor.execute(query)
        dd = self.cursor.fetchall()
        yy=[]
        for index in range(len(dd)):
            code=dd[index][0]
            yy.append(code)
        return pd.DataFrame(yy,columns=['Code'])
    
    def getBuySell(self,code):
        query = 'select BUYSELL from '+self.tableName+' where StockCode = "'+code+'"'
        
        self.cursor.execute(query)
        dd = self.cursor.fetchall()
        return dd[0][0]
    
if __name__ == '__main__':
    cp =YGGetDbData()
    DB = '../../Sqlite3/BuyList'+str(datetime.datetime.today().date())+'.db'
    cp.setProperties(DB,'BuyList')
    yy = cp.getCodeNameForReaReg()
#     print(yy['BuySell'])
    cp.buyStock(98120, 903,236200)
#     cp.sellStock(19210, 930,12000)
#     print(cp.getEndCode())
#     print(yy['Code'][0])
#     print(cp.getBuySell('019210'))