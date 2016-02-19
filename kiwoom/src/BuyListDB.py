# -*- coding: utf-8 -*-
import sqlite3
import sys
import DBMake
import datetime

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
    
    def getSelectQuery(self,Time="",count="",interval=""):
        '''set SimulatorTime if not,get the current Time'''
        
        
        if count=="":
            count=5
        count=int(count)
        
        if interval=="":
            interval=1
        interval=int(interval)
            
        self.tocount = 1
        
        if Time=="":
            Time = int(self.getTimeSource())
            
        Time=int(Time)
        currTime = self.TimeFormat(Time)
        beforeTime = self.calTime(currTime,interval)
#         print('beforeTime'+str(beforeTime),interval,currTime)
        
        self.whereQuery = 'select StockCode,StockName from kosdaq where "' + \
            str(beforeTime) + '"<"' + str(currTime) + '"'
            
        self.getSelectQuery_proc(count, beforeTime ,interval)

        
        

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
#         print('end')


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


    def getSelectQuery_proc(self, count, Time,interval):
        '''
        get the update query set
        '''

        if self.tocount == count:
            self.tocount = 0
            print(self.whereQuery)
            return self.whereQuery

        else:  

            Time=self.TimeFormat(Time)
            currTime = self.TimeFormat(Time)
            beforeTime =self.calTime(currTime, interval)
 
            self.whereQuery = self.whereQuery + ' and "' + \
                str(beforeTime) + '"<"' + str(currTime) + '"'

            self.tocount += 1
            self.getSelectQuery_proc(count, beforeTime,interval)
            
    def TimeFormat(self,Time):
        Time=str(Time)
        if len(Time)<4:
            Hour = Time[:1]
            Min = Time[1:]
        elif len(Time)==4:
            Hour = Time[:2]
            Min = Time[2:]
        
        if Min>='60':
            Min='0'
            Hour=str(int(Hour)+1)
        
#         print(Min)
        Time = datetime.time(int(Hour),int(Min))

        
        minute = Time.minute
        if Time.minute <10:
            minute=str(Time.minute)
            minute='0'+minute
        Time = str(Time.hour)+str(minute) 
        
        Time=int(Time)
        return Time
    
    def calTime(self,Time,Interval):
        
        Time=str(Time)
        if len(Time)<4:
            Hour = Time[:1]
            Min = Time[1:]
        elif len(Time)==4:
            Hour = Time[:2]
            Min = Time[2:]
        
        t1= datetime.timedelta(hours=int(Hour),minutes=int(Min))
        t2= datetime.timedelta(minutes=Interval)
        Time = t1-t2
        Time=str(Time)

        tt= Time.split(":")
        hour = tt[0]
        min = tt[1]
        seconds = tt[2]
        Time = str(hour)+str(min)




        return Time
    
    def printInfo(self):
        print('buylist DB : '+str(self.BuydbName))
        print('select DB : '+ str(self.selectDB))

if __name__ == '__main__':

    dbmake = BuyListDB()
    
    dbmake.getSelectDB()
    
#     for Time in range(900,1459):
#         Time = dbmake.TimeFormat(Time)
    for i in range(9,15):
        for j in range(0,60):
            if j<10:
                j=str(j)
                j=j[:0]+str('0')+j[0:]
            Time=str(i)+str(j)
            dd = dbmake.excuteQuery(dbmake.getSelectQuery(str(Time),'10',3))
            if ( len(dd) > 0 ):
                for code in dd:
                    print(str(code)+' '+str(Time))
#     dd = dbmake.getSelectQuery('1005','5','5')
#     print(dd)
#     dd = dbmake.excuteQuery(dbmake.getSelectQuery('1202','5',5))
    
    
#     for code in dd:
#         print(code)
#     print('total : '+str(len(dd)))