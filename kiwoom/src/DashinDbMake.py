# -*- coding: utf-8 -*-

import btsForDashin
from DBMake import dbm2
import sys,os
import time
from _sqlite3 import OperationalError
import multiprocessing as mp


class DashinDbMake(dbm2):

    def setDBName(self,dbName=""):

        
        if dbName=="":
            self.dbName="kosdaqDashin_"
        else: 
            self.dbName=dbName
            

        super().setDBName(self.dbName)
        

    def createTable(self):
        super().createTable(True)
        
    def updateCode_r(self,Code,Time,coast):
        
        try:
            Cursor = self.getCursor()
            query=super().updateCode(Code,Time,coast,Cursor)
            Cursor.execute(query)
        except:
            self.tracebackLog()
#             self.PrintException()
        
    def run(self):
        print('work start')
        self.setDBName()
        self.createTable()
#         while self.getTimeSource() != "1500":
        print('start')
        while self.getTimeSource()>='900' and self.getTimeSource()<='1500':
            if self.getTimeSource()=='1500':
                break
            try:
                self.initParse()
                _start = time.time()
                Time=self.getTimeSource()
#                 Time='1302'
                for code in self.codeNameCoast:
                    for name in self.codeNameCoast[code]:
                        self.updateCode_r(code,Time,self.codeNameCoast[code][name])
                        
                print('code inserted['+str(time.time()-_start)+'] 시간 ['+str(self.getTime())+']')
                self.commit()
                time.sleep(58)
            except : 
                self.tracebackLog()
#                 self.PrintException()
                continue

if __name__ == '__main__':
    
    dsm = DashinDbMake()
#     dsm.setDBName()
#     dsm.createTable()
    
    while True:
        if dsm.getTimeSource()=='900':
                
            dsm.start()
        else:
            time.sleep(1)