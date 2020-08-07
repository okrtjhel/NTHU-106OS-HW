# -*- coding: utf8 -*-
# hw1.py
# 陳涵宇, 104062203
# comments
def PrintBST(T):
	root = T[0]
	left = T[1]
	right = T[2]

	if left != None:
		PrintBST(left)	

	print(root)

	if right != None:
		PrintBST(right)
		
# your code here

# begin built-in test case follows your code in the same .py file
# the test case is run when you run this file as top-level, 
# but not if it is imported into another Python program as a module
if __name__ == '__main__':
	T = (17, (12, (6, None, None), (14, None, None)), (35, (32,	None, None), (40, None, None)))
	PrintBST(T)