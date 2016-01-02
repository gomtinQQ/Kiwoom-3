# -*- coding: utf-8 -*-

import win32com.client
from time import sleep





class ExcelCode:
            
    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.wb = self.excel.Workbooks.Add()
        self.ws = self.wb.Worksheets("Sheet1")
        self.ws.Cells(1,1).Value ="종목코드"
        self.ws.Cells(1,2).Value ="종목명"
        self.j=2
        print('Excel Object Created')
        
        print('Making Excel..')        
        totalMinute=5
        for i in range(9,16):
            for j in range(0,61):
                self.ws.Cells(1,totalMinute).Value =str(i)+":"+str(j)
                totalMinute+=1
        
    def addToExcel(self,codelist):
        self.codelist=codelist.split(';')
        i=2
        
        for a in self.codelist:
            self.ws.Cells(i,1).Value = a
            i += 1
                
    def addToExcelCodeName(self,mylist):
        self.ws.Cells(self.j,2).Value=mylist
        self.j+=1
        
        
        
    def excelVisible(self):
        self.excel.Visible = True
        
    def getCodeList(self):
        return self.codelist
    
    
    def addZero(self,str):
        str=str.strip()

        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
        return str
    
