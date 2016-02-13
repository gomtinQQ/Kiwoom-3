# -*- coding: utf-8 -*-

import ExcelMake
import DBMake

class ExcelToSqlite3(ExcelMake.ExcelCode):
    
    def __init__(self,setLayout=True):
        super().__init__(setLayout)


if __name__ == '__main__':
    
    e2s = ExcelToSqlite3(False)
    e2s.ExcelRead("D:\\OneDrive\\python\\ExcelData\\20160204\\20160204_yang_1")
    wb = e2s.getWorkBook();
    ws = e2s.getWorkSheet();
    indexCode=e2s.getIndexCode()
    
    
    i=1
    totalMinute=3
    codeNameCoast={}
    while(ws.Cells(i,1).Value is not None):
        code = ws.Cells(i,1).Value
        name = ws.Cells(i,2).Value
        innerNameCoast={}
        try:
            
            for Hour in range(9,15):
                for Min in range(0,60):
                    coast = ws.Cells(i,totalMinute).Value
                    Time = ws.Cells(1,totalMinute).Value
                    
                    coast=str(coast)
                    Time=int(Time)
                    innerNameCoast[Time]=coast
                    totalMinute+=1
            print(str(i)+'/'+str(len(indexCode)))
            codeNameCoast[code]=innerNameCoast
            totalMinute=3
            i+=1
        except :
            print('exception')
            
            
            