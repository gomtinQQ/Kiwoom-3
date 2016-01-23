from threading import Thread,Lock
import queue
import time

class ThreadClas(Thread):

    def __init__(self,q):
        Thread.__init__(self)
        self.q = q
#         self.q.put(self.getName())
        



    def run(self):
        
        # print('%s say hell world at time '%self.getName(),now)

        while(True):
            
            print(self.getName()+' - '+str(self.q.get() ))
            
            if self.q.qsize() == 0:
                break
              
              
              
if __name__ == '__main__':

    q = queue.Queue()
    
    
    for i in range(1,100001):
        q.put(i)
        
    start_time=time.time()
    
    dev =[]
    for i in range(2):
        test = ThreadClas(q)
        dev.append(test)
        test.start()
    
    for devlen in dev:
        devlen.join() 
    print('time')
    print(str(time.time()-start_time))
    
    