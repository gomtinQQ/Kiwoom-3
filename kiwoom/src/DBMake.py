# -*- coding: utf-8 -*-

import sqlite3
import ExcelMake
import bts
import time
import multiprocessing as mp
from _sqlite3 import OperationalError
import sys

class dbm2(mp.Process):
    
    def __init__(self,dbname=""):
        super(dbm2, self).__init__()

        
    def getConnection(self):
        return self.conn
        

        
    def updateCode(self,code,TimePerDict,cursor):
        _start = time.time()
        
#         for tp in TimePerDict.keys():
        for tp in list(TimePerDict):
            try:
                rtime = tp
                if tp[0]==9:
                    tp=tp[0:]+'0'+tp[:0]
                rec=tp[:2]+tp[3:]
                rec=int(rec)
                cursor.execute('update kosdaq set "'+str(rec)+'"="'+str(TimePerDict[rtime])+'" where StockCode='+str(code))
            except OperationalError:
                print("exception occured!!")
                continue
        print(str(code)+' setting ['+str(time.time()-_start)+']')
        self.commit()
    

    
    def setDBName(self,dbname):
        self.dbName=dbname
        
    def run(self):
        self.conn= sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        
        _start=time.time()
        all = len(self.codelist)
        i=0
        
        while True:
            TimePerDict = self.WQueue.get()
            if TimePerDict=='END':
                print('success~ ['+(time.time()-_start)+']')
                break
            i+=1
            for code in TimePerDict:
                self.updateCode(code,TimePerDict[code],self.cursor)
            print('=======================================================['+str(i)+'/'+str(all)+']')
#         print('hi')
        
        
    def setCodelist(self,codelist):
        self.codelist = codelist
        
    def commit(self):
        self.conn.commit()
    def setWQueue(self,WQueue):
        self.WQueue=WQueue

class multi(mp.Process):
    
    def __init__(self,RQueue,WQueue,bts):
        super(multi, self).__init__()
        self.WQueue=WQueue
        self.RQueue=RQueue
        self.bts=bts
    
    def run(self):
        
        codeandvalue={}
        while(True):
            print(self.name+" is working")
            code = self.RQueue.get()
            if code == 'END':
                self.RQueue.put('END')
                self.WQueue.put('END')
                break
            self.bts.IframeUrlWithCode(code)
            tpd = self.bts.getTimePerDic()
            codeandvalue[code] =tpd 
            self.WQueue.put(codeandvalue)
                        

if __name__ == '__main__':

    sys.setrecursionlimit(2000) #에러방지위해 뎁스 기본값 세팅
    
    readedExcel = ExcelMake.ExcelCode(setLayout=False)
    readedExcel.ExcelRead(fileName='D:\\Kiwoo\\ExcelData\\20160127\\20160127_yang_1.xlsx')
    wb = readedExcel.getWorkBook()
    ws = readedExcel.getWorkSheet()
    codelist = readedExcel.getCodeList()
    RQueue = mp.Queue()
    WQueue = mp.Queue()
    
    
    dbm = dbm2()
    dbm.setDBName("D:\\OneDrive\\python\\sqlite3\\kosdaq.db")
    bts = bts.mbts()
    
    
    
    for code in codelist:
        RQueue.put(code)
    RQueue.put('END')
    
    print('RQsetting ')
    process=[]
    for proc in range(5):
        proc = multi(RQueue,WQueue,bts)
        process.append(proc)
        proc.start()
         
#     WQueue.put('END')
    dbm.setWQueue(WQueue)
    dbm.setCodelist(codelist)
    dbm.start()
    dbm.join()
    dbm.commit()

