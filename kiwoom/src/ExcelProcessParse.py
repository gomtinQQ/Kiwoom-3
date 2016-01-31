# -*- coding: utf-8 -*-
import sqlite3
import win32com.client
import multiprocessing as mp
import bts
import ExcelMake
import time

class CodeParser(mp.Process):
    
    def setRW(self,rq,wq,codelist,readedExcel):
        self.rq=rq
        self.wq=wq
        self.codelist = codelist
        self.bt = bts.mbts()
    
    def run(self):
        
        for code in self.codelist:
            self.codeParse(code)
            
    def codeParse(self,code):
        
        self.bt.IframeUrlWithCode(self.addZeroToStockCode(str(code)))
        
        return self.bt.getTimePerDic()     
    
    
    def addZeroToStockCode(self,str):
        str=str.strip()

        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
        return str
    
class CodeWriter(mp.Process):
    
    def setRW(self,rq):
        self.rq=rq
        self.wq=wq
        
    def run(self):
        
        conn = sqlite3.connect("kospi.db")
        cursor = conn.cursor()
        cursor.execute("select * from kospi")
        print(cursor.fetchall())
    
    
if __name__ == '__main__':
    parser = CodeParser()
    
    readedExcel = ExcelMake.ExcelCode(setLayout=False)
    readedExcel.ExcelRead(fileName='D:\\Kiwoo\\ExcelData\\20160127\\20160127_yang_1.xlsx')
    wb = readedExcel.getWorkBook()
    ws = readedExcel.getWorkSheet()
    
    codelist = readedExcel.getCodeList()
    
    rq = mp.Queue()
    wq = mp.Queue()
    
    parser.setRW(rq, wq, codelist,readedExcel)
#     parser.start()
    
    codewriter = CodeWriter()
    
    codewriter.start()
    