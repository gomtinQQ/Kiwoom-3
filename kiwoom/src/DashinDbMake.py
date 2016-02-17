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
        

        
    def run(self):
        print('work start')
        while self.getTimeSource() != "1500":
            try:
                self.initParse()
                _start = time.time()
                Time=self.getTimeSource()
#                 Time='1302'
                for code in self.codeNameCoast:
                    for name in self.codeNameCoast[code]:
                        self.updateCode(code,Time,self.codeNameCoast[code][name])
                        
                print('code inserted['+str(time.time()-_start)+'] 시간 ['+str(self.getTime())+']')
                self.commit()
                time.sleep(58)
            except : 
                self.PrintException()
                continue

if __name__ == '__main__':
    dsm = DashinDbMake()
    dsm.setDBName()
    dsm.createTable()
    

    dsm.start()
#     proc = mp.process(target=dsm.doWork())
#     while True:
#         if dsm.getTimeSource()=='900':
#     proc.start()
#             break
#         else :
#             time.sleep(1)
