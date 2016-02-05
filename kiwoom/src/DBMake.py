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
        self.conn=""
        if dbname=="":
            self.conn = sqlite3.connect("D:\\OneDrive\\python\\sqlite3\\kosdaq1.db")
        else:
            self.conn = sqlite3.connect(dbname)
            
        self.cursor = self.conn.cursor()
    def getConnection(self,dbname=""):
            
        return self.conn
        
    def setCursor(self,conn):
        
        self.cursor=conn.cursor()
        
    def setNamelist(self,namelist,tablename,conn):
        
        self.cursor = conn.cursor()
        
        for name in namelist:
            name = str(name)
            self.cursor.execute("insert into "+tablename+" (StockName) values ("+name+")")
        conn.commit()

    def setNameCode(self,codeName,tablename,conn):
        
        self.cursor = conn.cursor()
        
        for name in namelist:
            name = str(name)
            self.cursor.execute("insert into "+tablename+" (StockName) values ("+name+")")
        conn.commit()

        
    def updateCode(self,code,TimePerDict):
        _start = time.time()
        
        for tp in TimePerDict.keys():
            try:
                rtime = tp
                if tp[0]==9:
                    tp=tp[0:]+'0'+tp[:0]
                rec=tp[:2]+tp[3:]
                rec=int(rec)
                self.cursor.execute('update kosdaq set "'+str(rec)+'"="'+str(TimePerDict[rtime])+'" where StockCode='+str(code))
            except OperationalError:
                continue
        print(str(code)+' setting ['+str(time.time()-_start)+']')
    
    def commit(self):
        self.conn.commit()
    
    def setWQueue(self,WQueue):
        self.WQueue=WQueue
        
    def run(self):
        
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
                self.updateCode(code,TimePerDict[code])
            print('=======================================================['+str(i)+'/'+str(all)+']')
#         print('hi')
        
        
    def setCodelist(self,codelist):
        self.codelist = codelist
    

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
    
    WQueue = mp.Queue()
    dbm = dbm2()
    
    bts = bts.mbts()
    
    RQueue = mp.Queue()
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
    dbm.setCursor(dbm.getConnection())
    dbm.start()
    dbm.join()
    dbm.commit()

