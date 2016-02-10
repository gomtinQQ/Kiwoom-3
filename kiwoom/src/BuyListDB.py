# -*- coding: utf-8 -*-
import sqlite3

import sys
import DBMake

class BuyListDB(DBMake.dbm2):
    
    def setInsertDBName(self):
        
        day=self.getDay()
        self.setDBProperties("D:\\OneDrive\\python\\sqlite3\\kosdaqDashin_buyList_"+str(day)+".db")
        self.InsertDB =self.getConnection() 
        self.InsertDB_cursor = self.InsertDB.cursor()
        
        query = 'alter table kosdaq add BuySell TEXT NOT NULL DEFAULT "N"'
        try:
            self.InsertDB_cursor.execute(query)
        except :
            print(sys.exc_info())
        
        
    def getSelectDB(self):
        day= self.getDay()
        self.setDBProperties("D:\\OneDrive\\python\\sqlite3\\kosdaq.db")
        self.selectDB = self.getConnection()
    
    def selectQuery(self):
        self.selectDB_cursor = self.selectDB.cursor()
        count =4
        self.tocount=1
        
        Time = int(self.getTimeSource())
#         Time = int('920')
        self.whereQuery= 'select StockCode,StockName from kosdaq where "'+str(Time-1)+'"<"'+str(Time)+'"'
        self.selectQueryUpdate(count,Time)
#         print(self.whereQuery)
        self.selectDB_cursor.execute(self.whereQuery)
        
#         print(self.selectDB_cursor.fetchall())
        self.buylist = self.selectDB_cursor.fetchall()
        self.whereQuery=""
        
        self.printBuyList()
        
    def printBuyList(self):
        for code in self.buylist:
            print(code[0],code[1])
            
    def insertQueryUpdate(self,code,Time,name):
        
        self.InsertDB_cursor=self.InsertDB.cursor()
        print(self.InsertDB_cursor)
        try:
            InsertQuery = 'insert into kosdaq (StockCode,StockName,"'+str(Time)+'",BuySell) values('+str(code)+',"'+str(name)+'",302,"Y")'
            self.InsertDB_cursor.execute(InsertQuery)
            print('insert')
        except :
            InsertQuery = 'update kosdaq set "'+str(Time)+'"="BUY", BuySell="Y" where StockCode ="'+str(code)+'"'
            self.InsertDB_cursor.execute(InsertQuery)
            print('update')
        
        self.InsertDB.commit()
    
    def selectQueryUpdate(self,count,Time):
        
        if self.tocount==count:
            self.tocount=0
            print('end')
            print(self.whereQuery)
            return self.whereQuery
        
        else:
            
            Time=Time-1
            self.whereQuery =self.whereQuery+' and "'+str(Time-1)+'"<"'+str(Time)+'"'

            self.tocount+=1
            print(self.tocount, count)
            self.selectQueryUpdate(count,Time)

if __name__ == '__main__':

    dbmake = BuyListDB()
#     dbmake.setInsertDBName()
#     dbmake.insertQueryUpdate('000660','901','하이')
    dbmake.getSelectDB()
#     dbmake.initParse()
#     dbmake.setInsertDBName()
#     dbmake.setCodeNameCoast('9:02')
#     dbmake.createTable(dbmake.getDBName())
    
#     dbmake.updateName()
    dbmake.selectQuery()