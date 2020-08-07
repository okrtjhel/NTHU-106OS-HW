# -*- coding: utf8 -*-
# disk.py
# 陳涵宇, 104062203
# disk scheduling algorithms

class DiskScheduler:
	_POLICIES = ['FCFS', 'SSTF', 'SCAN', 'LOOK', 'C-SCAN', 'C-LOOK']

	def __init__(self, nCylinders):
		self.nCylinders = nCylinders

	def schedule(self, initPos, requestQueue, policy, direction):
		'''
			request is the list of cylinders to access
			policy is one of the strings in _POLICIES.
			direction is 'up' or 'down'
			returns the list for the order of cylinders to access.
		'''
		if policy == 'FCFS':
			# return the disk schedule for FCFS
			order = requestQueue
			return order

		if policy == 'SSTF':
			# shortest seek time first
			# compute and return the schedule for the shortest seek time first
			order = []
			queue = requestQueue[:]
			pos = initPos
			for i in range(len(requestQueue)):
				dist = 999999
				closest = -1
				for x in queue:
					if abs(x - pos) < dist:
						dist = abs(x - pos)
						closest = queue.index(x)
				new = queue[closest]
				pos = new
				order.append(new)
				del queue[closest]
			return order

		if policy in ['SCAN', 'C-SCAN', 'LOOK', 'C-LOOK']:
			# sequentially one direction to one end, 
			# then sequentially to the other `
			# decide on direction (up or down) based on initial request
			# compute and return the schedule accordingly
			order = []
			pos = initPos
			d = direction
			queue = requestQueue[:]
			num = len(requestQueue)
			while(True):
				if(d == 'up'):
					new_queue = sorted(queue)
					for x in new_queue:
						if x >= pos:
							new = queue[queue.index(x)]
							order.append(new)
							del queue[queue.index(x)]
							num = num - 1
					if num is 0:
						break
					if policy == 'SCAN':
						d = 'down'
						pos = new_queue[len(new_queue)-1]
						if pos is not self.nCylinders-1:
							order.append(self.nCylinders-1)

					elif policy == 'C-SCAN':
						if new_queue[len(new_queue)-1] is not self.nCylinders-1:
							order.append(self.nCylinders-1)
						pos = 0
						if new_queue[0] is not 0:
							order.append(0)

					elif policy == 'LOOK':
						d = 'down'
						pos = new_queue[len(new_queue)-1]

					elif policy == 'C-LOOK':
						pos = new_queue[0]
									
						
				elif(d == 'down'):
					new_queue = sorted(queue, reverse=True)
					for x in new_queue:
						if x <= pos:
							new = queue[queue.index(x)]
							order.append(new)
							del queue[queue.index(x)]
							num = num - 1
					if num is 0:
						break
					if policy == 'SCAN':
						d = 'up'
						pos = new_queue[len(new_queue)-1]
						if pos is not 0:
							order.append(0)

					elif policy == 'C-SCAN':
						if new_queue[len(new_queue)-1] is not 0:
							order.append(0)
						pos = self.nCylinders-1
						if new_queue[0] is not self.nCylinders-1:
							order.append(self.nCylinders-1)

					elif policy == 'LOOK':
						d = 'up'
						pos = new_queue[len(new_queue)-1]

					elif policy == 'C-LOOK':
						pos = new_queue[0]

			return order

def totalSeeks(initPos, queue):
	lastPos = initPos
	totalMoves = 0
	for p in queue:
		totalMoves += abs(p - lastPos)
		lastPos = p
	return totalMoves

if __name__  == '__main__':
	def TestPolicy(scheduler, initHeadPos, requestQueue, policy, direction):
		s = scheduler.schedule(initHeadPos, requestQueue, policy, direction)
		t = totalSeeks(initHeadPos, s)
		print('policy %s %s (%d): %s' % (policy, direction, t, s))

	scheduler = DiskScheduler(200)
	requestQueue = [98, 183, 37, 122, 14, 124, 65, 67]
	initHeadPos = 53
	for policy in DiskScheduler._POLICIES:
		if policy[:2] == 'C-' or policy[-4:] in ['SCAN', 'LOOK']:
			TestPolicy(scheduler, initHeadPos, requestQueue, policy, 'up')
			TestPolicy(scheduler, initHeadPos, requestQueue, policy, 'down')
		else:
			TestPolicy(scheduler, initHeadPos, requestQueue, policy, '')

	print('more tests on SCAN and C-SCAN')
	rQs = [[98, 37, 0, 122, 14], [98, 37, 199, 122, 14], [98, 0, 37, 199, 14]]
	for q in rQs:
		print('Q=%s' % q)
		for policy in ['SCAN', 'C-SCAN']:
			for direction in ['up', 'down']:
				TestPolicy(scheduler, initHeadPos, q, policy, direction)
