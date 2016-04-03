# -*- coding: utf-8 -*-
import sqlite3
import sys,os
sys.path.append('../')
sys.path.append('../Data')
import time
import linecache
import multiprocessing as mp
from SRC.Database import MakeDB

class VolumeForeiCompany(MakeDB.DBMake):
        

#     def __init__(self):
#         self.initConfigSet()
        
    def createDatabase(self,DBName,tableName):
        '''형식에 맞는 테이블 생성.'''
        super().createDatabase(DBName,tableName)

    def initAndCreateVolume(self):
        
#         self.createDatabase('../../Sqlite3/VolumeForeignCompany.db','Volume')
        self.createDatabase(self.VolumeDB,self.VolumeTable)
        self.addDateColumn()
        self.addCodeNameData()
        self.addVolume()
        
    def initAndCreateForeign(self):
        self.createDatabase(self.ForeignerDB,self.ForeignerTable)
        self.addDateColumn()
        self.addCodeNameData()
        self.addForeign()
        
    def initAndCreateCompany(self):
        self.createDatabase(self.ComapanyDB,self.CompanyTable)
        self.addDateColumn()
        self.addCodeNameData()
        self.addCompany()
        
    def initAndCreateClose(self):
        self.createDatabase(self.ClosePriceDB,self.ClosePriceTable)
        self.addDateColumn()
        self.addCodeNameData()
        self.addDatePrice()
        
    def addUntilForeign(self):
        self.setProperties(self.ForeignerDB,self.ForeignerTable)
        self.addDateColumn()
        self.addForeign()
#         Foreign = mp.Process(name="Foreign",target=self.addForeign)
#         Foreign.start()
    def addUntilVolume(self):    
        self.setProperties(self.VolumeDB,self.VolumeTable)
        self.addDateColumn()
        self.addVolume()
#         Volume = mp.Process(name="Volume",target = self.addVolume)
#         Volume.start()
        
    def addUntilCompany(self):
        self.setProperties(self.ComapanyDB,self.CompanyTable)
        self.addDateColumn()
        self.addCompany()
#         Company = mp.Process(name="Company",target = self.addCompany)
#         Company.start()

    def addUntilClose(self):
        self.setProperties(self.ClosePriceDB,self.ClosePriceTable)
        self.addDateColumn() 
        self.addDatePrice()
        
    def addUntillDate(self):
        
        self.setProperties(self.ForeignerDB,self.ForeignerTable)
        self.addDateColumn()
        Foreign = mp.Process(name="Foreign",target=self.addForeign)
        Foreign.start()
        
        self.setProperties(self.VolumeDB,self.VolumeTable)
        self.addDateColumn()
        
        
        Volume = mp.Process(name="Volume",target = self.addVolume)
        Volume.start()
        
        self.setProperties(self.ComapanyDB,self.CompanyTable)
        self.addDateColumn()
        
        Company = mp.Process(name="Company",target = self.addCompany)
        Company.start()
        
if __name__ == '__main__':
    cp =VolumeForeiCompany()
#     cp.addUntillDate()
#     cp.initConfigSet()
#     cp.setLog()
    Foreignf = mp.Process(name="Foreign",target=cp.addUntilForeign)
    Volume = mp.Process(name="Volume",target = cp.addUntilVolume)
    Company = mp.Process(name="Company",target = cp.addUntilCompany)
    closePrice = mp.Process(name="Close",target = cp.addUntilClose)
     
    Foreignf.start()
    Volume.start()
    Company.start()
    closePrice.start()
#     wor11 = mp.Process(name="Company",target=cp.initAndCreateCompany)
#     wor12 = mp.Process(name="Foreign",target=cp.initAndCreateForeign)
#     wor13 = mp.Process(name="Volume",target=cp.initAndCreateVolume)
# 
#     wor11.start()
#     wor12.start()
#     wor13.start()
