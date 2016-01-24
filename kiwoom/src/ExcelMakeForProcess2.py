# -*- coding: utf-8 -*-
import ExcelMake
from multiprocessing import Process,Queue

class ExcelReadProc(Process):

    
    def __init__(self,rqueue,wqueue):
        
        Process.__init__(self)
#         super(ExcelReadProc,self).__init__()
        
        self.q=rqueue
        self.wq=wqueue

        
    
    def run(self):
        
#         i=0
        print('h')
        
        

    def getrQueue(self):
        return self.q
    
    def getwQueue(self):
        return self.wq
            
    def doWrite(self,writeQueue):

        wq=writeQueue

        print('claal!')

        while True:
            TimePerDict = wq.get()
            if TimePerDict == 'END':
                break;
            print(TimePerDict)
    def doExcel(self):
        
        self.excelMake=ExcelMake.ExcelCode()
        self.excelMake.ExcelRead(False)
         
        codelist = self.excelMake.getCodeList()
 
        for code in codelist:
            self.q.put(code)
        self.q.put('END')



if __name__ == '__main__':
    # tt = ExcelMake.ExcelCode(False)
    
    wq=Queue()
    
    rq=Queue()
    
    processes=[]
    
    exmp= ExcelReadProc(wq,rq)
    exmp.doExcel()
        
        
    processes.append(exmp)
    exmp.start()
#     rq = exmp.getrQueue()
    
    