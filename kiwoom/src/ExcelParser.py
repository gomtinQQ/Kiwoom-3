# -*- coding: utf-8 -*-

import win32com.client
import ExcelMake

class ExcelParser:
    
    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.readedExcel = ExcelMake.ExcelCode(False)
        self.readedExcel.ExcelRead()


        print('hi')
        
        
        
if __name__ == '__main__':
    test = ExcelParser()
    