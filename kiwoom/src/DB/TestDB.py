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
    

    def selectQuery(self,code):
#         code = 227950
        sql ="select * from "+str(self.BuyListTable)+" where StockCode = "+str(code)
        
        sql =str(sql)
        
        Connection = sqlite3.connect(self.BuyListDBToday)
#         self.cursor.execute(sql)
#         dd = self.cursor.fetchall()
        cursor = Connection.cursor()
        for i in range(1000):
            cursor.execute(sql)
            dd = cursor.fetchall()
            time.sleep(0.5)
        
            print(dd)

    def autoSet(self,code):
        autoData = 0
#         code = 227950
        Connection = sqlite3.connect(self.BuyListDBToday)
        cursor = Connection.cursor()
        standMinute = datetime.datetime.today().minute
        
        timeVal={}
        for i in range(1000):
            
            autoData +=10
            
            time.sleep(0.5)
            print("BEFORE IF",standMinute,datetime.datetime.today().minute)
            
#             dataset[0] = standMinute
            timeVal['few'] = '9'+str(standMinute),autoData
            if standMinute !=datetime.datetime.today().minute:
                print(timeVal['few'][0])
                print(timeVal['few'][1])
                tt= str(timeVal['few'][0])
                
                sql = "update "+str(self.BuyListTable)+" set '"+tt+"' = '"+str(timeVal['few'][1])+"' where StockCode = "+str(code)
                
                print("AFTER IF",standMinute,datetime.datetime.today().minute)
                standMinute = datetime.datetime.today().minute
                cursor.execute(sql)
                Connection.commit()
                timeVal['few']=None
#                 dataset.clear()
                
if __name__ == '__main__':
    td = TestDB()
#     tt = sqlite3.connect(td.BuyListDB)
    ConnArray=[]
    for con in range(10):
        ConnArray.append(sqlite3.connect(td.BuyListDB))
        
    td.TestSet(ConnArray.pop())
#     td.selectQuery()
    code = str(227950)
    dd = mp.Process(name="autoSet",target=td.autoSet, args=(code,))
    dd.start()
    
    ff = mp.Process(name="select",target=td.selectQuery, args=(code,))
    ff.start()
    