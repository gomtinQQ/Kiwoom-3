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
        
    def getCursor(self):
        return self.cursor
        
    def updateCode(self,code,TimePerDict,cursor):
        _start = time.time()
        
#         for tp in TimePerDict.keys():
        for tp in TimePerDict.keys():
            try:
                rtime = tp
                if tp[0]==9 :
                    tp=tp[0:]+'0'+tp[:0]
                rec=tp[:2]+tp[3:]
                if tp[0]!='c':
                    rec=int(rec)
                cursor.execute('update kosdaq set "'+str(rec)+'"="'+str(TimePerDict[rtime])+'" where StockCode='+str(code))
            except OperationalError as err:
#                 print("OperationalError exception occured!!"+str(sys.exc_info()))
                continue
            except Exception as er:
                print("Exception1 "+str(sys.exc_info()))
        print(str(code)+' setting ['+str(time.time()-_start)+']')
        self.commit()
    

    def createTable(self,dbName):
        self.dbName=dbName
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        
        _start=time.time()    
        
        self.cursor.execute('CREATE TABLE `kosdaq` (`StockCode`    INTEGER NOT NULL UNIQUE,`StockName`    INTEGER NOT NULL UNIQUE,PRIMARY KEY(StockCode,StockName));')
        print('table created')
        
        for i in range(9,15):
            for j in range(0,60):
                if j<10:
                    j=str(j)
                    j=j[:0]+str('0')+j[0:]
                self.cursor.execute("alter table kosdaq add '"+str(i)+str(j)+"' REAL")
        print("table created ["+str(time.time()-_start)+"]")
        self.commit()
        
    def dropTable(self,Table):
        
        self.cursor.execute()
    
    def setDBName(self,dbname):
        self.dbName=dbname
        
    def run(self):
        self.conn= sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        
        _start=time.time()
        all = len(self.codelist)
        i=0
        time.sleep(1)
        print(self.name+" is working")
        while (True):
            print('before get')
            try:
                TimePerDict = self.WQueue.get(timeout=5.0)
                print(TimePerDict)
#                 if len(TimePerDict):
#                     print("hi")
#                     time.sleep(1)
#                     continue
                if TimePerDict=='END':
                    print('success~ ['+(time.time()-_start)+']')
                    break
                i+=1
                print('before code')
                
                print('code = '+TimePerDict['code'])
                self.updateCode(TimePerDict['code'],TimePerDict,self.cursor)
                print('code end')
                print('=======================================================['+str(i)+'/'+str(all)+']')
            except Exception as er :
                print("Exception = "+str(sys.exc_info()))
                continue
#         print('hi')
        
        
    def setCodelist(self,codelist):
        self.codelist = codelist
        
    def commit(self):
        self.conn.commit()
        
    def setWQueue(self,WQueue):
        self.WQueue=WQueue

class multi(mp.Process):
    
    def __init__(self):
        super(multi, self).__init__()
#         mp.Process.__init__(self)

    
    def run(self):
        self.bts = bts.mbts()
        while(True):
#             print(self.name+" is working")
            try:
                code = self.RQueue.get()
                if code == 'END':
                    self.RQueue.put('END')
                    self.WQueue.put('END')
                    break

                self.bts.IframeUrlWithCode(code)
                
                tps=self.bts.getTimePerDic()
                self.WQueue.put(tps)
                
            except:
                print('put error :'+str(sys.exc_info()))
                        
    def setting(self,WQueue,RQueue):
        self.WQueue=WQueue
        self.RQueue=RQueue
        
if __name__ == '__main__':

    sys.setrecursionlimit(1000000) #에러방지위해 뎁스 기본값 세팅
    
    readedExcel = ExcelMake.ExcelCode(setLayout=False)
    readedExcel.ExcelRead(fileName='D:\\Kiwoo\\ExcelData\\20160127\\20160127_yang_1.xlsx')
    wb = readedExcel.getWorkBook()
    ws = readedExcel.getWorkSheet()
    codelist = readedExcel.getCodeList()
    RQueue = mp.Queue()
    WQueue = mp.Queue()
    
    
    dbm = dbm2()
    dbm.setDBName("D:\\OneDrive\\python\\sqlite3\\kosdaq.db")

    
    
    dbm.setCodelist(codelist)
    
    for code in codelist:
        RQueue.put(code)
    RQueue.put('END')
    
    
    
    
    print('RQsetting ')
    process=[]
    for proc in range(5):
        proc = multi()
        proc.setting(WQueue, RQueue)
        process.append(proc)
        proc.daemon= True
        proc.start()
    
#     WQueue.put('END')
    dbm.setWQueue(WQueue)
    dbm.start()
    dbm.join()
    dbm.commit()

