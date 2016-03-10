# -*- coding: utf-8 -*-

import sqlite3
import sys,os
from _sqlite3 import OperationalError
# sys.path.append('../')
sys.path.append('../Data')
import YGGetWebData
import time
import btsForDashin
import linecache
import MakeDB

class BuyListDB(MakeDB.DBMake):
    
    def setProperties(self,dbName="",tableName=""):
        DB= '../../Sqlite3/BuyList.db'
        if dbName !="":
            DbName=dbName
        Table='BuyList'
        if tableName !="":
            Table=tableName
            
        super().setProperties(DB,Table)
    
    def createDatabase(self,dbName,table):
        super().createDatabase(dbName,table)
        sql = "alter table "+self.tableName+" add BUYSELL TEXT default N;";
        try:
            for i in range(9,15):
                for j in range(0,60):
                    if j<10:
                        j=str(j)
                        j=j[:0]+str('0')+j[0:]
                    self.cursor.execute("alter table "+self.tableName+" add '"+str(i)+str(j)+"' INTEGER")
            self.cursor.execute(sql)
            self.conn.commit()  
        except :
            self.PrintException()
            
    def insertGold(self,code):
        
        sql = 'insert into '+self.tableName+' (StockCode) values("'+str(code)+'");'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            
        except OperationalError:
            
            self.createDatabase('../../Sqlite3/BuyList.db','BuyList')
            self.cursor.execute(sql)
            self.conn.commit()
        
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
    bld.setProperties()
#     bld.insertGold('041140')
#     bld.togleCode('127710')
    dd = bld.getCode()
    