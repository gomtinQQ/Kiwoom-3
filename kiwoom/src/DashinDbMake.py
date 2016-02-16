# -*- coding: utf-8 -*-

import btsForDashin
import DBMake
import sys,os
import time
from _sqlite3 import OperationalError
import multiprocessing as mp


class DashinDbMake(DBMake.dbm2):

    def setDBName(self,dbName=""):

        
        if dbName=="":
            self.dbName="kosdaqDashin_"
        else: 
            self.dbName=dbName
            

        super().setDBName(self.dbName)


    def createTable(self):
        super().createTable(True)
        

        
    def doWork(self):
        print('work start')
        while self.getTimeSource() == "1459":
            try:
                self.initParse()
                _start = time.time()
                Time=self.getTimeSource()
#                 Time='1302'
                for code in self.codeNameCoast:
                    for name in self.codeNameCoast[code]:
                        self.updateCode(code,Time,self.codeNameCoast[code][name])
                        
                print('code inserted['+str(time.time()-_start)+']')
                self.commit()
                time.sleep(60)
            except : 
                self.PrintException()
                continue

if __name__ == '__main__':
    dsm = DashinDbMake()
    dsm.setDBName()
    dsm.createTable()

    proc = mp.process(target=dsm.doWork())
    
    proc.start()