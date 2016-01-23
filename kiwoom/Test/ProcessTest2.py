import multiprocessing
import os



class Prt:
    
    def info(self,title):
        print(title)
        print('module name:',__name__)
        print('parent process:',os.getppid())
        print('process id:',os.getpid())
    
    def f(self,start,end,q):
#         self.info('fuction f')

        print('parent process:',os.getppid())
        print('process id:',os.getpid())
        
        
        i=start
        for i in range(start,end):
            i+=i
            
        q.put(i)
    
    
if __name__ == '__main__':
    pt = Prt()
#     pt.info('main line')
#     p = multiprocessing.Process(target=pt.f('bob'))
#     p.start()
#     p.join()
#     
#     p = multiprocessing.Process(target=pt.f('bo'))
#     
#     
    q = multiprocessing.Queue()
    pl=[]
    q.put(50)
    
    for p in range(2):
        p = multiprocessing.Process(target=pt.f ,args=(1,3,q))
        pl.append(p)
        p.start()
        
    print(q.get())
    