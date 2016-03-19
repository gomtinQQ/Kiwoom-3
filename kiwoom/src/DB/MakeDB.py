# -*- coding: utf-8 -*-
import multiprocessing as mp
import sqlite3
import configparser
import sys,os
sys.path.append('../')
sys.path.append('../Data')
import YGGetWebData
import time,datetime
import btsForDashin
import linecache
import traceback
import logging
from logging.handlers import RotatingFileHandler 

class DBMake():
    
    
    lock = mp.Lock()
    querylock = mp.Lock()
    config = configparser.ConfigParser()
    config.read("../config/config.ini")
    
    
#     def initConfigSet(self):
    def __init__(self):
        
        self.ForeignerDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB") 
        self.ComapanyDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB")
        self.VolumeDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB")
        self.ClosePriceDB = self.config.get("DATABASE","ClosePriceDB")
        self.BuyListDB = self.config.get("DATABASE","BuyListDB")
        today = datetime.datetime.today().date()
        oneDay = datetime.timedelta(days=1)
        YESTERDAY= str( today - oneDay)
        
        
        self.ForeignerDB = self.ForeignerDB+".db"
        self.ComapanyDB = self.ComapanyDB+".db"
        self.VolumeDB = self.VolumeDB+".db"
        self.ClosePriceDB = self.ClosePriceDB+".db"
        self.BuyListDB =self.BuyListDB+YESTERDAY+".db" 
        
        
        self.ForeignerTable = self.config.get("DATABASE","ForeignTable")
        self.CompanyTable = self.config.get("DATABASE","CompanyTable")
        self.VolumeTable = self.config.get("DATABASE","VolumeTable")
        self.ClosePriceTable = self.config.get("DATABASE","ClosePriceDBTable")
        
        self.BuyListTable = self.config.get("DATABASE","BuyListTable")
        self.BuyListVolumeRotateTable = self.config.get("DATABASE","BuyListVolumeRotateTable")
        self.BuyListRelativeTable = self.config.get("DATABASE","BuyListRelativeTable")
        
        
        
        
        self.start_date_closePrice = self.config.get("DATE","ClosePrice.StartDATE")
        self.start_date_Volume = self.config.get("DATE","Volume.StartDATE")
        self.start_date_Foreign= self.config.get("DATE","FOREIGN.StartDATE")
        self.start_date_Company= self.config.get("DATE","Company.StartDATE")
        
        self.fName = str(self.config.get("LOG","filename"))+'_'+str(datetime.datetime.today().date())
        self.loglevel = self.config.get("LOG","loglevel")
        self.fileSize = self.config.get("LOG","FILESIZE")
        
        for name,value in self.config.items():
            print('==========================',name,'==========================')
            for items in self.config.items(name):
                print('==',items[0],'=',items[1])
        

    def setLog(self):
        
#         logging.basicConfig(filename=self.fName,level = self.loglevel)
        
        self.logger = logging.getLogger("YGLogger")
        fomatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s")
        fileHandler = logging.FileHandler(self.fName)
        fileHandler = RotatingFileHandler(filename=self.fName,maxBytes=int(self.fileSize)*1024*1024)
        fileHandler.setFormatter(fomatter)
        
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(self.loglevel)
         
        self.logger.debug('*****************************DBMake Logging Start*****************************')
        
    def debug(self,msg):
        self.logger.debug(msg)
    
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
                    self.PrintException()
                    continue
                
                self.commit()
            i+=1
            print('code[',code,'] Total[',index,'] (',i,'/',len(self.codeNameCoast),')')
#     def addTodayClosePrice(self):
#         '''오늘날짜 까지를 세팅한다.'''
#         if self.codeNameCoast ==None:
#             self.setCodeNameCoast()
#         for code in self.codeNameCoast:
#             
#             data = YGGetWebData.getStockPriceData(str(code),date)
        
        
            
    def addDateColumn(self):
        
        '''날짜칼럼 삽입.'''
        try:
            self.codeNameCoast
        except AttributeError:
            self.setCodeNameCoast()
            
        if self.tableName ==None:
            raise ("Table Name not Assigned")
        
        code='005930'   #삼성전자의 데이터를갖고 날짜를 가져온다.
        data = YGGetWebData.getStockPriceData(str(code),self.start_date_closePrice)
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
            
            data = YGGetWebData.getStockPriceData(str(code),self.start_date_Volume)
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
            
            data = YGGetWebData.getForeignerAndCompanyPureBuy(str(code),self.start_date_Foreign)
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
            
            data = YGGetWebData.getForeignerAndCompanyPureBuy(str(code),self.start_date_Company)
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