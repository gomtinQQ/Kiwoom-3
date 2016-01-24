# -*- coding: utf-8 -*-
import ExcelMake
import multiprocessing as mp



class ExcelMakeForProcess(Process):

	
	def __init__(self,queue):
		super(ExcelMakeForProcess,self).__init__()
		self.queue=queue
		
	
	
	def run(self):
		self.queue
        
		self.excelMake=ExcelMake.ExcelCode(False)
		self.excelMake.ExcelRead(False)
		self.excelMake.excelVisible()
        

		codelist = self.excelMake.getCodeList()

		for code in codelist:
			q.put(code)
		q.put('END')
		

	def doParse(self,readQueue,writeQueue):

		q=readQueue
		wq = writeQueue
        
# 		excelMake=ExcelMake.ExcelCode(False)
# 		excelMake.ExcelRead(True)
# 		excelMake.excelVisible()
		codelist = self.excelMake.getCodeList()
		
		for code in codelist:
			q.put(code)
		q.put('END')
		

		i=0
		# while True:
		while i<10:
			code = q.get()
			if code== 'END':
				wq.put('END')
				break

			timePerDict = self.excelMake.getPercent(code)
			wq.put(timePerDict)
			i+=1
# 		return wq

			
	def doWrite(self,writeQueue):

		wq=writeQueue

		print('claal!')

		while True:
			TimePerDict = wq.get()
			if TimePerDict == 'END':
				break;
			print(TimePerDict)




if __name__ == '__main__':
    # tt = ExcelMake.ExcelCode(False)

    exmp= ExcelMakeForProcess()

    
    writeQueue=mp.Queue()
    
    readQueue=mp.Queue()

    
    # while writeQueue.empty()==False:
    #     writeQueue.get()
    
    # while readQueue.empty()==False:
    #     readQueue.get()
    
#     p = mp.Process(target=exmp.doRead, args=(readQueue,))
#     p.setDaemon=True
#     p.start()
#     p.join()
    exmp.doRead(readQueue)
    pp = mp.Process(target=exmp.doParse,args=(readQueue,writeQueue,))
#     pp.setDaemon=True
    pp.start()
    pp.join()
    
    ppp = mp.Process(target=exmp.doWrite,args=(writeQueue,))
#     ppp.setDaemon=True
    ppp.start()
    ppp.join()
     
#     readQueue = exmp.doRead(readQueue)
#     writeQueue= exmp.doParse(readQueue,writeQueue)
#     exmp.doWrite(writeQueue)
    
    
    
#     exmp.doWrite(queue)

    # tt.ExcelRead()
    # tt.excelVisible()
    # tt.setAllValue()
    # tt.ExcelExitWithSave()
