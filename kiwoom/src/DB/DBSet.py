# -*- coding: utf-8 -*-
import multiprocessing as mp
import sqlite3
import configparser
import sys,os
sys.path.append('../')
sys.path.append('../Data')
import YGGetWebData
import time,datetime
import btsForDashin
import linecache
import traceback
import logging
from logging.handlers import RotatingFileHandler 

class DBSet():
    
    
    lock = mp.Lock()
    querylock = mp.Lock()
    config = configparser.ConfigParser()
    config.read("../config/config.ini")
    
    lock = mp.Lock()
    querylock = mp.Lock()
    config = configparser.ConfigParser()
    config.read("../config/config.ini")
    
    
#     def initConfigSet(self):
    def __init__(self):
        
        self.ForeignerDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB") 
        self.ComapanyDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB")
        self.VolumeDB = self.config.get("DATABASE","VolumeAndForeignAndCompanyDB")
        self.ClosePriceDB = self.config.get("DATABASE","ClosePriceDB")
        self.BuyListDB = self.config.get("DATABASE","BuyListDB")
        today = datetime.datetime.today().date()
        oneDay = datetime.timedelta(days=1)
        YESTERDAY= str( today - oneDay)
        
        
        self.ForeignerDB = self.ForeignerDB+".db"
        self.ComapanyDB = self.ComapanyDB+".db"
        self.VolumeDB = self.VolumeDB+".db"
        self.ClosePriceDB = self.ClosePriceDB+".db"
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
        
        self.fName = str(self.config.get("LOG","filename"))+'_'+str(datetime.datetime.today().date())
        self.loglevel = self.config.get("LOG","loglevel")
        self.fileSize = self.config.get("LOG","FILESIZE")
        
        for name,value in self.config.items():
            print('==========================',name,'==========================')
            for items in self.config.items(name):
                print('==',items[0],'=',items[1])
        

    def setLog(self):
        
#         logging.basicConfig(filename=self.fName,level = self.loglevel)
        
        self.logger = logging.getLogger("YGLogger")
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
        