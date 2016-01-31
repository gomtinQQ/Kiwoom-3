# -*- coding: utf-8 -*-

import sqlite3
import ExcelMake
import bts
import time
from _sqlite3 import OperationalError

class dbm:
    
    def __init__(self,dbname=""):
        
        self.conn=""
        
        if dbname=="":
            self.conn = sqlite3.connect("D:\\OneDrive\\python\\sqlite3\\kosdaq.db")
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
        
    def update(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute('''update kosdaq set '900'='100','901'='320' where StockCode='900090' ''')
        
        '''update kosdaq set '900'='100','901'='320' where StockCode='900090' '''
        self.conn.commit()
        
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


if __name__ == '__main__':

    readedExcel = ExcelMake.ExcelCode(setLayout=False)
    readedExcel.ExcelRead(fileName='D:\\Kiwoo\\ExcelData\\20160127\\20160127_yang_1.xlsx')
    wb = readedExcel.getWorkBook()
    ws = readedExcel.getWorkSheet()
    
    codelist = readedExcel.getCodeList()
    
    dbm = dbm()
    bts = bts.mbts()
    
    i = 1
    all = len(codelist)
    for code in codelist:
        bts.IframeUrlWithCode(code)
        tpd = bts.getTimePerDic()
         
        dbm.updateCode(code,tpd)
        print(str(code)+' ['+str(i)+'/'+str(all)+']')
        i+=1
        dbm.commit()
