# -*- coding: utf-8 -*-
import sqlite3
import sys,os
sys.path.append('../')
sys.path.append('../DB')
import DBSet
import time,datetime
import pandas as pd


class YGGetDbData(DBSet.DBSet):
    
    def getCodeNameForReaReg(self):
        '''초기 실시간데이터받기용 쿼리'''
        query = 'select StockCode,BUYSELL from '+self.BuyListTable
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
        super().setProperties(dbName,table)
        
        
    def updateRelativeCode(self,Code,relative,pastMinute):
        tim = datetime.datetime.now()
        hour = str(tim.hour)
        minute = str(pastMinute)
        foTime = hour+minute
        
        info = str(relative)
        query = 'update '+self.BuyListRelativeTable+' set "'+foTime+ '" = '+str(info)+' where StockCode = '+str(Code)
        
        self.cursor.execute(query)
        self.conn.commit()
        
    def updateVolumeCode(self,Code,Rotate,foTime):
        
        info = str(Rotate)
        foTime = str(foTime)
        
        query = 'update '+self.BuyListVolumeRotateTable+' set "'+foTime+ '" = '+str(info)+' where StockCode = '+str(Code)
        
        self.cursor.execute(query)
        self.conn.commit()
    
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
    
    def insertGold(self,code):
        
        try:
            sql = 'insert into '+self.BuyListTable+' (StockCode) values("'+str(code)+'");'
            self.cursor.execute(sql)
            sql = 'insert into '+self.BuyListVolumeRotateTable+' (StockCode) values("'+str(code)+'");'
            self.cursor.execute(sql)
            sql = 'insert into '+self.BuyListRelativeTable+' (StockCode) values("'+str(code)+'");'
            self.cursor.execute(sql)
            
            self.conn.commit()
            
        except OperationalError:
            
            print(traceback.print_exc())
    
    
if __name__ == '__main__':
    cp =YGGetDbData()
#     DB = '../../Sqlite3/BuyList'+str(datetime.datetime.today().date())+'.db'
    DB = cp.BuyListDBToday
    table = cp.BuyListTable
    print(DB,table)
    cp.setProperties(DB,table)
    
    yy = cp.getCodeNameForReaReg()
#     print(yy['BuySell'])
#     cp.buyStock(98120, 903,236200)
    cp.updateVolumeCode(227950, 3820,932)
#     cp.sellStock(19210, 930,12000)
#     print(cp.getEndCode())
#     print(yy['Code'][0])
#     print(cp.getBuySell('019210'))