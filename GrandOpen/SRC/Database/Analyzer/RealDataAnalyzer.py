# -*- coding: utf-8 -*-

import sqlite3
import sys,os
from _sqlite3 import OperationalError
# sys.path.append('../')
sys.path.append('../Data')
sys.path.append('../DB')

import time,datetime

import traceback
import multiprocessing as mp
from SRC.Database import DBSet
from SRC.Database import YGBuyListDB

class RealAnalyse(DBSet.DBSet):

    def getSelectQuery(self,tableName,buySell,Time="",count="",interval="",multiplicationCheck="1"):
        '''set SimulatorTime if not,get the current Time'''
        
        if count=="":
            count=5
        count=int(count)
        
        if interval=="":
            interval=1
        interval=int(interval)
        self.tocount = 1
        
        if Time=="":
            Time = int(self.getNowTime())       #1분전 시간을 구한다
            
        Time=int(Time)
        currTime = self.getNowTime()
        beforeTime = self.pastAgo(currTime,interval)
        
        op=">"
        if buySell =="B" or buySell =="BUY":
            op = "<"
        if multiplicationCheck is "1":
            self.whereQuery = 'select StockCode,StockName from '+tableName+' where "' + \
                str(beforeTime) +'"'+op+'"' + str(currTime) + '"'   
            
            self.getSelectQuery_proc(count, beforeTime ,interval,op)
            return self.whereQuery
        else:
            self.whereQuery = 'select StockCode,StockName from '+tableName+' where "' + \
                str(beforeTime) +'"*'+multiplicationCheck+''+op+'"' + str(currTime) +'"'
            return self.whereQuery
    
    def getSelectQuery_proc(self, count, Time,interval,op):
        '''
        get the update query set
        '''

        if self.tocount == count:
            self.tocount = 0
            return self.whereQuery

        else:
            currTime = Time
            beforeTime =self.pastAgo(currTime, interval)
 
            self.whereQuery = self.whereQuery + ' and "' + \
                str(beforeTime) +'"'+ op +'"' + str(currTime) + '"'

            self.tocount += 1
            self.getSelectQuery_proc(count, beforeTime,interval,op)
    
    def analyseVolume(self,YG):
        conn = sqlite3.connect(self.BuyListDBYesterday)
        cursor = conn.cursor()
        
        query = self.getSelectQuery(self.BuyListVolumeRotateTable,count=2,buySell="SELL")
        print(query)
        cursor.execute(query)
        dd = cursor.fetchall()

        for i in range(len(dd)):
            YG.updateBuy(dd[i][0])
        
    def analysePrice(self,YG):
        conn = sqlite3.connect(self.BuyListDBYesterday)
        cursor = conn.cursor()
        
        query = self.getSelectQuery(self.BuyListRelativeTable, count=2,buySell="SELL")
        
        cursor.execute(query)
        dd = cursor.fetchall()

        for i in range(len(dd)):
            YG.updateBuy(dd[i][0])
    
    def checkCodeSet(self,YG,connection,Cursor,tableName,BS,multiplicationCheck="1",count="",interval=""):
        try:            
            conn = connection
            cursor = Cursor

            if BS =="BUY":
                if count =="":
                    count=4
                if interval =="":
                    interval=1
                if multiplicationCheck is "1":
                    query = self.getSelectQuery(tableName, buySell=BS,count=count,interval=interval)
                    print(query)
                else:
                    query = self.getSelectQuery(tableName,buySell=BS,multiplicationCheck=multiplicationCheck,count=count,interval=interval)
                    print(query)
            
                cursor.execute(query)
                buyListCode= cursor.fetchall()
                for i in range(len(buyListCode)): 
                    YG.updateBuy(buyListCode[i][0],cursor,conn)
#                     print(buyListCode[i][0])
                    
            elif BS == "SELL":
                
                if count =="":
                    count=3
                if interval =="":
                    interval=1
                    
                query = self.getSelectQuery(tableName, buySell=BS,count=count,interval=interval)
            
                cursor.execute(query)
                buyListCode= cursor.fetchall()
#                 print(query)
                for i in range(len(buyListCode)):
                    YG.updateSell(buyListCode[i][0],cursor,conn)
#                     print(buyListCode[i][0])
            elif BS == "END":
                
                query = 'select StockCode from '+tableName+' where "BUYSELL"="Y" or "BUYSELL"="B"'
                cursor.execute(query)
                buyListCode = cursor.fetchall()
                
                print("영업종료하자")
                for i in range(len(buyListCode)):
                    YG.updateSell(buyListCode[i][0],cursor,conn)
                
                    
            else :
                print('Select correctly Buy or Sell ')
                
