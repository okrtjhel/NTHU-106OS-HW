# -*- coding: utf8 -*-
# hw3.py
# 陳涵宇, 104062203
# comments
# your code here
import socket
def MakeServerSocket(host='', port=8888, limit=10):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind((host, port))
	except socket.error as msg: 
		print('bind fails: '+str(msg[0]))
		import sys
		sys.exit(-1)
	s.listen(limit)
	return s

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
	T = (17, (12, (6, None, None), (14, None, None)), (35, (32,	None, None), (40, None, None)))
	s = MakeServerSocket()
	conn, addr = s.accept()
	while True:
		for val in YieldBST(T):
			data = conn.recv(1024)
			msg = str(val) + '\n'
			conn.sendall(msg.encode('utf-8'))
		conn.close()
