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

    def getSelectQuery(self,tableName,buySell,Time="",count="",interval=""):
        '''set SimulatorTime if not,get the current Time'''
        
        if count=="":
            count=5
        count=int(count)
        
        if interval=="":
            interval=1
        interval=int(interval)
        self.tocount = 1
        
        if Time=="":
            Time = int(self.getNowTime())
            
        Time=int(Time)
        currTime = self.getNowTime()
        beforeTime = self.pastAgo(currTime,interval)
        
        op=">"
        if buySell =="B" or buySell =="BUY":
            op = "<"
        self.whereQuery = 'select StockCode,StockName from '+tableName+' where "' + \
            str(beforeTime) +'"'+op+'"' + str(currTime) + '"'
            
        self.getSelectQuery_proc(count, beforeTime ,interval,op)
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
    
    def checkCodeSet(self,YG,db,tableName,BS):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        query = self.getSelectQuery(tableName, buySell=BS,count=2)
        
        cursor.execute(query)
        buyListCode= cursor.fetchall()
        
        
        try:
            print(query)
            if BS =="BUY":
                for i in range(len(buyListCode)): 
                    YG.updateBuy(buyListCode[i][0])
            elif BS == "SELL":
                for i in range(len(buyListCode)):
                    YG.updateSell(buyListCode[i][0])
                    
            else :
                print('Select correctly Buy or Sell ')
        except :
            self.tracebackLog()
        
        
    def gogo(self,YG=""):
        
        print(YG)
        if YG =="":
            print('YGMAKING')
            YG = YGBuyListDB.YGGetDbData()
            YG.setProperties(YG.BuyListDBYesterday,YG.BuyListRelativeTable)
        while(True):
            try:
#                 self.analyseVolume(YG)
#                 self.analysePrice(YG)
                self.checkCodeSet(YG,self.BuyListDBYesterday, self.BuyListRelativeTable,'BUY' )
                self.checkCodeSet(YG,self.BuyListDBYesterday, self.BuyListVolumeRotateTable,'BUY' )
                
                self.checkCodeSet(YG,self.BuyListDBYesterday, self.BuyListRelativeTable,'SELL' )
                self.checkCodeSet(YG,self.BuyListDBYesterday, self.BuyListVolumeRotateTable,'SELL' )
                
                
                time.sleep(0.5)
                
            except Exception:
                self.tracebackLog()
                break
                continue
                
            
if __name__ == '__main__':
    ra = RealAnalyse()
    df =[]
    df.append("YG")
    YG = YGBuyListDB.YGGetDbData()
#     print(YG.BuyListDBYesterday,YG.BuyListRelativeTable)
    YG.setProperties(YG.BuyListDBYesterday,YG.BuyListRelativeTable)
    proc = mp.Process(target=ra.gogo, args=(YG,) ) 
    proc.start()
#     print(ra.getSelectQuery('tableName','BUY',interval=60,count=1))