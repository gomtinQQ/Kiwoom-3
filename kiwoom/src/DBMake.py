# -*- coding: utf-8 -*-

import sqlite3
import ExcelMake
import bts
import time
import multiprocessing as mp
import DBMake
import linecache
import btsForDashin 
from _sqlite3 import OperationalError
import sys,os

class dbm2(mp.Process):
    
    def __init__(self,dbname=""):
        super(dbm2, self).__init__()
        
    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

        
    def getConnection(self):
        return self.conn
        
    def getCursor(self):
        return self.cursor
        
#     def updateCode(self,code,TimePerDict,cursor):
#         _start = time.time()
# 
#         for tp in TimePerDict.keys():
#             try:
#                 rtime = tp
#                 if tp[0]==9 :
#                     tp=tp[0:]+'0'+tp[:0]
#                 rec=tp[:2]+tp[3:]
#                 if tp[0]!='c':
#                     rec=int(rec)
#                 cursor.execute('update kosdaq set "'+str(rec)+'"="'+str(TimePerDict[rtime])+'" where StockCode='+str(code))
#             except OperationalError as err:
#                 continue
#             except Exception as er:
#                 print("Exception ! "+str(sys.exc_info()))
#                 continue
#         print(str(code)+' setting ['+str(time.time()-_start)+']')
#         self.commit()

    def createTable(self):
        '''형식에 맞는 테이블 생성.'''
#         self.dbName=dbName
#         self.conn = sqlite3.connect(self.dbName)
#         self.cursor = self.conn.cursor()
        
        _start=time.time()    
        try:
            self.cursor.execute('CREATE TABLE `kosdaq` (`StockCode`    \
            INTEGER NOT NULL UNIQUE,`StockName`    \
            INTEGER NOT NULL UNIQUE,PRIMARY KEY(StockCode,StockName));')
            
            for i in range(9,15):
                for j in range(0,60):
                    if j<10:
                        j=str(j)
                        j=j[:0]+str('0')+j[0:]
                    self.cursor.execute("alter table kosdaq add '"+str(i)+str(j)+"' REAL")
            print("table created ["+str(time.time()-_start)+"]")
        except :
            self.PrintException()
        self.commit()
        
    def setDBProperties(self,dbName):
        
        if not os.path.exists("../Sqlite3"):
            os.mkdir("../Sqlite3")
        if not os.path.exists("../Sqlite3\\DAESHIN\\"):
            os.mkdir("../Sqlite3\\DAESHIN\\")
        if not os.path.exists("../Sqlite3\\DAESHIN\\"+str(self.getDay())):
            os.mkdir("../Sqlite3\\DAESHIN\\"+str(self.getDay()))
            
        self.dbName=dbName
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        return self.conn

    def setDBName(self,dbName):
        '''make Each Folder and Makde Database File'''
        '''Auto Set DBProperties'''
        
        path="../Sqlite3\\DAESHIN\\"+str(self.getDay())+"\\"
        dbName=dbName+str(self.getDay())+".db"
        self.dbName=path+dbName
        conn = self.setDBProperties(self.dbName)
        return conn
        
    def getSelectDB(self,dbName):
        
        '''return Connection'''
        
        path="../Sqlite3\\DAESHIN\\"+str(self.getDay())+"\\"
        dbName=dbName+str(self.getDay())+".db"
        dbName=path+dbName
        
        if os.path.exists(dbName):
            return sqlite3.connect(dbName)
        else:
            raise RuntimeError('db is not exists make DB!')
        
    def updateCode(self,Code,Time,coast):
        
        '''코드,시간,가격적으면 DB에 update'''
        Time = str(Time)
