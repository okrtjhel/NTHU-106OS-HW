# -*- coding: utf8 -*-
# hw2.py
# 陳涵宇, 104062203
# comments
# your code here
def YieldBST(T):
	if T is not None:
		root = T[0]
		left = T[1]
		right = T[2]
		yield from YieldBST(left)
		yield root
		yield from YieldBST(right)

# begin built-in test case follows your code in the same .py file
# the test case is run when you run this file as top-level, 
# but not if it is imported into another Python program as a module
if __name__ == '__main__':
	L = []
	T = (17, (12, (6, None, None), (14, None, None)), (35, (32,	None, None), (40, None, None)))
	for v in YieldBST(T):
		L.append(v)
	print(L)