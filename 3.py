class mrange(object):
	"""
	Can handle slice indexing
	mrange(-var) = mrange(0, -var, -1)
	"""
	__slots__ = ['_slice']
	def __init__(self, *args):
		self._slice = slice(*args)
		if self._slice.stop < 0 and self._slice.start is None and self._slice.step is None:
			self._slice = slice(0, self._slice.stop, -1)
	
	@property
	def start(self):
		if self._slice.start is not None:
			return self._slice.start
		return 0
	@property
	def stop(self):
		return self._slice.stop
	@property
	def step(self):
		if self._slice.step is not None:
			return self._slice.step
		return 1

	def __hash__(self):
		return hash(self._slice)
		
	def __cmp__(self, other):
		return (cmp(type(self), type(other)) or cmp(self._slice, other._slice))

	def __repr__(self):
		return 'mrange(%r, %r, %r)' % (self.start, self.stop, self.step)
	
	def __len__(self):
		return self._len()

	def _len(self):
		if abs(self.stop - self.start) % self.step == 0:
			return abs(self.stop - self.start) / abs(self.step)
		else:
			return 1 + abs(self.stop - self.start) / abs(self.step)

	def __getitem__(self, index):
		if isinstance(index, slice):
			start, stop, step = index.indices(self._len())
			return mrange(self._index(start), self._index(stop), step*self.step)
		elif isinstance(index, (int, long)):
			if index < 0:
				fixed_index = index + self._len()
			else:
				fixed_index = index
			if not 0 <= fixed_index < self._len():
				raise IndexError("Index %d out of %r" % (index, self))
			return self._index(fixed_index)
		else:
			raise TypeError("mrange indices must be slices or integers")
	def _index(self, i):
		return self.start + self.step * i
		
assert len(mrange(3)) == len(xrange(3))
assert list(mrange(3)) == list(xrange(3))

assert list(mrange(1, 8, 2)) == list(xrange(1, 8, 2))
assert len(mrange(1, 3)) == len(xrange(1, 3))
assert list(mrange(1, 8, 2)) == list(xrange(1, 8, 2))
assert len(mrange(1, 8, 2)) == len(xrange(1, 8, 2))

assert list(mrange(-3)) == [0, -1, -2]
assert list(mrange(1, -8, -2)) == list(xrange(1, -8, -2))

assert mrange(1, 8, 2)[1:][0] == 3
assert mrange(1, 8, 2)[1:][-1] == 7
assert mrange(1, 8, 2)[:2][0] == 1
assert mrange(1, 8, 2)[:2][-1] == 3
assert mrange(1, 8, 2)[::-1][0] == 7
assert mrange(1, 8, 2)[::-1][-1] == 1
assert mrange(1, 8, 2)[2:0:-1][0] == 5
assert mrange(1, 8, 2)[2:0:-1][-1] == 3