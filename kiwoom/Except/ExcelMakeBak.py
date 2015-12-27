# -*- coding: utf-8 -*-

import win32com.client
from bqplot.testing import __main__



class ExcelCode:
            
    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.wb = self.excel.Workbooks.Add()
        self.ws = self.wb.Worksheets("Sheet1")
        self.ws.Cells(1,1).Value ="종목코드"
        self.ws.Cells(1,2).Value ="종목명"
        
        self.j=2
        print('success')
        
    def addToExcel(self,codelist):
        codelist=codelist.split(';')
        i=2
        
        for a in codelist:
            self.ws.Cells(i,1).Value = a
            i += 1
        self.excel.Visible = True
        
        
    def addToExcelCodeName(self,mylist):
        if mylist !=  None:
            self.ws.Cells(self.j,2).Value=mylist
            self.j+=1
        
        