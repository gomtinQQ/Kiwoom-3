# -*- coding: utf-8 -*-

import multiprocessing as mp
import time

class Process1(mp.Process):

    def __init__(self):

        super(mp.Process,self).__init__()
        print('hi')

    def run(self):
        print('1 - run')
        
        i=1
        while True:
            self.q.put(i)
            i+=1
            if i==10:
                self.q.put('END')
            time.sleep(1)

    def setwQueue(self,wq):

        self.q = wq


    def setrQueue(self,rq):

        self.rq = rq

class Process2(mp.Process):

    def run(self):
        print('process2 start')
        a=0
        while True:
#             self.lock.acquire()
            bt = self.wq.get()
#             self.lock.release()
            if bt =='END':
            
                self.wq.put('END')
                print(self.name +' break')
                break
            
            a+=bt
            print(self.name+' : '+'a의 값은   ' +str(a) + ' code : '+str(bt))                
                
        self.rq.put(a)
            


    def setrQueue(self,rq):
        self.rq = rq

    def setwQueue(self,wq):
        self.wq = wq
        
    def setLock(self,lock):
        self.lock=lock
        
    def pta(self):
        a=0
        while self.rq.empty() !=True:
           a+=self.rq.get() 
#         p = self.rq.get()+self.rq.get()
        print(a)
        
        
if __name__=='__main__':
    
#     pc2 = Process2()
#     pc22= Process2()
#     pc222= Process2()
    
    print(mp.cpu_count())
    
    wq = mp.Manager().Queue()
    rq = mp.Queue()
    lock = mp.Lock()
    
    for i in range(1,50001):
        wq.put(i)
    
    wq.put('END')
    
    processes=[]
    
    __start = time.time()
    
    for proc in range(6):
        proc = Process2()
        proc.setwQueue(wq)
        proc.setrQueue(rq)
        processes.append(proc)
        proc.start()
        
    for proc1 in processes:
        proc1.join()
        
    processes[0].pta() 
    print((time.time()-__start))
    
#     pc2.setwQueue(wq)
#     pc2.setrQueue(rq)
#     pc22.setwQueue(wq)
#     pc22.setrQueue(rq)
#     pc222.setwQueue(wq)
#     pc222.setrQueue(rq)
    
#     pc2.daemon=True
#     pc22.daemon=True
    
    
#     pc2.setLock(lock)
#     pc22.setLock(lock)
#     pc222.setLock(lock)
#     
#     pc2.start()
#     pc22.start()
#     pc222.start()
#     
#     pc2.join()
#     pc22.join()
#     pc222.join()
#     pc2.pta()
    