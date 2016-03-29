# -*- coding: utf-8 -*-

import sqlite3
import sys,os
from _sqlite3 import OperationalError
# sys.path.append('../')
sys.path.append('../Data')
sys.path.append('../DB')
import YGGetWebData
import time,datetime
import btsForDashin
import MakeDB
import traceback
import multiprocessing as mp
import DBSet
import YGBuyListDB 

class RealAnalyse(DBSet.DBSet):

    def getSelectQuery(self,tableName,Time="",count="",interval=""):
        '''set SimulatorTime if not,get the current Time'''
        
        if count=="":
            count=5
        count=int(count)
        
        if interval=="":
            interval=1
        interval=int(interval)
            
#         print(self.getNowTime(),self.pastAgo(interval))
        self.tocount = 1
        
        if Time=="":
            Time = int(self.getNowTime())
            
        Time=int(Time)
        currTime = self.getNowTime()
        beforeTime = self.pastAgo(currTime,interval)
        
        self.whereQuery = 'select StockCode,StockName from '+tableName+' where "' + \
            str(beforeTime) + '"<"' + str(currTime) + '"'
            
        self.getSelectQuery_proc(count, beforeTime ,interval)

        
        
#         print(self.whereQuery)
        return self.whereQuery
    
    def getSelectQuery_proc(self, count, Time,interval):
        '''
        get the update query set
        '''

        if self.tocount == count:
            self.tocount = 0
#             print(self.whereQuery)
            return self.whereQuery

        else:  
#             Time=self.TimeFormat(Time)
#             currTime = self.TimeFormat(Time)
            currTime = Time
            print(currTime,interval)
            beforeTime =self.pastAgo(currTime, interval)
 
            self.whereQuery = self.whereQuery + ' and "' + \
                str(beforeTime) + '"<"' + str(currTime) + '"'

            self.tocount += 1
            self.getSelectQuery_proc(count, beforeTime,interval)
    
    def analyseVolume(self,YG):
        conn = sqlite3.connect(self.BuyListDBYesterday)
        cursor = conn.cursor()
        
        
#         query="select \""+str(beTime)+"\",\""+str(toTime)+ "\" from "+self.BuyListVolumeRotateTable+" where StockCode = 227950"
        query = self.getSelectQuery(self.BuyListVolumeRotateTable,count=2)
#         print(query)
        print(query)
        cursor.execute(query)
        dd = cursor.fetchall()
        print(dd)
#         if dd[0][0]<dd[0][1]:
        print(dd[0][0],dd[0][1])
        for i in range(len(dd)):
            YG.updateBuy(dd[i][0])
        
    def analysePrice(self,YG):
        conn = sqlite3.connect(self.BuyListDBYesterday)
        cursor = conn.cursor()
        
        query = self.getSelectQuery(self.BuyListRelativeTable, count=2)
        
        cursor.execute(query)
        dd = cursor.fetchall()
#         print(dd)
        for i in range(len(dd)):
            YG.updateBuy(dd[i][0])
        
    def gogo(self):
        while(True):
            try:
                YG = YGBuyListDB.YGGetDbData()
                YG.setProperties(YG.BuyListDBYesterday,YG.BuyListRelativeTable)
                self.analyseVolume(YG)
                self.analysePrice(YG)
                time.sleep(0.5)
                
            except Exception:
                self.tracebackLog()
                continue
                
            
if __name__ == '__main__':
    ra = RealAnalyse()
    
    proc = mp.Process(target=ra.gogo)
    proc.start()
#     print(ra.getSelectQuery('tableName'))