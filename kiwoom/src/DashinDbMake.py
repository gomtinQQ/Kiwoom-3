# -*- coding: utf-8 -*-

import btsForDashin
import DBMake
import sys
import time
from _sqlite3 import OperationalError
import multiprocessing as mp


class DashinDbMake(DBMake.dbm2):

    def setDBName(self,day):
        self.dbName="D:\\OneDrive\\python\\sqlite3\\kosdaqDashin_"+str(day)+".db"

    def setDBProperties(self):
        super().setDBProperties(self.dbName)

    def createTable(self):
        super().createTable()
        
        try:
            self.codeNameCoast
        except AttributeError:
            self.initParse()
        
        for code in self.codeNameCoast:
            for name in self.codeNameCoast[code]:
                self.setCode(code,name)
        self.commit()

        
    def doWork(self):
        print('work start')
        while True:
            try:
#                 bfd = btsForDashin.btsForReal()
#                 bfd.UrlParsing()
#                 self.codeNameCoast = bfd.getCodeNameCoast()
                self.initParse()
                _start = time.time()
                Time=self.getTimeSource()
                
                for code in self.codeNameCoast:
                    for name in self.codeNameCoast[code]:
                        self.updateCode(code,Time,self.codeNameCoast[code][name])
                        
                print('code inserted['+str(time.time()-_start)+']')
                self.commit()
                time.sleep(60)
            except : 
                print(str(sys.exc_info()))
                continue

if __name__=="__main__":
    
    
    dsm = DashinDbMake()
    dsm.setDBName(dsm.getDay())
    dsm.setDBProperties()
    dsm.createTable()

    proc = mp.process(target=dsm.doWork())
    proc.start()
    