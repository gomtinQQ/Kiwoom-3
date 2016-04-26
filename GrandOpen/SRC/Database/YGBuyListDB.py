# -*- coding: utf-8 -*-
import sqlite3
import sys,os
from _sqlite3 import OperationalError
sys.path.append('../')
sys.path.append('../DB')
import time,datetime
import pandas as pd
from SRC.Database import DBSet


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
        
        
#     def updateRelativeCode(self,Code,relative,pastMinute):
    def updateRelativeCode(self,Code,relative,timeVal):
#         tim = datetime.datetime.now()
#         hour = str(tim.hour)
#         minute = str(pastMinute)
#         foTime = hour+minute
        foTime = str(timeVal[0])
        
        info = str(relative)
        
        if info.startswith("-"):
            info=info[1:]
        
        query = 'update '+self.BuyListRelativeTable+' set "'+foTime+ '" = '+str(info)+' where StockCode = '+str(Code)
#         print(query)
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except OperationalError:
            self.tracebackLog()
            print("relative [",relative,"]")
        
    def updateVolumeCode(self,Code,Rotate,timeVal):
        
        foTime = str(timeVal[0])
        info = str(timeVal[1])
        
        if info.startswith("-"):
            info=info[1:]
        
        query = 'update '+self.BuyListVolumeRotateTable+' set "'+foTime+ '" = '+str(info)+' where StockCode = '+str(Code)
#         print(query)
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except OperationalError:
            self.tracebackLog()
            print("info [",info,"]")
    
    def updateBuy(self,code,cursor,conn):
        
        code = str(code)

        '''사기전 현재 보유상태 체크'''        
        selQuery = 'select BUYSELL from '+self.BuyListTable+' where StockCode = '+code
        
        cursor.execute(selQuery)
        buySell = cursor.fetchall()

#         print(str(buySell[0][0]))
        if str(buySell[0][0]) == "N":
            '''미보유 일때만 구매'''
            query = 'update '+self.BuyListTable+' set "BUYSELL"="B" where StockCode = '+code
        
            cursor.execute(query)
            conn.commit()
#             print(code,' buy !')
        else :
#             print('사기전 보유수량이 있음 (',code,')')
            pass
    
    def buyStock(self,code,time,CurrPrice):
        '''update BuyList set '900'=0 where StockCode = 19210'''
        price=CurrPrice
        query = 'update '+self.BuyListTable+' set "'+ str(time) +'" ='+str(price)+', "BUYSELL"="Y"  where StockCode = '+str(code)
        self.cursor.execute(query)
        self.conn.commit()
        
    def updateSell(self,code,cursor,conn):
        code = str(code)
        
        '''팔기전 현재 보유상태 체크'''
        selQuery = 'select BUYSELL from '+self.BuyListTable+' where StockCode = '+code
        
        cursor.execute(selQuery)
        buySell = cursor.fetchall()
        
        if str(buySell[0][0]) == "Y" or str(buySell[0][0]) == "B":
            
            query = 'update '+self.BuyListTable+' set "BUYSELL"="S" where StockCode = '+code
            cursor.execute(query)
            conn.commit()
        
    def sellStock(self,code,time,CurrPrice):
        price=CurrPrice
        query = 'update '+self.BuyListTable+' set "'+ str(time) +'" ='+str(price)+', "BUYSELL"="N"  where StockCode = '+str(code)
        self.cursor.execute(query)
        self.conn.commit()
        
    def getEndCode(self):
        query = 'select StockCode from '+self.BuyListTable+' where "BUYSELL"="Y"'
        self.cursor.execute(query)
        dd = self.cursor.fetchall()
        yy=[]
        for index in range(len(dd)):
            code=dd[index][0]
            yy.append(code)
        return pd.DataFrame(yy,columns=['Code'])
    
    def getBuySell(self):
#         query = 'select BUYSELL from '+self.BuyListTable+' where StockCode = "'+code+'"'
        query = 'select StockCode,BUYSELL from '+self.BuyListTable
        
        self.cursor.execute(query)
        dd = self.cursor.fetchall()
        
        arw=[]
        for i in range(len(dd)):
            if dd[i][1] =="B":
                arw.append(dd[i])
            elif dd[i][1] =="S":
                arw.append(dd[i])
        return arw
    
    def insertGold(self,code,name):
        
        try:
#             sql = 'insert into '+self.BuyListTable+' (StockCode) values("'+str(code)+'");'
            
            sql = self.insertGoldQuery.format(tableName=self.BuyListTable,StockCode=str(code),StockName=str(name))
            self.cursor.execute(sql)
            
            sql = self.insertGoldQuery.format(tableName=self.BuyListVolumeRotateTable,StockCode=str(code),StockName=str(name))
#             sql = 'insert into '+self.BuyListVolumeRotateTable+' (StockCode) values("'+str(code)+'");'
            self.cursor.execute(sql)
            sql = self.insertGoldQuery.format(tableName=self.BuyListRelativeTable,StockCode=str(code),StockName=str(name))
#             sql = 'insert into '+self.BuyListRelativeTable+' (StockCode) values("'+str(code)+'");'
            self.cursor.execute(sql)
            
            self.conn.commit()
            
        except Exception:
            
            self.tracebackLog()
    
    
if __name__ == '__main__':
    cp =YGGetDbData()
    cp.insertGold('000222')
#     DB = '../../Sqlite3/BuyList'+str(datetime.datetime.today().date())+'.db'
    DB = cp.BuyListDBToday
    table = cp.BuyListTable
    print(DB,table)
    cp.setProperties(DB,table)
    
    yy = cp.getCodeNameForReaReg()
#     print(yy['BuySell'])
#     cp.buyStock(98120, 903,236200)
#     cp.updateVolumeCode(227950, 3820,932)
#     cp.sellStock(19210, 930,12000)
#     print(cp.getEndCode())
#     print(yy['Code'][0])
    dd = cp.getBuySell()
    for i in range(len(dd)):
        print(str(dd[i][1]))