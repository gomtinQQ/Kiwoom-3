# -*- coding: utf-8 -*-


import multiprocessing as mp

q = mp.Queue()


for i in range(1,51):
    q.put(i)




while(q.empty() ==False ):
    print(q.get())