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

    	# for index in range(2,len(self.codelist)+1):
    	# 	self.MuchVal = 
    	# 	print(index)
        i=2
        value = self.codelist
        try:
            while(value[i] != None):
            	j=3
            	while(int(self.ws.Cells(1,j).Value) !=1451):

                	value[i]=self.ws.Cells(i,j).Value 씨발 못하겠따...
                i+=1
            
        except KeyError:
            print('end')
        
if __name__ == '__main__':
    test = ExcelParser()
    test.parse()