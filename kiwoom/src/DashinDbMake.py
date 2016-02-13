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

#     proc = mp.process(target=dsm.doWork())
#     proc.start()