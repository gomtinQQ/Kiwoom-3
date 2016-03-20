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


    
    def analyseVolume(self,YG):
        conn = sqlite3.connect(self.BuyListDBToday)
        cursor = conn.cursor()
        
        currTime =datetime.datetime.today()
        currMin = currTime.minute
        one_past = int(currMin)-1
        
        currHour = currTime.hour
        
        if currMin <2:
            currMin='0'+str(currMin)
        toTime = str(currHour)+str(currMin)
        beTime = str(currHour)+str(one_past)
        toTime='901'
        beTime='900'
        
        query="select \""+str(beTime)+"\",\""+str(toTime)+ "\" from "+self.BuyListVolumeRotateTable+" where StockCode = 227950"
        cursor.execute(query)
        dd = cursor.fetchall()
        
        if dd[0][0]<dd[0][1]:
            YG.updateBuy(227950)
        print(dd[0][0],dd[0][1])
        
    def analysePrice(self):
        conn = sqlite3.connect(self.BuyListDBToday)
        cursor = conn.cursor()
        
        currTime =datetime.datetime.today()
        currMin = currTime.minute
        one_past = int(currMin)-1
        
        currHour = currTime.hour
        
        if currMin <2:
            currMin='0'+str(currMin)
        toTime = str(currHour)+str(currMin)
        beTime = str(currHour)+str(one_past)
        
        query="select \""+str(beTime)+"\" from "+self.BuyListRelativeTable
        
        cursor.execute(query)
        dd = cursor.fetchall()
#         print(dd)
        
    def gogo(self):
        try:
            YG = YGBuyListDB.YGGetDbData()
            YG.setProperties(YG.BuyListDBToday,YG.BuyListRelativeTable)
            while(True):
                self.analyseVolume(YG)
                self.analysePrice()
                time.sleep(0.5)
                
        except Exception:
            self.tracebackLog()
                
            
if __name__ == '__main__':
    ra = RealAnalyse()
    
    proc = mp.Process(target=ra.gogo)
    proc.start()