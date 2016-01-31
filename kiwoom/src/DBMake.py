# -*- coding: utf-8 -*-

import sqlite3
import ExcelMake
import bts
import time
import multiprocessing as mp
from _sqlite3 import OperationalError

class dbm(mp.Process):
    
    def __init__(self,dbname=""):
        super(multi, self).__init__()
        self.conn=""
        
        if dbname=="":
            self.conn = sqlite3.connect("D:\\OneDrive\\python\\sqlite3\\kosdaq1.db")
        else:
            self.conn = sqlite3.connect(dbname)
            
        self.cursor = self.conn.cursor()
    
    def getConnection(self,dbname=""):
            
        return self.conn
        

    def setCodelist(self,codelist,tablename,conn):
        
        self.cursor = conn.cursor()
        
        for code in codelist:
            code = str(code)
            self.cursor.execute("insert into "+tablename+" (StockCode) values ("+code+")")
        conn.commit()
        
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
#                 print(str(rec))
#                 print(str(TimePerDict[rtime]))
#                 print(str(code))
                self.cursor.execute('update kosdaq set "'+str(rec)+'"="'+str(TimePerDict[rtime])+'" where StockCode='+str(code))
            except OperationalError:
                continue
        print(str(code)+' setting ['+str(time.time()-_start)+']')
    
    def commit(self):
        self.conn.commit()
    
    def setWQueue(self,WQueue):
        self.WQueue=WQueue
        
    def run(self):
        while True:
            TimePerDict = self.Wqueue.get()
        
            self.updateCode(code,TimePerDict)
        
    def setCodelist(self,codelist):
        self.codelist = codelist
    

class multi(mp.Process):
    
    def __init__(self,RQueue,WQueue,bts):
        super(multi, self).__init__()
        self.WQueue=WQueue
        self.RQueue=RQueue
        self.bts=bts
    
    def run(self):
        
        while(True):
            print(self.name+" is working")
            code = self.RQueue.get()
            if code == 'END':
                self.RQueue.put('END')
                break
            self.bts.IframeUrlWithCode(code)
            tpd = self.bts.getTimePerDic()
            
            self.WQueue.put(tpd)
                        

if __name__ == '__main__':

    readedExcel = ExcelMake.ExcelCode(setLayout=False)
    readedExcel.ExcelRead(fileName='D:\\Kiwoo\\ExcelData\\20160127\\20160127_yang_1.xlsx')
    wb = readedExcel.getWorkBook()
    ws = readedExcel.getWorkSheet()
    
    codelist = readedExcel.getCodeList()
    
    dbm = dbm()
    bts = bts.mbts()
    
    RQueue = mp.Queue()
    WQueue = mp.Queue()
    for code in codelist:
        RQueue.put(code)
    RQueue.put('END')
    
    print('RQsetting ')
    process=[]
    for proc in range(5):
        proc = multi(RQueue,WQueue,bts)
        process.append(proc)
        proc.start()
     
    for code in codelist:
         
    
    
    dbm.commit()