#         try:
#             Time=Time[:Time.index(":")]+Time[Time.index(":")+1:]
#         except ValueError:
#             print(sys.exc_info())
        
            
        print('###'+Time)
        Code=str(Code)
        self.cursor.execute('update kosdaq set "'+Time+'"="'+coast+'" where StockCode='+Code)
        
        
    def dropTable(self,Table):
        
        self.cursor.execute('drop TABLE `kosdaq`')
        
    def setCode(self,code,name):
        _start=time.time()
        try:
            self.cursor.execute('Insert into kosdaq (StockCode,StockName) values("'+code+'","'+name+'")')
        except :
            self.PrintException()
        
        print('['+name+'] setting ['+str(time.time()-_start)+']')



    def getDay(self):
        '''
        get today
        month,day
        ex)0204
        '''

        now = time.localtime()
        mon = now.tm_mon
        day = now.tm_mday

        if int(mon) <10:
            mon = '0'+str(mon)
            mon=str(mon)
        if int(day)<10:
            day = '0'+str(day)
            day = str(day)
        monday = str(mon)+str(day)
        return monday

    def getTime(self):
        
        Time = self.getTimeSource()
        Time = Time[:2]+':'+Time[2:]
        
        return Time
        
    
    def getTimeSource(self):

        '''
        get Time
        ex)903 , 1003, 1102, ...
        '''
        now = time.localtime()
        Hour = now.tm_hour
        Minute=now.tm_min
        
        if int(Minute)<10:
            Minute='0'+str(Minute)
        Time = str(Hour)+str(Minute)
        return Time
        
    def run(self):
        self.conn= sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        
        _start=time.time()
        all = len(self.codelist)
        i=0
        time.sleep(1)
        print(self.name+" is working")
        while (True):
            print('before get')
            try:
                TimePerDict = self.WQueue.get(timeout=5.0)
                print(TimePerDict)
#                 if len(TimePerDict):
#                     print("hi")
#                     time.sleep(1)
#                     continue
                if TimePerDict=='END':
                    print('success~ ['+(time.time()-_start)+']')
                    break
                i+=1
                print('before code')
                
                print('code = '+TimePerDict['code'])
                self.updateCode(TimePerDict['code'],TimePerDict,self.cursor)
                print('code end')
                print('=======================================================['+str(i)+'/'+str(all)+']')
            except Exception as er :
                print("Exception = "+str(sys.exc_info()))
                continue
#         print('hi')
        
        
    def setCodelist(self,codelist):
        self.codelist = codelist
        
    def commit(self):
        self.conn.commit()
        
    def setWQueue(self,WQueue):
        self.WQueue=WQueue
        
    def initParse(self):
        '''대신증권 홈페이지에서 값들을 가져온후 Diction으로 저장'''
        print('parse start')
        self.dbm = DBMake.dbm2()
        bfd = btsForDashin.btsForReal()
        self.codeNameCoast = bfd.UrlParsing()
        
        print('parse end')
    
    def updateName(self):
        print('updateName Start')
        _start=time.time()
        
        for code in self.codeNameCoast:
            for name in self.codeNameCoast[code]:
                self.cursor.execute('update kosdaq set StockName="'+str(name)+'" where StockCode="'+str(code)+'"')
                print('success')
        self.commit()
    
    def setCodeNameCoast(self,Time):
        if self.codeNameCoast == None:
            print('파싱안되서 새로만듦')
            self.initParse()
        
        for code in self.codeNameCoast:
            for name in self.codeNameCoast[code]:
                self.updateCode(code,Time,self.codeNameCoast[code][name])
                

class multi(mp.Process):
    
    def __init__(self):
        super(multi, self).__init__()
#         mp.Process.__init__(self)

    
    def run(self):
        self.bts = bts.mbts()
        while(True):
#             print(self.name+" is working")
            try:
                code = self.RQueue.get()
                if code == 'END':
                    self.RQueue.put('END')
                    self.WQueue.put('END')
                    break

                self.bts.IframeUrlWithCode(code)
                
                tps=self.bts.getTimePerDic()
                self.WQueue.put(tps)
                
            except:
                print('put error :'+str(sys.exc_info()))
                        
    def setting(self,WQueue,RQueue):
        self.WQueue=WQueue
        self.RQueue=RQueue
        
        
    
if __name__ == '__main__':

    sys.setrecursionlimit(1000000) #에러방지위해 뎁스 기본값 세팅
    
    readedExcel = ExcelMake.ExcelCode(setLayout=False)
    readedExcel.ExcelRead(fileName='D:\\Kiwoo\\ExcelData\\20160127\\20160127_yang_1.xlsx')
    wb = readedExcel.getWorkBook()
    ws = readedExcel.getWorkSheet()
    codelist = readedExcel.getCodeList()
    RQueue = mp.Queue()
    WQueue = mp.Queue()

    dbm = dbm2()
    dbm.setDBName("D:\\OneDrive\\python\\sqlite3\\kosdaq.db")

    
    
    dbm.setCodelist(codelist)
    
    for code in codelist:
        RQueue.put(code)
    RQueue.put('END')
    
    
    
    
    print('RQsetting ')
    process=[]
    for proc in range(5):
        proc = multi()
        proc.setting(WQueue, RQueue)
        process.append(proc)
        proc.daemon= True
        proc.start()
    
#     WQueue.put('END')
    dbm.setWQueue(WQueue)
    dbm.start()
    dbm.join()
    dbm.commit()

