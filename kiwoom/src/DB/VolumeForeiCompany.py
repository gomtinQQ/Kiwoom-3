# -*- coding: utf-8 -*-

import sqlite3
import sys,os
sys.path.append('../')
sys.path.append('../Data')
import YGGetWebData
import time
import btsForDashin
import linecache
import MakeDB
import multiprocessing as mp

class VolumeForeiCompany(MakeDB.DBMake):
        

    def createDatabase(self,DBName,tableName):
        '''형식에 맞는 테이블 생성.'''
        super().createDatabase(DBName,tableName)

    def initAndCreateVolume(self):
        self.createDatabase('../../Sqlite3/VolumeForeignCompany.db','Volume')
        self.addDateColumn()
        self.addCodeNameData()
        self.addVolume()
        
    def initAndCreateForeign(self):
        self.createDatabase('../../Sqlite3/VolumeForeignCompany.db','Foreigner')
        self.addDateColumn()
        self.addCodeNameData()
        self.addForeign()
        
    def initAndCreateCompany(self):
        self.createDatabase('../../Sqlite3/VolumeForeignCompany.db','Company')
        self.addDateColumn()
        self.addCodeNameData()
        self.addCompany()
        
        
        
if __name__ == '__main__':
    cp =VolumeForeiCompany()
    
    wor11 = mp.Process(name="Company",target=cp.initAndCreateCompany)
    wor12 = mp.Process(name="Foreign",target=cp.initAndCreateForeign)
    wor13 = mp.Process(name="Volume",target=cp.initAndCreateVolume)

    wor11.start()
    wor12.start()
    wor13.start()
    
#     cp.initAndCreateForeign()
#     cp.initAndCreateVolume()
#     cp.initAndCreateCompany()