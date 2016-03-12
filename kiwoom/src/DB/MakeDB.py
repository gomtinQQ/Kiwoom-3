# -*- coding: utf-8 -*-
import multiprocessing as mp
import sqlite3
import configparser
import sys,os
sys.path.append('../')
sys.path.append('../Data')
import YGGetWebData
import time
import btsForDashin
import linecache

class DBMake():
    
    
    lock = mp.Lock()
    querylock = mp.Lock()
    config = configparser.ConfigParser()
    config.read("../config/config.ini")
    
    def initConfigSet(self):
        
        self.ForeignerDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB") 
        self.ComapanyDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB")
        self.VolumeDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB")
        self.ClosePriceDB = self.config.get("DATABASE","ClosePriceDB")
        
#         print(self.VolumeDB)
        self.ForeignerTable = self.config.get("DATABASE","ForeignTable")
        self.CompanyTable = self.config.get("DATABASE","CompanyTable")
        self.VolumeTable = self.config.get("DATABASE","VolumeTable")
        self.ClosePriceTable = self.config.get("DATABASE","ClosePriceDBTable")
#         print(self.VolumeTable)
    
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
    def commit(self):
        
        self.lock.acquire()
        self.conn.commit()
        self.lock.release()
        
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
        
        self.commit()
    
    def addCodeNameData(self):
        '''테이블 생성후 코드와,이름 삽입'''
        
        if self.codeNameCoast ==None:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
            
        for code in self.codeNameCoast:
            for Name in self.codeNameCoast[code]:
                query = 'Insert into '+self.tableName+' \
                (StockCode,StockName) \
                values ("'+str(code)+'","'+str(Name)+'");'
                self.cursor.execute(query)
        self.commit()
    
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
                
                self.commit()
            print(code,index,len(self.codeNameCoast))

        
            
    def addDateColumn(self):
        
        '''날짜칼럼 삽입.'''
        try:
            self.codeNameCoast
        except AttributeError:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        code='126700'   #126700의 데이터를갖고 날짜를 가져온다.
        data = YGGetWebData.getStockPriceData(str(code),'2014-09-1')
#         print(len(self.codeNameCoast),len(data['DateIndex']))
        for index in range(len(data['DateIndex'])):
            try:
#                 print(index)
#                 print(data['DateIndex'][index])
                Date = str(data['DateIndex'][index]).replace("'","")
#                 print(Date)
                query1 = "alter table "+self.tableName+" add "+str(Date)+" INTEGER;";
                self.cursor.execute(query1)
            except Exception:
                self.PrintException()
                continue
        self.commit()
    
    def addVolume(self):
        
        if self.codeNameCoast ==None:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        i=0
        for index,code in enumerate(self.codeNameCoast):
            
            data = YGGetWebData.getStockPriceData(str(code),'2016-02-04')
            for index in range(len(data)):
                try:
#                     print(str(data['DateIndex'][index]))
                    Date = str(data['DateIndex'][index]).replace("'","")
                    volume= data['volume'][index]
                    
                    query = "update "+self.tableName+" set "+Date+" = "+str(volume)+" where StockCode='"+str(code)+"';"
                    self.cursor.execute(query)
                except Exception : 
                    self.PrintException()
                    continue
                
                self.commit()
            i+=1
            print('Code[',code,']','Total[',index,'] [',i,'/',len(self.codeNameCoast),'] (Volume)')
    
    def addForeign(self):
        
        if self.codeNameCoast ==None:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        i=0
        for index,code in enumerate(self.codeNameCoast):
            
            data = YGGetWebData.getForeignerAndCompanyPureBuy(str(code),'2016-02-04')
            for index in range(len(data)):
                try:
                    Date = str(data['DateTime'][index]).split(' ')
                    Date = Date[0]
                    Foreign= data['Foreign'][index]
                    
                    query = "update "+self.tableName+" set '"+Date+"' = "+str(Foreign)+" where StockCode='"+str(code)+"';"
                    self.cursor.execute(query)
                except Exception : 
                    self.PrintException()
                    continue
                
                self.commit()
            i+=1
            print('Code[',code,']','Total[',index,'] [',i,'/',len(self.codeNameCoast),'] (Foreign)')
    
    def addCompany(self):
        
        if self.codeNameCoast ==None:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        i=0
        for index,code in enumerate(self.codeNameCoast):
            
            data = YGGetWebData.getForeignerAndCompanyPureBuy(str(code),'2016-02-04')
            for index in range(len(data)):
                try:
                    Date = str(data['DateTime'][index]).split(' ')
                    Date = Date[0]
                    Company= data['Company'][index]
                    
                    query = "update "+self.tableName+" set '"+Date+"' = "+str(Company)+" where StockCode='"+str(code)+"';"
                    self.cursor.execute(query)
                except Exception : 
                    self.PrintException()
                    continue
                
                self.commit()
            i+=1
            print('Code[',code,']','Total[',index,'] [',i,'/',len(self.codeNameCoast),'] (Company) ')
    
    def ConfigTest(self):
        print(self.config.sections())
        print(self.config.options("DATABASE"))
        print(self.config.get("DATABASE","volumeandforeignandcompanydb"))
        
if __name__ == '__main__':
    cp =DBMake()
    cp.createDatabase('../../Sqlite3/test.db')
#     cp.addCodeNameData()
#     cp.addDatePrice()
#     cp.addDateColumn()