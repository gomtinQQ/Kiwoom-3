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

class closePriceMake(MakeDB.DBMake):
        

    def createDatabase(self,DBName,table):
        '''형식에 맞는 테이블 생성.'''
        super().createDatabase(DBName,table)
        
    def initAndCreateDefaultDB(self):
        self.initConfigSet()
        self.createDatabase(self.ClosePriceDB,self.ClosePriceTable)
        self.addDateColumn()
        self.addCodeNameData()
        self.addDatePrice()
        
    def addUntillDate(self):
        self.initConfigSet()
        self.setProperties(self.ClosePriceDB,self.ClosePriceTable)
#         sql = "update "+self.ClosePriceTable+" set " +date+" = "+price+" where StockCode = '"+code+"'" 
        self.addDatePrice()
        
if __name__ == '__main__':
    cp =closePriceMake()
    cp.addUntillDate()
#     cp.initAndCreateDefaultDB()