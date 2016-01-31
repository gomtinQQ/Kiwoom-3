# -*- coding: utf-8 -*-

import sqlite3
import ExcelMake

conn = sqlite3.connect("D:\\OneDrive\\python\\sqlite3\\kosdaq.db")



cursor = conn.cursor()

# cursor.execute("CREATE TABLE kosdaq1(StockCode text, StockName int)")
# cursor.executemany('''insert into kosdaq values(?,?)''',("한",'한양'))

# cursor.execute("insert into kosdaq ('StockCode','StockName') values(?,?)",(900090,'gg'))



class dbm:
    
    def con(self,dbname=""):
        self.conn=""
        
        if dbname=="":
            self.conn = sqlite3.connect("D:\\OneDrive\\python\\sqlite3\\kosdaq.db")
        else:
            self.conn = sqlite3.connect(dbname)
            
        return self.conn
        

    def setCodelist(self,codelist,tablename,conn):
        
        self.cursor = conn.cursor()
        
        for code in codelist:
            code = str(code)
            self.cursor.execute("insert into "+tablename+" (StockCode) values ("+code+")")
        conn.commit()
        
    def setNamelist(self,namelist,tablename,conn):
        
        self.cursor = conn.cursor()
        
        for name in namelist:
            name = str(name)
            self.cursor.execute("insert into "+tablename+" (StockName) values ("+name+")")
        conn.commit()

    def setNameCode(self,codeName,tablename,conn):
        
        self.cursor = conn.cursor()
        
        for name in namelist:
            name = str(name)
            self.cursor.execute("insert into "+tablename+" (StockName) values ("+name+")")
        conn.commit()
        
    

if __name__ == '__main__':
#     ex = dbm()
#     con = dbm().con()
    
    readedExcel = ExcelMake.ExcelCode(setLayout=False)
    readedExcel.ExcelRead(fileName='D:\\Kiwoo\\ExcelData\\20160127\\20160127_yang_1.xlsx')
    wb = readedExcel.getWorkBook()
    ws = readedExcel.getWorkSheet()
    
    codeName = readedExcel.getCodeName()
    
    codelist = readedExcel.getCodeList()
    print(codeName)
    
    dbm().con()
    
    dbm().setCodelist(codelist, 'kosdaq' , dbm().con())
#     dbm().setNamelist(namelist, 'kosdaq' , dbm().con())
#     
# cursor.execute("select * from kosdaq")
# conn.commit()
# 
# print(cursor.fetchall())
# conn.close()