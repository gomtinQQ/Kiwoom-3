# -*- coding: utf-8 -*-
import multiprocessing
import os
import time


class Prt:

    def reader(self,queue):
        while True:
            msg = queue.get()
            if (msg=='DONE'):
                break;
    
    def writer(self,count,queue):
        for ii in range(0,count):
            queue.put(ii)
        queue.put('DONE')
        

    
if __name__ == '__main__':
    pt = Prt()

    # for count in [10000,100000,1000000]:
    #     queue = multiprocessing.Queue()

    #     reader_p = multiprocessing.Process(target = pt.reader,args=((queue),))
        
    #     reader_p.start()

    #     _start = time.time()
    #     pt.writer(count,queue)
    #     reader_p.join()

    #     print(count,'hi',(time.time()-_start))
    print('ㅇ')