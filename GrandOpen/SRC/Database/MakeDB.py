# -*- coding: utf-8 -*-
import multiprocessing as mp
import sqlite3
import configparser
import sys,os
from _sqlite3 import OperationalError
from SRC.WEB import YGGetWebData,btsForDashin
from SRC.Database import DBSet
import time,datetime
import linecache
import traceback
import logging
from logging.handlers import RotatingFileHandler

class DBMake(DBSet.DBSet):
    
    
        
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
#             self.PrintException()
            self.tracebackLog()
         
        self.commit()
    def createDatabase2(self,DBName,table):
        
        self.setTable(table)
        self.dbName=DBName
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
         
        _start=time.time()
        try:
            self.cursor.execute('CREATE TABLE `'+self.tableName+'` \
            (`BUYSELL`  TEXT ,\
            `StockTime` TEXT );')
             
            print("table created ["+str(time.time()-_start)+"]")
        except :
#             self.PrintException()
            self.tracebackLog()
         
        self.commit()
        
    
    def addCodeNameData(self):
        '''테이블 생성후 코드와,이름 삽입'''
        
#         if self.codeNameCoast ==None:
        try :
            self.codeNameCoast
        except:
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
        
#         if self.codeNameCoast ==None:
        self.setProperties(self.ForeignerDB,self.ClosePriceTable)
        self.addDateColumn()
        try:
            self.codeNameCoast
        except AttributeError : 
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        i=0
        for index,code in enumerate(self.codeNameCoast):
            
            data = YGGetWebData.getStockPriceData(str(code),self.start_date_closePrice)
            for index in range(len(data)):
                try:
                    Date = str(data['DateIndex'][index]).replace("'","")
                    Price= data['close'][index]
                    
                    query = "update "+self.tableName+" set "+Date+" = "+str(Price)+" where StockCode='"+str(code)+"';"
                    self.cursor.execute(query)
                except Exception : 
                    self.tracebackLog()
#                     self.PrintException()
                    continue
                
                self.commit()
            i+=1
            print('code[',code,'] Total[',index,'] (',i,'/',len(self.codeNameCoast),') (ClosePrice)')
        
        
            
    def addDateColumn(self):
        
        '''날짜칼럼 삽입.'''
        try:
            self.codeNameCoast
        except AttributeError:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        code='005930'   #126700의 데이터를갖고 날짜를 가져온다.
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
            except OperationalError:
                print('날짜컬럼 생성하다 중복에러 (상관없음)')
                continue
            except Exception:
                self.tracebackLog()
#                 self.PrintException()
#                 continue
        self.commit()
    
    def addVolume(self):
        

        self.setProperties(self.VolumeDB,self.VolumeTable)
        self.addDateColumn()
        try:
            self.codeNameCoast
        except:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        
        i=0
        for index,code in enumerate(self.codeNameCoast):
            
            data = YGGetWebData.getStockPriceData(str(code),self.start_date_Volume)
            for index in range(len(data)):
                try:
#                     print(str(data['DateIndex'][index]))
                    Date = str(data['DateIndex'][index]).replace("'","")
                    volume= data['volume'][index]
                    
                    query = "update "+self.tableName+" set "+Date+" = "+str(volume)+" where StockCode='"+str(code)+"';"
                    self.cursor.execute(query)
                except Exception : 
                    self.tracebackLog()
#                     self.PrintException()
                    continue
                
                self.commit()
            i+=1
            print('Code[',code,']','Total[',index,'] [',i,'/',len(self.codeNameCoast),'] (Volume)')
    
    def addForeign(self):
        self.setProperties(self.ForeignerDB,self.ForeignerTable)
        self.addDateColumn()
        try:
            self.codeNameCoast
        except:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        
        i=0
        for index,code in enumerate(self.codeNameCoast):
            
            data = YGGetWebData.getForeignerAndCompanyPureBuy(str(code),self.start_date_Foreign)
            for index in range(len(data)):
                try:
                    Date = str(data['DateTime'][index]).split(' ')
                    Date = Date[0]
                    Foreign= data['Foreign'][index]
                    
                    query = "update "+self.tableName+" set '"+Date+"' = "+str(Foreign)+" where StockCode='"+str(code)+"';"
                    self.cursor.execute(query)
                except Exception : 
                    self.tracebackLog()
#                     self.PrintException()
                    continue
                
                self.commit()
            i+=1
            print('Code[',code,']','Total[',index,'] [',i,'/',len(self.codeNameCoast),'] (Foreign)')
    
    def addCompany(self):
        self.setProperties(self.ComapanyDB,self.CompanyTable)
        self.addDateColumn()
        try:
            self.codeNameCoast
        except:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        i=0
        for index,code in enumerate(self.codeNameCoast):
            
            data = YGGetWebData.getForeignerAndCompanyPureBuy(str(code),self.start_date_Company)
            for index in range(len(data)):
                try:
                    Date = str(data['DateTime'][index]).split(' ')
                    Date = Date[0]
                    Company= data['Company'][index]
                    
                    query = "update "+self.tableName+" set '"+Date+"' = "+str(Company)+" where StockCode='"+str(code)+"';"
                    self.cursor.execute(query)
                except Exception : 
                    self.tracebackLog()
#                     self.PrintException()
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