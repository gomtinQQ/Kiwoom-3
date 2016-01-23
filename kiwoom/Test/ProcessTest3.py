import multiprocessing as mp
import time




class pttest:

	def worker(self,start,end,queue):

		
		b=0
		for i in range(start,end):
			b+=i

		queue.put(b)

	

if __name__ == '__main__':

	pt = pttest()

	queue = mp.Queue()

	num=10

	_start=time.time()
	pc = mp.Process(target=pt.worker,args=(1,11000000,queue,))
	pc.setDaemon=True
	pc.start()

	# pc1 = mp.Process(target=pt.worker,args=(11000000,17000000,queue,))
	# pc1.setDaemon=True
	# pc1.start()

	# pc2 = mp.Process(target=pt.worker,args=(17000000,19000000,queue,))
	# pc2.setDaemon=True
	# pc2.start()

	# pc3 = mp.Process(target=pt.worker,args=(19000000,20000000,queue,))
	# pc3.setDaemon=True
	# pc3.start()

	pc1 = mp.Process(target=pt.worker,args=(1,20000000,queue,))
	pc1.setDaemon=True
	pc1.start()

	# pc.join()
	pc1.join()
	# pc2.join()
	# pc3.join()
	print(queue.get())
	# print(queue.get())
	print((time.time()-_start))