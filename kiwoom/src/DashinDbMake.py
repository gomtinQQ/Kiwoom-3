# -*- coding: utf-8 -*-

import btsForDashin
import DBMake
import sys,os
import time
from _sqlite3 import OperationalError
import multiprocessing as mp


class DashinDbMake(DBMake.dbm2):

    def setDBName(self,day):
#         self.dbName="D:\\OneDrive\\python\\sqlite3\\kosdaqDashin_"+str(day)+".db"
        

        self.dbName="kosdaqDashin_"+str(day)

        super().setDBName(self.dbName)


    def createTable(self):
        super().createTable()
        
        try:
            self.codeNameCoast
        except AttributeError:
            self.initParse()
        '''set Stock Code and Name'''
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
#                 Time='1302'
                for code in self.codeNameCoast:
                    for name in self.codeNameCoast[code]:
                        self.updateCode(code,Time,self.codeNameCoast[code][name])
                        
                print('code inserted['+str(time.time()-_start)+']')
                self.commit()
                time.sleep(60)
            except : 
                # print(sys.exc_info())
                print('h')
                print(sys.gettrace())
                continue

if __name__ == '__main__':
    dsm = DashinDbMake()
    dsm.setDBName(dsm.getDay())
    dsm.createTable()

    proc = mp.process(target=dsm.doWork())
    proc.start()