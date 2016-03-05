# -*- coding: utf-8 -*-

import sqlite3
import sys,os
sys.path.append('../')
sys.path.append('../Data')
import YGGetWebData
import time
import btsForDashin
import linecache

class DBMake():
        
    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
        
    def setTable(self,tableName):
        self.tableName = tableName
    
    def setCodeNameCoast(self):
        bfd = btsForDashin.btsForReal()
        self.codeNameCoast = bfd.UrlParsing()
    
    def setProperties(self,dbName,table):
        
        self.dbName=dbName
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        self.setTable(table)
        
    def createDatabase(self,DBName,table):
        '''형식에 맞는 테이블 생성.'''
        self.setTable(table)
        self.dbName=DBName
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        
        _start=time.time()
        try:
            self.cursor.execute('CREATE TABLE `'+self.tableName+'` \
            ( \
            `StockCode`  INTEGER NOT NULL UNIQUE,\
            `StockName`  INTEGER UNIQUE,\
            PRIMARY KEY(StockCode)\
            );')
            
            print("table created ["+str(time.time()-_start)+"]")
        except :
            self.PrintException()
        self.conn.commit()
    
    def addCodeNameData(self):
        '''테이블 생성후 코드와,이름 삽입'''
        
        if self.codeNameCoast ==None:
            self.setCodeNameCoast()
        if self.tableName ==None:
            raise ("Table Name not Assigned")
            
        for code in self.codeNameCoast:
            for Name in self.codeNameCoast[code]:
                query = 'Insert into '+self.tableName+'\
                (StockCode,StockName) \
                values ("'+str(code)+'","'+str(Name)+'");'
                self.cursor.execute(query)
        self.conn.commit()
    
    def addDatePrice(self):
        '''날짜에 맞게  종가를 대입한다.'''
        
        if self.codeNameCoast ==None:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        for index,code in enumerate(self.codeNameCoast):
            
            data = YGGetWebData.getStockPriceData(str(code),'2014-09-1')
            for index in range(len(data)):
                try:
                    Date = str(data['DateIndex'][index]).replace("'","")
                    Price= data['close'][index]
                    
                    query = "update "+self.tableName+" set "+Date+" = "+str(Price)+" where StockCode='"+str(code)+"';"
                    self.cursor.execute(query)
                except Exception : 
                    self.PrintException()
                    continue
                
                self.conn.commit()
            print(code,index,len(self.codeNameCoast))

        
            
    def addDateColumn(self):
        
        '''날짜칼럼 삽입.'''
        if self.codeNameCoast ==None:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        code='126700'
        data = YGGetWebData.getStockPriceData(str(code),'2014-09-1')
        
        for index in range(len(self.codeNameCoast)):
            try:
                Date = str(data['DateIndex'][index]).replace("'","")
                print(Date)
                query1 = "alter table "+self.tableName+" add "+str(Date)+" INTEGER;";
                self.cursor.execute(query1)
            except Exception:
                continue
        self.conn.commit

        
if __name__ == '__main__':
    cp =closePriceMake()
    cp.createDatabase('../../Sqlite3/test.db')
#     cp.addCodeNameData()
    cp.addDatePrice()
#     cp.addDateColumn()