# -*- coding: utf-8 -*-

import sqlite3
import sys,os
sys.path.append('../')
sys.path.append('../Data')
import YGGetWebData
import time
import btsForDashin
import linecache
import MakeDB

class closePriceMake(MakeDB.DBMake):
        

    def createDatabase(self,DBName):
        '''형식에 맞는 테이블 생성.'''
        super().createDatabase(DBName,'ClosePrice')
#         self.dbName=DBName
#         self.conn = sqlite3.connect(self.dbName)
#         self.cursor = self.conn.cursor()
#         
#         _start=time.time()
#         try:
#             self.cursor.execute('CREATE TABLE `ClosePrice` \
#             ( \
#             `StockCode`  INTEGER NOT NULL UNIQUE,\
#             `StockName`  INTEGER NOT NULL UNIQUE,\
#             PRIMARY KEY(StockCode,StockName)\
#             );')
#             
#             print("table created ["+str(time.time()-_start)+"]")
#         except :
#             self.PrintException()
#         self.conn.commit()
    
#     def addCodeNameData(self):
#         '''테이블 생성후 코드와,이름 삽입'''
#         
#         self.dbName='../../Sqlite3/ClosePriceDB.db'
#         self.conn = sqlite3.connect(self.dbName)
#         self.cursor = self.conn.cursor()
#         
#         bfd = btsForDashin.btsForReal()
#         self.codeNameCoast = bfd.UrlParsing()
#         for code in self.codeNameCoast:
#             for Name in self.codeNameCoast[code]:
#                 query = 'Insert into ClosePrice\
#                 (StockCode,StockName) \
#                 values ("'+str(code)+'","'+str(Name)+'");'
#                 self.cursor.execute(query)
#         self.conn.commit()
    
#     def addDatePrice(self):
#         '''날짜에 맞게  종가를 대입한다.'''
        
#         self.dbName='../../Sqlite3/ClosePriceDB.db'
#         self.conn = sqlite3.connect(self.dbName)
#         self.cursor = self.conn.cursor()
#         bfd = btsForDashin.btsForReal()
#         self.codeNameCoast = bfd.UrlParsing()
#         
#         for index,code in enumerate(self.codeNameCoast):
#             
#             data = YGGetWebData.getStockPriceData(str(code),'2014-09-1')
#             for index in range(len(data)):
#                 try:
# #                     print(code)
#                     Date = str(data['DateIndex'][index]).replace("'","")
#                     Price= data['close'][index]
#                     
#                     query = "update ClosePrice set "+Date+" = "+str(Price)+" where StockCode='"+str(code)+"';"
#                     self.cursor.execute(query)
#                 except Exception : 
#                     self.PrintException()
#                     continue
#                 
#                 self.conn.commit()
#             print(code,index,len(self.codeNameCoast))
            
#     def addDateColumn(self):
#         
#         '''날짜칼럼 삽입.'''
#         self.dbName='../../Sqlite3/ClosePriceDB.db'
#         self.conn = sqlite3.connect(self.dbName)
#         self.cursor = self.conn.cursor()
#         bfd = btsForDashin.btsForReal()
#         self.codeNameCoast = bfd.UrlParsing()
#         code='126700'
#         data = YGGetWebData.getStockPriceData(str(code),'2014-09-1')
#         
#         for index in range(len(self.codeNameCoast)):
#             try:
#                 Date = str(data['DateIndex'][index]).replace("'","")
#                 print(Date)
#                 query1 = "alter table ClosePrice add "+str(Date)+" INTEGER;";
#                 self.cursor.execute(query1)
#             except Exception:
#                 continue
#         self.conn.commit
    def initAndCreateDefaultDB(self):
        self.createDatabase('../../Sqlite3/ClosePriceDB.db')
        self.addDateColumn()
        self.addCodeNameData()
        self.addDatePrice()
        
        
if __name__ == '__main__':
    cp =closePriceMake()
    cp.initAndCreateDefaultDB()