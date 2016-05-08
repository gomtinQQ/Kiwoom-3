# -*- coding: utf-8 -*-

import sqlite3
import sys,os
from _sqlite3 import OperationalError
# sys.path.append('../')
sys.path.append('../Data')
import time,datetime
import traceback
from SRC.Database import MakeDB

class BuyListDB(MakeDB.DBMake):
    
    def setProperties(self,dbName="",tableName=""):
#         DB= '../../Sqlite3/'+self.BuyListDB
#         if dbName !="":
#             DbName=dbName
#         Table='BuyList'
#         if tableName !="":
#             Table=tableName
            
        super().setProperties(dbName,tableName)
    
    def createDatabase(self,dbName,table):
        super().createDatabase(dbName,table)
        sql = "alter table "+table+" add BUYSELL TEXT default N;";
        try:
            _start=time.time()
            for i in range(9,15):
                for j in range(0,60):
                    if j<10:
                        j=str(j)
                        j=j[:0]+str('0')+j[0:]
                    self.cursor.execute("alter table "+table+" add '"+str(i)+str(j)+"' INTEGER")
            self.cursor.execute(sql)
            self.cursor.execute("alter table "+table+" add BSTime Text ")
            self.conn.commit()  
            print("DataColumn Added ["+str(time.time()-_start)+"]")
        except :
#             self.PrintException()
            self.tracebackLog()
            
                    
    def createDatabase2(self,dbName,table,StockCodeList):
        super().createDatabase2(dbName,table)
        try:
            _start=time.time()
            
            for i in range(len(StockCodeList)):
                
                self.cursor.execute("alter table "+table+" add '"+StockCodeList[i][0]+"' INTEGER")
            self.conn.commit()  
            print("DataColumn Added ["+str(time.time()-_start)+"]")
        except :
#             self.PrintException()
            self.tracebackLog()
        self.insertStockTime(table)
        
    def insertStockTime(self,table):
        
        for i in range(9,15):
            for j in range(0,60):
                if j<10:
                    j=str(j)
                    j=j[:0]+str('0')+j[0:]
                self.cursor.execute("insert into "+table+" (StockTIME) values ('"+str(i)+str(j)+"')")   #전체 다팔고 시작하기위해 S로 시작함.
        self.conn.commit()  
        

    def createDefaultDB(self):
        
        self.createDatabase(self.BuyListDBToday, self.BuyListTable)
        self.createDatabase(self.BuyListDBToday ,self.BuyListVolumeRotateTable)
        self.createDatabase(self.BuyListDBToday ,self.BuyListRelativeTable)
        
        
    def createDefaultDB2(self,StockCodeList):
        
        self.createDatabase(self.BuyListDBToday, self.BuyListTable)
        self.createDatabase2(self.BuyListDBToday ,self.BuyListVolumeRotateTable,StockCodeList)
        self.createDatabase2(self.BuyListDBToday ,self.BuyListRelativeTable,StockCodeList)
            
#     def insertGold(self,code):
#         
#         try:
#             sql = 'insert into '+self.BuyListTable+' (StockCode) values("'+str(code)+'");'
#             self.cursor.execute(sql)
#             sql = 'insert into '+self.BuyListVolumeRotateTable+' (StockCode) values("'+str(code)+'");'
#             self.cursor.execute(sql)
#             sql = 'insert into '+self.BuyListRelativeTable+' (StockCode) values("'+str(code)+'");'
#             self.cursor.execute(sql)
#             
#             self.conn.commit()
#             
#         except OperationalError:
#             
#             print(traceback.print_exc())
        
    def togleCode(self,code):
        sesql = 'select BUYSELL from '+self.tableName+' where StockCode = '+code
        dd = self.cursor.execute(sesql)
        GUBUN = str(self.cursor.fetchall()[0][0])
        if GUBUN=='N':
            GUBUN='Y'
        elif GUBUN=='Y':
            GUBUN='N'
        sql = 'update '+self.tableName+' set BUYSELL ="'+GUBUN+'" where StockCode = "'+code+'";'
        self.cursor.execute(sql)
        self.conn.commit()
        
    

if __name__ == '__main__':
    bld = BuyListDB()
#     bld.createDatabase('../../Sqlite3/BuyList.db','BuyList')
#     bld.setProperties()
    today = datetime.datetime.today().date()
    oneDay = datetime.timedelta(days=1)
        
    YESTERDAY= str( today - oneDay)
    bld.createDatabase('../../Sqlite3/BuyList'+YESTERDAY+'.db',bld.BuyListVolumeRotateTable)
    bld.addCodeNameData()
    bld.createDatabase('../../Sqlite3/BuyList'+YESTERDAY+'.db',bld.BuyListRelativeTable)
    bld.addCodeNameData()
#     bld.insertGold('041140')
#     bld.togleCode('127710')
    dd = bld.getCode()
    