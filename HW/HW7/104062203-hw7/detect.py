# -*- coding: utf8 -*-
# detect.py
# 陳涵宇, 104062203
# Deadlock Detection, similar to Banker's

from banker import Banker, sumColumn, IncrVec, DecrVec, GtVec, LeVec

class DeadlockDetector(Banker):
	def __init__(self, alloc, totalRsrc):
		Banker.__init__(self, alloc, None, totalRsrc)

	def detect(self, Request):
		'''detect deadlock with the request matrix'''
		# 1(a) initialize Work = a copy of Available
		# 1(b) Finish[i] = (Allocation[i] == [0, ...0])
		# optionally, you can keep a Sequence list
		Sequence = []  # use this list to save the safe sequence
		Work = [0 for x in range(self.m)] # your code to initialize Work vector
		Finish = [False for y in range(self.n)]
		for i in range(0, self.m):
			Work[i] = self.Available[i]

		for j in range(self.n):
			for k in range(self.m):
				if self.Allocation[j][k] is not 0:
					Finish[i] = False
					break

		print('Finish=%s' % Finish)
		counter = 0
		for _ in range(self.n):
			change = False
			for i in range(self.n):
				# Step 2: similar to safety algorithm
				#   if there is an i such that (Finish[i] == False)
				#   and Request_i <= Work, (hint: LeVec() or GtVec()) then
				#   Step 3: 
				#     Work += Allocation[i] # hint IncrVec()
				#     Finish[i] = True
				#        continue Step 2
				print('i=%d, ' % i, end="")
				if LeVec(Request[i], Work):
					if Finish[i] == False:
						Finish[i] = True
						change = True
						print('(Request[%d]=%s) <= ' % (i, Request[i]), end="")
						print('(Work=%s) ' % Work, end="")
						print(Finish[i], end="")
						print(', append P%d' % i)
						IncrVec(Work, self.Allocation[i])
						Sequence.append(i)
						counter = counter + 1
						print('(+Allocation[%d]=%s)=> ' % (i, self.Allocation[i]), end="")
						print('Work=%s, ' % Work, end="")
						print('Finish=%s' % Finish)
						if counter is self.n:
							return Sequence
					else:
						print('Finish[%d] True, skipping' % i)
				else:
					print('(Request[%d]=%s) <= ' % (i, Request[i]), end="")
					print('(Work=%s) ' % Work, end="")
					print(Finish[i], end="")
					print(', P%d must wait' % i)
			if change is False:
				return None
		# Step 4: either done iterating or (no such i exists)
		#    Finish vector indicates deadlocked processes.
		#    if all True then no deadlock.


if __name__ == '__main__':
	Allocation  = [[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1], [0, 0, 2]]
	Request     = [[0, 0, 0], [2, 0, 2], [0, 0, 0], [1, 0, 0], [0, 0, 2]]
	Request1    = [[0, 0, 0], [2, 0, 2], [0, 0, 1], [1, 0, 0], [0, 0, 2]]
	Available   = [0, 0, 0]
	TotalResources = [7, 2, 6]
	d = DeadlockDetector(Allocation, TotalResources)
	s = d.detect(Request)
	if s is not None:
		print('sequence = %s' % s)
	else:
		print('deadlock')
	s = d.detect(Request1)
	if s is not None:
		print('sequence = %s' % s)
	else:
		print('deadlock')
