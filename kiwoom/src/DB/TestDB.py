# -*- coding: utf-8 -*-
import sqlite3
import sys,os
import random
sys.path.append('../')
sys.path.append('../Data')
import YGGetWebData
import time,datetime
import btsForDashin
import linecache
import MakeDB
import multiprocessing as mp

class TestDB(MakeDB.DBMake):
    def TestSet(self,connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
    

    def selectQuery(self):
        code = 227950
        sql ="select * from "+str(self.BuyListTable)+" where StockCode = "+str(code)
        
        sql =str(sql)
        
        Connection = sqlite3.connect(self.BuyListDB)
#         self.cursor.execute(sql)
#         dd = self.cursor.fetchall()
        cursor = Connection.cursor()
        for i in range(1000):
            cursor.execute(sql)
            dd = cursor.fetchall()
            time.sleep(0.5)
        
            print(dd)

    def autoSet(self):
        autoData = 0
        code = 227950
        Connection = sqlite3.connect(self.BuyListDB)
        cursor = Connection.cursor()
        standMinute = datetime.datetime.today().minute
        for i in range(1000):
            
            autoData +=10
            
            time.sleep(0.5)
            sql = "update "+str(self.BuyListTable)+" set '900' = '"+str(autoData)+"' where StockCode = "+str(code)
            print("BEFORE IF",standMinute,datetime.datetime.today().minute)
            if standMinute !=datetime.datetime.today().minute:
                print("AFTER IF",standMinute,datetime.datetime.today().minute)
                standMinute = datetime.datetime.today().minute
                cursor.execute(sql)
                Connection.commit()
                
                
        
if __name__ == '__main__':
    td = TestDB()
#     tt = sqlite3.connect(td.BuyListDB)
    ConnArray=[]
    for con in range(10):
        ConnArray.append(sqlite3.connect(td.BuyListDB))
        
    td.TestSet(ConnArray.pop())
#     td.selectQuery()
    dd = mp.Process(name="autoSet",target=td.autoSet)
    dd.start()
    
    ff = mp.Process(name="select",target=td.selectQuery)
    ff.start()
    