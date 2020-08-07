from fifo import FIFO
from minheap import MinHeap
from task import Task
from npsched import NPScheduler, testNPScheduler
from psched import PScheduler, testPScheduler


if __name__ == '__main__':
	tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
	print('tasks = %s' % tasks)
	for policy in ['SJF', 'FCFS', 'RR']:
		tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
		testNPScheduler(tasks, policy)
		tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
		testPScheduler(tasks, policy)
