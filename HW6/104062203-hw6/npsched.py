from fifo import FIFO
from minheap import MinHeap
from task import Task
import queue

class NPScheduler:
	def __init__(self, N, policy='SJF'):
		self.N = N   # number of time steps to schedule
		self.running = None
		self.clock = 0
		self.policy = policy
		# instantiate the readyQueue, which may be a FIFO or MinHeap
		# you may need additional queues for 
		# - tasks that have been added but not released yet
		# - tasks that have been completed
		# - the Gantt chart
		if policy == 'RR':
			self.readyQueue = FIFO()
		else:
			self.readyQueue = MinHeap()
		self.notReadyQueue = FIFO()
		self.doneQueue = FIFO()
		self.ganttChart = FIFO()

	def addTask(self, task):
		# if the release time of the new task is not in the future, then
		# put it in ready queue; otherwise, put into not-ready queue.
		# you may need to copy the scheduler policy into the task
		task.setPriorityScheme(self.policy)
		if self.clock < task.releaseTime():
			self.notReadyQueue.put(task)
		else:
			self.readyQueue.put(task)


	def dispatch(self, task):
		# dispatch here means assign the chosen task as the one to run
		# in the current time step.
		# the task should be removed from ready-queue by caller;
		# The task may be empty (None).
		# This method will make an entry into the Gantt chart and perform
		# bookkeeping, including
		# - recording the last dispatched time of this task,
		# - increment the wait times of those tasks not scheduled
		#   but in the ready queue
		self.running = task
		self.ganttChart.put(self.running)
		if self.running is not None:
			self.running.lastDispatchedTime = self.clock
			for r in self.readyQueue:
				r.incrWaitTime()

	def releaseTasks(self):
		'''
			this is called at the beginning of scheduling each time step to see
			if new tasks became ready to be released to ready queue, when their
			release time is no later than the current clock.
		'''
		while True:
			r = self.notReadyQueue.head()
			# assuming the not-Ready Queue outputs by release time
			if r is None or r.releaseTime() > self.clock:
				break
			r = self.notReadyQueue.get()
			r.setPriorityScheme(self.policy)
			self.readyQueue.put(r)

	def checkTaskCompletion(self):
		# if there is a current running task, check if it has just finished.
		# (i.e., decrement remaining time and see if it has more work to do.
		# If so, perform bookkeeping for completing the task, 
		# - move task to done-queue, set its completion time and lastrun time
		# set the scheduler running task to None, and return True
		# (so that a new task may be picked.)
		# but if not completed, return False.
		# If there is no current running task, also return True.
		if self.running is None:
			return True
		# your code here
		else:
			self.running.decrRemaining()
			if self.running.done():
				self.running.setCompletionTime(self.clock)
				self.doneQueue.put(self.running)
				self.running = None
				return True
			else:
				return False

	def schedule(self):
		# scheduler that handles nonpreemptive scheduling.
		# the policy such as RR, SJF, or FCFS is handled by the task as it 
		# defines the attribute to compare (in its __iter__() method)
		# first, check if added but unreleased tasks may now be released
		# (i.e., added to ready queue)
		self.releaseTasks()
		if self.checkTaskCompletion() == False:
			# There is a current running task and it is not done yet!
			# the same task will continue running to its completion.
			# simply redispatch the current running task.
			self.dispatch(self.running)
		else:
			# task completed or no running task.
			# get the next task from priority queue and dispatch it.
			newTask = self.readyQueue.head()
			if newTask is not None:
				newTask = self.readyQueue.get()
				self.dispatch(newTask)
			else:
				self.dispatch(None)


	def clockGen(self):
		for self.clock in range(self.N):
			# now run scheduler here
			self.schedule()
			yield self.clock


	def getSchedule(self):
		return '-'.join(map(str, self.ganttChart))
		# return self.ganttChart

	def getThroughput(self):
		# calculate and return throughput as a tuple
		length = 0
		lastClock = -1
		for r in self.doneQueue:
			if r is not None:
				length = length + 1
				if lastClock < r.completionTime:
					lastClock = r.completionTime
		return (length, lastClock)

	def getWaitTime(self):
		# calculate and return
		waitTime = 0
		length = 0
		for r in self.doneQueue:
			if r is not None:
				length = length + 1
				waitTime = waitTime + r.waitingTime
		return (waitTime, length)

	def getTurnaroundTime(self):
		# calculate the turnaround time in terms of a tuple with
		#  separate turnaround times, #processes
		turnAroundTime = 0
		length = 0
		for r in self.doneQueue:
			if r is not None:
				length = length + 1
				turnAroundTime = turnAroundTime + r.turnaroundTime()
		return (turnAroundTime, length)

def testNPScheduler(tasks, policy):
	# the tuples are release time, cpuBurst, taskName
	nClocks = 20
	scheduler = NPScheduler(nClocks, policy)

	for t in tasks:
		scheduler.addTask(t)

	for clock in scheduler.clockGen():
		pass

	# the next three lines are for testing part 2.5
	thruput = scheduler.getThroughput()
	waittime = scheduler.getWaitTime()
	turnaround = scheduler.getTurnaroundTime()

	print('nonpreemptive %s: %s' % (scheduler.policy, scheduler.getSchedule()))

	# the next line is for testing part 2.5
	print('  thruput = %s = %.2f, waittimes = %s = %.2f, turnaroundtime = %s = %.2f'\
	   % (thruput, thruput[0]/thruput[1],
	      waittime, waittime[0]/waittime[1],
	      turnaround, turnaround[0]/turnaround[1]))

if __name__ == '__main__':
	tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
	print('tasks = %s' % tasks)
	for policy in ['SJF', 'FCFS', 'RR']:
		tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
		testNPScheduler(tasks, policy)
