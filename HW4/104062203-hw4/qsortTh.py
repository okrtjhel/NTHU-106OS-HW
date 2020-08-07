import threading

maxthreads = 4

def Partition(A, p, r):
	x = A[r]
	i = p - 1
	for j in range(p, r):
		if (A[j] <= x):
			i = i + 1
			A[i], A[j] = A[j], A[i]
	A[i+1], A[r] = A[r], A[i+1]
	return i + 1

def QuickSort(A, p, r):
	if p < r:
		q = Partition(A, p, r)
		if threading.active_count() <= maxthreads:
			th = threading.Thread(target=QuickSort, args=(A, p, q-1))
			th.start()
			th.join()
		else:
			QuickSort(A, p, q-1)
		QuickSort(A, q+1, r)
	else:
		pass

if __name__ == '__main__':
	with open('randomInt.txt', 'r') as fh:
		LEN = int(fh.readline().strip())
		L = []
		x = 0
		while x < LEN:
			L.append(int(fh.readline().strip()))
			x = x + 1
	fh.close()
	QuickSort(L, 0, len(L)-1)
	if L == list(range(LEN)):  # Python3 list(range(LEN)) instead of range(LEN)
		print("successfully sorted")
	else:
		print("sort failed: %s" % L)
