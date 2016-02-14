# -*- coding: utf-8 -*-
import sqlite3
import sys
import DBMake

class BuyListDB(DBMake.dbm2):

    def setBuyListDB(self,dbName=""):

        if dbName=="":
            self.BuydbName="kosdaqDashin_List_"
        else :
            self.BuydbName=dbName


        self.BuydbName = self.setDBName(self.BuydbName)
        self.Buydb_cursor = self.BuydbName.cursor()
        self.createTable()
        query = 'alter table kosdaq add BuySell TEXT NOT NULL DEFAULT "N"'

        try:
            self.Buydb_cursor.execute(query)
        except :
            self.PrintException()

    def getSelectDB(self,dbName=""):
        if dbName=="":
            selectDB="kosdaqDashin_"
        else:
            selectDB=dbName
        self.selectDB=super().getSelectDB(selectDB)
        
        return self.selectDB
    
    def getSelectQuery(self,Time=""):
        '''set SimulatorTime if not,get the current Time'''
        
        count = 5
        self.tocount = 1
        
        if Time=="":
            Time = int(self.getTimeSource())
            
        Time=int(Time)
        currTime = self.TimeFormat(Time)
        beforeTime = self.TimeFormat(currTime-1)
        
        
        self.whereQuery = 'select StockCode,StockName from kosdaq where "' + \
            str(beforeTime) + '"<"' + str(currTime) + '"'
            
        self.getSelectQuery_proc(count, beforeTime)

        
        

        return self.whereQuery

    def excuteQuery(self,query):
        cursor = self.selectDB.cursor()
        cursor.execute(query)
#         print(cursor.fetchall())
        
#         print(self.selectDB.cursor().execute)
#         print(self.selectDB.cursor().fetchall())
        self.buylist = cursor.fetchall()
        
        return  self.buylist 

    def printBuyList(self):
        
        for code in self.buylist:
            print(code[0], code[1])
        print('end')


    def insertQueryUpdate(self, code, Time, name):

        self.Buydb_cursor = self.BuydbName.cursor()
        print(self.Buydb_cursor)
        try:
            InsertQuery = 'insert into kosdaq (StockCode,StockName,"' + \
            str(Time) + '",BuySell) values(' + str(code) + ',"' + str(name) + '",302,"Y")'
            self.InsertDB_cursor.execute(InsertQuery)
            print('inserted')
        except:
            InsertQuery = 'update kosdaq set "' + \
                str(Time) + '"="BUY", BuySell="Y" where StockCode ="' + \
                str(code) + '"'
            self.Buydb_cursor.execute(InsertQuery)
            print('updated')

        self.BuydbName.commit()


    def getSelectQuery_proc(self, count, Time):
        '''
        get the update query set
        '''

        if self.tocount == count:
            self.tocount = 0
            print('end')
            print(self.whereQuery)
            return self.whereQuery

        else:  
            
            Time=self.TimeFormat(Time)
            currTime = self.TimeFormat(Time)
            beforeTime = self.TimeFormat(currTime-1)
 
            self.whereQuery = self.whereQuery + ' and "' + \
                str(beforeTime) + '"<"' + str(currTime) + '"'

            self.tocount += 1
            self.getSelectQuery_proc(count, beforeTime)
            
    def TimeFormat(self,Time):
        Time=str(Time)
        if len(Time)<4:
            Hour = Time[:1]
            Min = Time[1:]
        elif len(Time)==4:
            Hour = Time[:2]
            Min = Time[2:]
            
        if int(Min)>=60:
            Hour = int(Hour)
            Min ='59'
                
        Time = str(Hour)+Min
        Time=int(Time)
        return Time
    
    def printInfo(self):
        print('buylist DB : '+str(self.BuydbName))
        print('select DB : '+ str(self.selectDB))

if __name__ == '__main__':

    dbmake = BuyListDB()
    
#     dbmake.setBuyListDB()
#     dbmake.getSelectQuery('1003')
    dbmake.getSelectDB()
#     dbmake.printInfo()
    dd = dbmake.excuteQuery(dbmake.getSelectQuery('1414'))
    print(dd)