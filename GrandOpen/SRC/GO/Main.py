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

from SRC.QT import KiwoomQT
from SRC.Database.Analyzer import RealDataAnalyzer
from SRC.Database import VolumeForeiCompany
from SRC.Database.ConditionSearch import GoldenSearchFromDB


class Main():
    config = configparser.ConfigParser()
    config.read("../CONFIG/config.ini")
    
    def __init__(self):
#         VolumeForeiCompany.VolumeForeiCompany(self.config).gogo()
        for name,value in self.config.items():
            print('[',name,']')
            for items in self.config.items(name):
                print(items[0],'=',items[1])
#         print(self.config.items("Init.Run"))
        
        for name,value in self.config.items("Init.Run"):
            
            if value !="0":
                print(value,"Start!")
#                 eval(value).gogo(self.config)
                
                proc = mp.Process(target=eval(value).gogo , args=(self.config,))
                proc.start
#                 name.gogo(self.config)
#         KiwoomQT.gogo(self.config)
#         GoldenSearchFromDB.gogo(self.config)
             
                
        
        
if __name__ == '__main__':
    Main()