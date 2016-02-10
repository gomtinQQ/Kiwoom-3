# -*- coding: utf-8 -*-

import btsForDashin
import DBMake
import sys
import time
from _sqlite3 import OperationalError
import multiprocessing as mp


class selectBuyList:
    
    def createSelectTable(self,day):
        try:
            self.dbmForInsert.createTable("D:\\OneDrive\\python\\sqlite3\\kosdaqDashin_buyList_"+str(day)+".db")
        except OperationalError :
            print('table already exists')
            print(str(sys.exc_info()))
           
    def initDB(self):
        self.dbmForSelect = DBMake.dbm2()
        self.dbmForInsert = DBMake.dbm2()
        
            

    def getTime(self):
        now = time.localtime()
        Hour = now.tm_hour
        Minute=now.tm_min
#         print(str(Hour) +':'+ str(Minute))
        return str(Hour)+':'+str(Minute)
    
    def getDay(self):
        now = time.localtime()
        mon = now.tm_mon
        day = now.tm_mday
        
        if int(mon) <10:
            mon = '0'+str(mon)
            mon=str(mon)
        if int(day)<10:
            day = '0'+str(day)
            day = str(day)
        monday = str(mon)+str(day)
        print(monday)
        return monday
        

                
    def commit(self):
        self.dbmForInsert.commit()
        self.dbmForInsert.comm
        
    def setDBProperties(self,day):
        self.dbmForInsert.setDBProperties("D:\\OneDrive\\python\\sqlite3\\kosdaqDashin_buyList_"+str(day)+".db")
        
    def selectBuy(self):
        pass
    def inserBuy(self):
        pass
    
    def doWork(self):
        print('work start')
        while True:
            try:
                bfd = btsForDashin.btsForReal()
                bfd.UrlParsing()
                self.codeNameCoast = bfd.getCodeNameCoast()
                _start = time.time()
                Time=self.getTime()
                for code in self.codeNameCoast:
                    for name in self.codeNameCoast[code]:
                        self.dbm.updateCode(code,Time,self.codeNameCoast[code][name])
                        
                print('code inserted['+str(time.time()-_start)+']')
                self.commit()
                time.sleep(60)
            except : 
                print(str(sys.exc_info()))
                continue

if __name__=="__main__":
    sbl = selectBuyList()
    sbl.initDB()
    print('ss')
