import threading

def MakeParkingLot(N):
	global sem  # semaphore for the parking lot
	global spots # list for the spots
	global spotsSync  # for synchronizing access to spots
	spots = [None for i in range(N)]
	#  your code to initialize sem and spotsSync
	sem = threading.Semaphore(value=N)
	spotsSync = threading.Lock()

def MakeCars(C):
	# your code here to spawn threads
	# don’t forget to return the list
	th_car = [];
	for i in range(0,C):
		th = threading.Thread(target=Park, args=(i,))
		th_car.append(th)
	return th_car

def Park(car):
	global sem, spots, spotSync

	while sem is 0:pass
	sem.acquire()
	spotsSync.acquire()
	cur_spot = 0
	for i in range(len(spots)):
		if spots[i] is None:
			spots[i] = car
			cur_spot = i
			break

	snapshot = spots[:]  # make a copy for printing
	print("Car %d got spot: %s" % (car, snapshot))
	spotsSync.release()
	
	import time
	import random
	st = random.randrange(1,10)
	time.sleep(st)
	sem.release()
	
	spots[cur_spot] = None
	snapshot = spots[:]  # make a copy for printing
	print("Car %d left after %d sec, %s" % (car, st, snapshot))
	

if __name__ == '__main__':
	MakeParkingLot(5)
	cars = MakeCars(15)
	for i in range(15): cars[i].start()
