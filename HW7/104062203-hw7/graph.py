# -*- coding: utf8 -*-
# graph.py
# 陳涵宇, 104062203
# this is template code for graph and DFS

class Graph:
	def __init__(self, G):
		'''
			G is a dictionary of adjacency list that maps each vertex u (string)
			to a list of vertices v (so (u, v) is an edge)
		'''
		self.G = G
		self.vertices = list(G.keys())

	def Adj(self, v):
		'''iterator for the adjacency list'''
		for i in self.G[v]:
			yield i

	def V(self):
		'''iterator for the vertices'''
		for i in self.vertices:
			yield i

	def findCycle(self):
		'''
			your code to return a list of vertice that form a cycle
			by calling a modified version of DFS or some other algorithm.
		'''
		self.found_cycle = False
		self.cycle = []
		DFS(self)
		if self.found_cycle is False:
			self.cycle = []

		return self.cycle # return None for now but you should return list


### Code for DFS ###
# you may want to adopt it into the Graph class or keep it as separate code.

WHITE = 'white'
GRAY =  'gray'
BLACK = 'black'


def DFS(G):
	G.color = {} # color, which is WHITE, GRAY, or BLACK
	G.pred = {}  # the predecessor
	# you may add your own field for tracking cycles
	for u in G.V():
		G.color[u] = WHITE
		G.pred[u] = None
	for u in G.V():
		if G.color[u] == WHITE:
			DFSVisit(G, u)

def DFSVisit(G, u):
	if G.found_cycle:
		return
	G.cycle.append(u)
	G.color[u] = GRAY
	for v in G.Adj(u):
		if G.color[v] == GRAY and G.found_cycle is False:
			G.cycle.append(v)
			G.found_cycle = True
			return
		if G.color[v] == WHITE and G.found_cycle is False:
			G.pred[v] = u
			DFSVisit(G, v)
	# add your own code for cycle detection
	G.color[u] = BLACK
	if G.found_cycle is False:
		G.cycle.pop()

# our test case. Define a dictionary of adjacency lists for each vertex.

if __name__ == '__main__':
	L = [
	{'P1':['R1'], 'P2':['R3', 'R4', 'R5'], 'P3': ['R5'], 'P4': ['R2'],
	'P5': [], 'R1':['P2'], 'R2': ['P1'], 'R3': ['P5'], 'R4': ['P3'], 
	'R5': ['P4'] },
	{'P1': ['P2'], 'P2': ['P3', 'P4', 'P5'], 'P3':['P4'], 
	'P4': ['P1'], 'P5': [] }
	]

	for g in map(Graph, L):
		print('g=%s, cycle=%s' % (g.G, g.findCycle()))