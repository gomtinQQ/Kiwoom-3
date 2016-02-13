# -*- coding: utf-8 -*-
import sqlite3
import sys
import DBMake

class BuyListDB(DBMake.dbm2):

    def setBuyListDB(self,day):

        self.BuydbName="kosdaqDashin_List_"+str(day)



        self.BuydbName = self.setDBName(self.BuydbName)
        self.BuydbName_cursor = self.BuydbName.cursor()

        query = 'alter table kosdaq add BuySell TEXT NOT NULL DEFAULT "N"'

        try:
            self.BuydbName_cursor.execute(query)
        except :
            print(sys.exc_info())

    def getSelectDB(self):
        day = self.getDay()
        self.setDBProperties("D:\\OneDrive\\python\\sqlite3\\kosdaq.db")
        self.selectDB = self.getConnection()

    def selectQuery(self):

        count = 5
        self.tocount = 1

        Time = int(self.getTimeSource())
#         Time = int('920')
        self.whereQuery = 'select StockCode,StockName from kosdaq where "' + \
            str(Time - 1) + '"<"' + str(Time) + '"'
        self.selectQueryUpdate(count, Time)
#         print(self.whereQuery)
        self.BuydbName_cursor.execute(self.whereQuery)

#         print(self.selectDB_cursor.fetchall())
        self.buylist = self.BuydbName_cursor.fetchall()
        self.whereQuery = ""

        self.printBuyList()
        

    def printBuyList(self):
        for code in self.buylist:
            print(code[0], code[1])



    def insertQueryUpdate(self, code, Time, name):

        self.InsertDB_cursor = self.InsertDB.cursor()
        print(self.InsertDB_cursor)
        try:
            InsertQuery = 'insert into kosdaq (StockCode,StockName,"' + str(
                Time) + '",BuySell) values(' + str(code) + ',"' + str(name) + '",302,"Y")'
            self.InsertDB_cursor.execute(InsertQuery)
            print('insert')
        except:
            InsertQuery = 'update kosdaq set "' + \
                str(Time) + '"="BUY", BuySell="Y" where StockCode ="' + \
                str(code) + '"'
            self.InsertDB_cursor.execute(InsertQuery)
            print('update')

        self.InsertDB.commit()


    def selectQueryUpdate(self, count, Time):
        '''
        update where절 쿼리를 가져온다.
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
            print(self.tocount, count)
            self.selectQueryUpdate(count, Time)

if __name__ == '__main__':

    dbmake = BuyListDB()
#     dbmake.setInsertDBName()
#     dbmake.insertQueryUpdate('000660','901','하이')
    dbmake.setBuyListDB(dbmake.getDay())
    dbmake.createTable()
    # dbmake.getSelectDB()
    # dbmake.initParse()

#     dbmake.setInsertDBName()
#     dbmake.setCodeNameCoast('9:02')
#     dbmake.createTable(dbmake.getDBName())

#     dbmake.updateName()
    dbmake.selectQuery()