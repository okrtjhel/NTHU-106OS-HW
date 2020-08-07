# -*- coding: utf8 -*-
# memalloc.py
# 陳涵宇, 104062203
import bisect

class MemAlloc:

	_POLICIES = ('FirstFit', 'BestFit', 'WorstFit')

	def __init__(self, totalMemSize, policy = 'BestFit'):
		if not policy in MemAlloc._POLICIES:
			raise ValueError('policy must be in %s' % MemAlloc._POLICIES)
		self.allocation = { } # map pointer to (size)
		self.holes = [(0, totalMemSize)] # sorting by pointer
		# your code here
		self.policy = policy

	# insert your own utility methods as needed

	def malloc(self, reqSize):
		'''return the starting address of the block of memory, or None'''
		# your code here
		if self.policy is 'FirstFit':
			for space in self.holes:
				if reqSize <= space[1]:
					s_addr = space[0]
					self.allocation[space[0]]=reqSize
					if reqSize < space[1]:
						self.holes.append((space[0]+reqSize,space[1]-reqSize))
					self.holes.remove(space)
					self.holes.sort()
					return s_addr
		elif self.policy is 'BestFit':
			best = (-1,-1)
			flag = False
			# find the smallest space that fit the request
			for space in self.holes:
				if reqSize <= space[1]:
					if best[1] < 0 or space[1] < best[1]:
						best = space
						flag = True
			# if space is found
			if flag:
				s_addr = best[0]
				self.allocation[best[0]]=reqSize
				if reqSize < best[1]:
					self.holes.append((best[0]+reqSize,best[1]-reqSize))
				self.holes.remove(best)
				self.holes.sort()
				return s_addr
		elif self.policy is 'WorstFit':
			worst = (-1,-1)
			flag = False
			# find the largest space that fit the request
			for space in self.holes:
				if reqSize <= space[1]:
					if worst[1] < space[1]:
						worst = space
						flag = True
			# if space is found
			if flag:
				s_addr = worst[0]
				self.allocation[worst[0]]=reqSize
				if reqSize < worst[1]:
					self.holes.append((worst[0]+reqSize,worst[1]-reqSize))
				self.holes.remove(worst)
				self.holes.sort()
				return s_addr
		return None


	def free(self, pointer):
		'''free the previously allocated memory starting at pointer'''
		# your code here
		# if empty holes list
		if self.holes is None:
			self.holes.append((pointer,self.allocation[pointer]))
		else:
			# if (p, s) goes before the first hole on the list
			if pointer < self.holes[0][0]:
				first = self.holes[0]
				# if (p, s) and first hole are disjoint
				if pointer+self.allocation[pointer] < first[0]:
					self.holes.append((pointer,self.allocation[pointer]))
				# if contiguous
				else:
					new_addr = pointer
					new_size = first[0]+first[1]-pointer
					self.holes.remove(first)
					self.holes.append((new_addr,new_size))
			# if (p, s) goes after the last hole on the list
			elif pointer > self.holes[len(self.holes)-1][0]:
				last = self.holes[len(self.holes)-1]
				# if (p, s) and last hole are disjoint
				if last[0]+last[1] < pointer:
					self.holes.append((pointer,self.allocation[pointer]))
				# if contiguous
				else:
					new_addr = last[0]
					new_size = pointer+self.allocation[pointer]-last[0]
					self.holes.remove(last)
					self.holes.append((new_addr,new_size))
			# if (p, s) goes between hole [i] and hole [i+1]
			else:
				temp_addr = 0
				# find where (p, s) should be placed
				for i in range(len(self.holes)):
					if self.holes[i][0] < pointer and pointer < self.holes[i+1][0]:
						temp_addr = i
						break
				temp1 = self.holes[temp_addr]
				temp2 = self.holes[temp_addr+1]
				# if all three are contiguous
				if temp1[0]+temp1[1] >= pointer and pointer+self.allocation[pointer] >= temp2[0]:
					new_addr = temp1[0]
					new_size = temp2[0]+temp2[1]-temp1[0]
					self.holes.remove(temp1)
					self.holes.remove(temp2)
					self.holes.append((new_addr,new_size))
				# if (p, s) contiguous with [i]
				elif temp1[0]+temp1[1] >= pointer:
					new_addr = temp1[0]
					new_size = pointer+self.allocation[pointer]-temp1[0]
					self.holes.remove(temp1)
					self.holes.append((new_addr,new_size))
				# if (p, s) contiguous with [i+1]
				elif pointer+self.allocation[pointer] >= temp2[0]:
					new_addr = pointer
					new_size = temp2[0][0]+temp2[0][1]-pointer
					self.holes.remove(temp2)
					self.holes.append((new_addr,new_size))
				# if all three are disjoint
				else:
					self.holes.append((pointer,self.allocation[pointer]))
		del self.allocation[pointer]
		self.holes.sort()

	def __str__(self):
		return repr(self.allocation)


def runTestScript(requests):
	ff = MemAlloc(20, 'FirstFit')
	bf = MemAlloc(20, 'BestFit')
	wf = MemAlloc(20, 'WorstFit')
	ffSym = {}
	bfSym = {}
	wfSym = {}
	for name, size in requests:
		if size is None:
			# do a free() call
			ff.free(ffSym[name]); del(ffSym[name])
			bf.free(bfSym[name]); del(bfSym[name])
			wf.free(wfSym[name]); del(wfSym[name])
			print('free(%s)' % name)
		else: 
			# do an malloc() call
			ffSym[name] = ff.malloc(size)
			bfSym[name] = bf.malloc(size)
			wfSym[name] = wf.malloc(size)
			print('%s=malloc(%d):' % (name, size))
		print(' FirstFit symbols=%s holes=%s allocation=%s' % (ffSym, ff.holes, ff.allocation))
		print(' BestFit symbols=%s holes=%s allocation=%s' % (bfSym, bf.holes, bf.allocation))
		print(' WorstFit symbols=%s holes=%s allocation=%s' % (wfSym, wf.holes, wf.allocation))

if __name__ == '__main__':

	requests = [('a', 10), ('b', 1), ('c', 4), ('c', None), ('a', None),
				('d', 9),  # worst fit and first fit would use (0, 10), but best fit would use (11, 9)
				('e', 10), # worst fit and first fit wold fail, but best fit would succeed with (0, 10)
	]
	runTestScript(requests)

	print('------------------------')

	requests = [('a', 3), ('b', 6), ('c', 2), ('d', 5), # malloc
				('a', None), ('c', None), # free
				('e', 2),  # best fit (9, 2), first fit (0, 2), worst fit (16, 2)
				('b', None), # free: best fit merges (0,3) and (3,6) => (0,9)
					# first fit merges (3,6), (9,2) => (3, 8)
					# worst fit merges (0,3), (3,6), (9,2) => (0,11)
				('f', 11)   # both best fit and first fit fail, but worst fit succeeds
	]
	runTestScript(requests)