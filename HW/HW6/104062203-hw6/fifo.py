class FIFO:
   def __init__(self, initList=[]):
      self.A = list(initList)
   def get(self):
      return self.A.pop(0)
   def put(self, val):
      self.A.append(val)
   def head(self):
      return len(self.A) and self.A[0] or None
   def __iter__(self):
      for i in self.A:
         yield i
   def __len__(self):
      return len(self.A)
   def __repr__(self):
      return repr(self.A)

if __name__ == '__main__':
   f = FIFO(range(3))
   print("%s, expect %s" % (repr(f), '[0, 1, 2]'))
   f.put(6)
   print("f.put(6), f.get() = %d, expect 0" % f.get())
   print("f.head() = %d, expect 1" % f.head())
   print("len(f) = %d, expect 3" % len(f))