#             print(buyListCode,BS)
        except :
            self.tracebackLog()
    
    def getSelectQueryMulti(self,tableName,buySell):
        currTime = self.getNowTime()
        beforeTime = self.pastAgo(currTime, 1)
        
        qwefwefqwef
        query = 'select StockCode from '+tableName+' where "'+beforeTime+'"*2'
        
        return query
        
        
    def setDB(self,DB):
        self.DB= DB
    def setConfig(self,config):
        self.config=config
    
    def gogo(self,Test=""):
        
        YG = YGBuyListDB.YGGetDbData()
        YG.setProperties(self.DB,YG.BuyListRelativeTable)
        
        conn = sqlite3.connect(self.BuyListDBYesterday)
        cursor = conn.cursor()
        
        mode="Real"
        if Test is not None:
            mode=Test
        
        if mode =="Real":
            
            while(True):
                print("901분 부터 시작합니다.. [현재시각 :",self.getNowTime(),"]")
                if self.getNowTime()=="0901" or self.getNowTime() =="901":
                    break
                else:
                    time.sleep(1)
                    
            print("Real data 분석 시작 !!!!!!!!!!!!!!!!!!!!!!!!!")
            while(True):
                try:
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'BUY' )
                    self.checkCodeSet(YG,conn,cursor, self.BuyListVolumeRotateTable,'BUY' )
                    
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'SELL' )
                    self.checkCodeSet(YG,conn,cursor, self.BuyListVolumeRotateTable,'SELL' )
                    
                    if self.getNowTime() == "1449":
                        self.checkCodeSet(YG,conn,cursor,self.BuyListTable,'END')
                        break
                    
                    time.sleep(0.5)
                except Exception:
                    self.tracebackLog()
                    print("realData Analyzer종료함.")
#                     break
                    continue
            print("장 종료되었음.")
        elif mode=="Test":
            
            while(self.getNowTime()!= "1500"):
                try:
    #                 self.analyseVolume(YG)
    #                 self.analysePrice(YG)
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'BUY')
                    self.checkCodeSet(YG,conn,cursor, self.BuyListVolumeRotateTable,'BUY')
                     
#                     self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'SELL',count=1,interval=1 )
#                     self.checkCodeSet(YG,conn,cursor, self.BuyListVolumeRotateTable,'SELL' ,count=1,interval=1)
                    
#                     if self.getNowTime() == "1449":
#                     self.checkCodeSet(YG,conn,cursor,self.BuyListTable,'END')
#                     break
                    
                    time.sleep(0.5)
                except Exception:
                    self.tracebackLog()
                    break
                    continue
        elif mode =="RealPart2":
#             while(True):
#                 print("901분 부터 시작합니다.. [현재시각 :",self.getNowTime(),"]")
#                 if self.getNowTime()=="0901" or self.getNowTime() =="901":
#                     break
#                 else:
#                     time.sleep(1)
            '''select StockCode,StockName,"1252","1253" ,(("1253"-"1252")/CAST ("1253" AS REAL))*100 from Relative where (("1253"-"1252")/CAST ("1253" AS REAL))*100.0>0'''
            print("RealPart2 분석 시작 !!!!!!!!!!!!!!!!!!!!!!!!!")
            while(True):
                try:
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'BUY',multiplicationCheck="10",count=1,interval=1 ) #1분전보다 1프로 이상 증가?
                     
                    
                    self.checkCodeSet(YG,conn,cursor, self.BuyListVolumeRotateTable,'BUY' ) #1분전 상황보다 거래량이 5배이상 증가 ?
                    
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'SELL' )    #산것보다 가격이 2프로이상 증가?
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'SELL' )    #산것보다 가격이 3프로이상 하락 ?
                    
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'SELL' )    #산후 시간이 5분이상 지남 ? 
                    
                    self.checkCodeSet(YG,conn,cursor, self.BuyListRelativeTable,'SELL' )    #거래량 사기전 5분동안 < 산후 5분동안?
                    
                    if self.getNowTime() == "1449":
                        self.checkCodeSet(YG,conn,cursor,self.BuyListTable,'END')
                        break
                    
                    time.sleep(0.5)
                except Exception:
                    self.tracebackLog()
                    print("realData Analyzer종료함.")
#                     break
                    continue
            print("장 종료되었음.")
                
            
if __name__ == '__main__':
    ra = RealAnalyse()
    
    YG = YGBuyListDB.YGGetDbData()
#     YG.setProperties(YG.BuyListDBToday,YG.BuyListRelativeTable)
    
    ra.setDB(YG.BuyListDBYesterday)
    proc = mp.Process(target=ra.gogo,args=["RealPart2",]) 
    proc.start()

#     ra.start()
#     print(ra.getSelectQuery('tableName','BUY',interval=60,count=1))