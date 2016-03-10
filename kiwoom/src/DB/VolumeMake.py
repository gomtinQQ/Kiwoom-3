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

class VolumeMake(MakeDB.DBMake):
        

    def createDatabase(self,DBName,tableName):
        '''형식에 맞는 테이블 생성.'''
        super().createDatabase(DBName,tableName)

    def initAndCreateVolume(self):
        self.createDatabase('../../Sqlite3/VolumeForeignCompany.db','Volume')
        self.addDateColumn()
        self.addCodeNameData()
        self.addDateVolume()
        
    def initAndCreateForeign(self):
        self.createDatabase('../../Sqlite3/VolumeForeignCompany.db','Foreigner')
        self.addDateColumn()
        self.addCodeNameData()
        self.addForeign()
        
    def initAndCreateCompany(self):
        self.createDatabase('../../Sqlite3/VolumeForeignCompany.db','Company')
        self.addDateColumn()
        self.addCodeNameData()
        self.addDateVolume()
        
        
        
if __name__ == '__main__':
    cp =VolumeMake()
    cp.initAndCreateForeign()