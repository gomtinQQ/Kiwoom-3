# -*- coding: utf-8 -*-

import btsForDashin
import DBMake
import sys
import time
from _sqlite3 import OperationalError
import multiprocessing as mp


class DashinDbMake:
    
    def createTable(self,day):
        try:
            self.dbm.createTable("D:\\OneDrive\\python\\sqlite3\\kosdaqDashin_"+str(day)+".db")
        except OperationalError :
            print('table있음')
            print(str(sys.exc_info()))
           
    def initParse(self):
        print('parse start')
        self.dbm = DBMake.dbm2()
        bfd = btsForDashin.btsForReal()
        bfd.UrlParsing()
        self.codeNameCoast = bfd.getCodeNameCoast()
        print('parse end')

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
        
    def setCodeNameCoast(self,Time):
        for code in self.codeNameCoast:
            for name in self.codeNameCoast[code]:
#             dbm.setCode(code,name)
                self.dbm.updateCode(code,Time,self.codeNameCoast[code][name])
                
    def commit(self):
        self.dbm.commit()
        
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
    
    
    dsm = DashinDbMake()
    dsm.initParse()
    dsm.createTable(dsm.getDay())

    dsm.commit()        
    
    proc = mp.process(target=dsm.doWork())
    proc.start()
    