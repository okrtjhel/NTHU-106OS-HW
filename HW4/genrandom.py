import random
LEN = 20000000
L = list(range(LEN))
random.shuffle(L)
fh = open("randomInt.txt", "w")
# first write is the length
fh.write(str(LEN)+'\n')
for i in L:
	fh.write(str(i)+'\n')
fh.close()
