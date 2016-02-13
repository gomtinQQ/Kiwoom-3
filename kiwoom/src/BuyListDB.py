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
            selectDB="dbName"
        selectDB=super().getSelectDB(selectDB)
        
        return selectDB
    
    def selectQuery(self,Time=""):
        '''set SimulatorTime if not,get the current Time'''
        
        count = 5
        self.tocount = 1
        Time=int(Time)
        
        if Time=="":
            Time = int(self.getTimeSource())
            
        
        self.whereQuery = 'select StockCode,StockName from kosdaq where "' + \
            str(Time - 1) + '"<"' + str(Time) + '"'
        self.selectQueryUpdate(count, Time)

        self.getSelectDB().cursor().execute(self.whereQuery)


        self.buylist = self.getSelectDB().cursor().fetchall()
        self.whereQuery = ""

        self.printBuyList()
        

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


    def selectQueryUpdate(self, count, Time):
        '''
        get the update query set
        '''

        if self.tocount == count:
            self.tocount = 0
            print('end')
            print(self.whereQuery)
            return self.whereQuery

        else:  
            Time = Time - 1
            self.whereQuery = self.whereQuery + ' and "' + \
                str(Time - 1) + '"<"' + str(Time) + '"'

            self.tocount += 1
            self.selectQueryUpdate(count, Time)

if __name__ == '__main__':

    dbmake = BuyListDB()
    
    dbmake.setBuyListDB()
    

    dbmake.selectQuery(902)