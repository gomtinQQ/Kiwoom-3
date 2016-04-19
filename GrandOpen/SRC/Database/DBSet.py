# -*- coding: utf-8 -*-
import multiprocessing as mp
import sqlite3
import configparser
import sys,os
sys.path.append('../')
sys.path.append('../Data')
import time,datetime
import linecache
import traceback
import logging
from logging.handlers import RotatingFileHandler
from SRC.Database import btsForDashin 

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]




class DBSet(object):
    
    __metaclass__ = Singleton
    
    lock = mp.Lock()
    querylock = mp.Lock()
    config = configparser.ConfigParser()
    config.read("../CONFIG/config.ini")
    
    
    
#     def initConfigSet(self):
    def __init__(self):
        
        self.ForeignerDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB") 
        self.ComapanyDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB")
        self.VolumeDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB")
#         self.ClosePriceDB = config.get("DATABASE","ClosePriceDB")
        self.BuyListDB = self.config.get("DATABASE","BuyListDB")
        today = datetime.datetime.today().date()
        oneDay = datetime.timedelta(days=1)
        YESTERDAY= str( today - oneDay)
        
        
        self.ForeignerDB = self.ForeignerDB+".db"
        self.ComapanyDB = self.ComapanyDB+".db"
        self.VolumeDB = self.VolumeDB+".db"
#         self.ClosePriceDB = self.ClosePriceDB+".db"
        self.BuyListDBYesterday =self.BuyListDB+YESTERDAY+".db"
        self.BuyListDBToday = self.BuyListDB+str(today)+".db" 
        
        
        self.ForeignerTable = self.config.get("DATABASE","ForeignTable")
        self.CompanyTable = self.config.get("DATABASE","CompanyTable")
        self.VolumeTable = self.config.get("DATABASE","VolumeTable")
        self.ClosePriceTable = self.config.get("DATABASE","ClosePriceDBTable")
        
        self.BuyListTable = self.config.get("DATABASE","BuyListTable")
        self.BuyListVolumeRotateTable = self.config.get("DATABASE","BuyListVolumeRotateTable")
        self.BuyListRelativeTable = self.config.get("DATABASE","BuyListRelativeTable")
        
        
        
        
        self.start_date_closePrice = self.config.get("DATE","ClosePrice.StartDATE")
        self.start_date_Volume = self.config.get("DATE","Volume.StartDATE")
        self.start_date_Foreign= self.config.get("DATE","FOREIGN.StartDATE")
        self.start_date_Company= self.config.get("DATE","Company.StartDATE")
        
        
        self.insertGoldQuery = self.config.get("QueryList","InsertGold")
        
        self.fName = str(self.config.get("LOG","filename"))+'_'+str(datetime.datetime.today().date())
        self.loglevel = self.config.get("LOG","loglevel")
        self.fileSize = self.config.get("LOG","FILESIZE")
        
#         for name,value in config.items():
#             print('==========================',name,'==========================')
#             for items in config.items(name):
#                 print('==',items[0],'=',items[1])
        

    def setLog(self):
        
#         logging.basicConfig(filename=self.fName,level = self.loglevel)
        
        self.logger = logging.getLogger(__name__)
        fomatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s")
        fileHandler = logging.FileHandler(self.fName)
        fileHandler = RotatingFileHandler(filename=self.fName,maxBytes=int(self.fileSize)*1024*1024)
        fileHandler.setFormatter(fomatter)
        
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(self.loglevel)
         
        self.logger.debug('*****************************DBMake Logging Start*****************************')
        
    def debug(self,msg):
        self.logger.debug(msg)
    
    def tracebackLog(self):
        print(traceback.print_exc())
        
    def commit(self):
        self.lock.acquire()
        self.conn.commit()
        self.lock.release()
        
    def setProperties(self,dbName,table):
        self.dbName=dbName
#         print(self.dbName)
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        self.setTable(table)
        
    def setTable(self,tableName):
        self.tableName = tableName
        
    def setCodeNameCoast(self):
        bfd = btsForDashin.btsForReal()
        self.codeNameCoast = bfd.UrlParsing()
        
    def getNowTime(self):
        dd = datetime.datetime.today()
        hours = str(dd.hour)
        
#         if len(hours)<2:
#             hours = '0'+hours
        minute = str((dd-datetime.timedelta(minutes=1)).minute)
#         minute = str(dd.minute-1)
        if len(minute)<2:
            minute ='0'+minute
            
        return hours+minute
    
    def pastAgo(self,time,interval):
        today = datetime.datetime.today()
        
        year_to = today.year
        month_to = today.month
        day_to = today.day
        
        if len(time)<4:
            time='0'+time
        t_hour = (time[:2])

        while len(t_hour)<2:
            t_hour = '0'+t_hour
        t_minute = int(time[2:])
        now = datetime.datetime(year=year_to,month=month_to,day=day_to,hour=int(t_hour),minute=t_minute)
#         now = datetime.timedelta(hours=t_hour,minutes=t_minute)
        ago = datetime.timedelta(minutes=interval)
        dd = now-ago
        hours = str(dd.hour)
#         if len(hours)<2:
#             hours = '0'+hours
        minute = str(dd.minute)
        if len(minute)<2:
            minute='0'+minute
        return str(hours)+minute
    
    def timeFormat(self,time):
        time=str(time)
        if len(time) !=4:
            raise  "타임을 4자리로맞추세요"
        hour = time[:2]
        minute = time[2:]
        
    def setQueue(self,q):
        self.dbQueue=q
        
        
        
        
        
        