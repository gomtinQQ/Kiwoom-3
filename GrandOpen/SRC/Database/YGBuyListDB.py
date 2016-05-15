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
    
    def __init__(self):
        super(YGGetDbData,self).__init__()
    
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
        
        if info.startswith("-") or info.startswith("+") :
            info=info[1:]
        if len(info)<=0:
            info='-1'
        
        query = 'update '+self.BuyListRelativeTable+' set "'+foTime+ '" = '+info+' where StockCode = '+str(Code)
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except OperationalError:
            print(query)
            self.debug(query)
            self.tracebackLog()
#             print("relative [",relative,"]")
            
            
    def updateRelativeCode2(self,Code,relative,timeVal):
#         tim = datetime.datetime.now()
#         hour = str(tim.hour)
#         minute = str(pastMinute)
#         foTime = hour+minute
        foTime = str(timeVal[0])
        
        info = str(relative)
        
        if info.startswith("-"):
            info=info[1:]
        
        query = "update {tableName} set '{StockCode}' = '{info}' where StockTime = '{foTime}'".format(tableName=self.BuyListRelativeTable,StockCode =Code,info=info,foTime=foTime)
#         print(query)
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except OperationalError:
            self.tracebackLog()
            print("relative [",relative,"]")
        
    def updateVolumeCode(self,Code,timeVal):
        
        foTime = str(timeVal[0])
        info = str(timeVal[1])
        Code = str(Code)
#         if info.startswith("-") or info.startswith("+"):
#             info=info[1:]
        if len(info) is 0:
            info='0'
        if len(Code) >6:
            Code=Code[1:]
        
        query = 'update '+self.BuyListVolumeRotateTable+' set "'+foTime+ '" = '+info+' where StockCode = '+Code
#         print(query)
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except OperationalError:
            self.debug(query)
            self.tracebackLog()
#             print("info [",info,"]")
    def updateVolumeCode2(self,Code,timeVal):
        
        '''변경된소스'''
        
        foTime = str(timeVal[0])
        info = str(timeVal[1])
        
        if info.startswith("-"):
            info=info[1:]
        '''update BuyList set "130960" = "130" where StockTime = "900"'''
        query = "update {tableName} set '{StockCode}' = '{info}' where StockTime = '{foTime}'"\
        .format(tableName=self.BuyListVolumeRotateTable,StockCode =Code,info=info,foTime=foTime)
        print(query)
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
            print(query)
#             print('사기전 보유수량이 있음 (',code,')')
            self.tracebackLog()
    
    def buyStock(self,code,time,CurrPrice):
        '''update BuyList set '900'=0 where StockCode = 19210'''
        price=CurrPrice
        if len(str(price))==0:
            price='-1'
        try:
            if len(code)>6:
                code = code[1:]
                print(code)
#             query = 'update '+self.BuyListTable+' set "'+ str(time) +'" ='+str(price)+', "BUYSELL"="Y"  where StockCode = '+str(code)
#             query = 'update '+self.BuyListTable+' set "BSTime" = "'+str(time)+'" where StockCode = '+str(code)
            query = 'update {tableName} set "{time}" ={price} , "BUYSELL"="Y", "BSTime" = "{time2}" where StockCode = {Code}'\
            .format(tableName=self.BuyListTable,time=str(time),price=price,time2=str(time),Code=str(code))
            self.cursor.execute(query)
            #update BuyList set "BSTime" = 914 where StockCode = "222810"
#             self.cursor.execute(query)
            self.conn.commit()
        except :
#             print(query)
            
            self.tracebackLog(query)
        
    def updateSell(self,code,cursor,conn):
        code = str(code)
        
        '''팔기전 현재 보유상태 체크'''
        selQuery = 'select BUYSELL from '+self.BuyListTable+' where StockCode = '+code
        
        try:
            cursor.execute(selQuery)
            buySell = cursor.fetchall()
            query = 'update '+self.BuyListTable+' set "BUYSELL"="S" where StockCode = '+code
        
#             if str(buySell[0][0]) == "Y" or str(buySell[0][0]) == "B":
            if len(buySell) !=0:
                cursor.execute(query)
                conn.commit()
        except :
#             print(query)
            self.debug(query)
            self.tracebackLog(query)
        
    def sellStock(self,code,time,CurrPrice):
        price=CurrPrice
        code=str(code)
        if len(str(price))==0:
            price='-1'
        try:
            if len(code)>6:
                code = code[1:]
            query = 'update '+self.BuyListTable+' set "'+ str(time) +'" ='+str(price)+', "BUYSELL"="N"  where StockCode = '+code
            self.cursor.execute(query)
            self.conn.commit()
        except : 
#             print(query)
            self.debug(query)
            self.tracebackLog(query)
        
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
            
    def insertGold2(self,code,name):
        
        try:
            '''BuyList에만 넣기위한 쿼리.'''
#             sql = 'insert into '+self.BuyListTable+' (StockCode) values("'+str(code)+'");'
            
            sql = self.insertGoldQuery.format(tableName=self.BuyListTable,StockCode=str(code),StockName=str(name))
            self.cursor.execute(sql)
            
#             sql = self.insertGoldQuery.format(tableName=self.BuyListVolumeRotateTable,StockCode=str(code),StockName=str(name))
# #             sql = 'insert into '+self.BuyListVolumeRotateTable+' (StockCode) values("'+str(code)+'");'
#             self.cursor.execute(sql)
#             sql = self.insertGoldQuery.format(tableName=self.BuyListRelativeTable,StockCode=str(code),StockName=str(name))
#             sql = 'insert into '+self.BuyListRelativeTable+' (StockCode) values("'+str(code)+'");'
#             self.cursor.execute(sql)
            
            self.conn.commit()
            
        except Exception:
            
            self.tracebackLog()
    
    
if __name__ == '__main__':
    cp =YGGetDbData()
#     cp.insertGold('000222')
#     DB = '../../Sqlite3/BuyList'+str(datetime.datetime.today().date())+'.db'
    DB = cp.BuyListDBToday
    table = cp.BuyListTable
    cp.setProperties(DB,table)
    print(DB,",",table)
    
    timeVal = {}
    sJongmokCode = "130960"
    timeVal[sJongmokCode] = "900","287002"
    
    cp.updateVolumeCode2(sJongmokCode, timeVal[sJongmokCode])
    cp.updateRelativeCode2(sJongmokCode,"1360",timeVal[sJongmokCode])
    
    
#     yy = cp.getCodeNameForReaReg()
#     print(yy['BuySell'])
#     cp.buyStock(98120, 903,236200)
#     cp.updateVolumeCode(227950, 3820,932)
#     cp.sellStock(19210, 930,12000)
#     print(cp.getEndCode())
#     print(yy['Code'][0])
#     dd = cp.getBuySell()
#     for i in range(len(dd)):
#         print(str(dd[i][1]))