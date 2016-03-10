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
        

    def createDatabase(self,DBName):
        '''형식에 맞는 테이블 생성.'''
        super().createDatabase(DBName,'Volume')

    def initAndCreateDefaultDB(self):
        self.createDatabase('../../Sqlite3/Volume.db')
        self.addDateColumn()
        self.addCodeNameData()
        self.addDateVolume()
        
        
if __name__ == '__main__':
    cp =VolumeMake()
    cp.initAndCreateDefaultDB()