# -*- coding: utf-8 -*-

import win32com.client
import ExcelMake

class ExcelParser:
    
    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.readedExcel = ExcelMake.ExcelCode(False)
        self.readedExcel.ExcelRead()

        self.codelist = self.readedExcel.getIndexCode()

        self.wb = self.readedExcel.getWorkBook()
        self.ws = self.readedExcel.getWorkSheet()
        
    def parse(self):
    	
    	try:
    		

    	except Exception:

        
        
        
if __name__ == '__main__':
    test = ExcelParser()
    test.parse()