import unittest

class mrange(object):
    """
    Can handle slice indexing, contains, index method, comparement, can be reversed
    """
    __slots__ = ['_slice','_len']
    def __init__(self, *args):
        if len(args) == 1:
            start, stop, step = 0, args[0], 1
        elif len(args) == 2:
            start, stop, step = args[0], args[1], 1
        elif len(args) == 3:
            start, stop, step = args
        else:
            raise TypeError('mrange() requires one, two or three int arguments')
        try:
            start, stop, step = int(start), int(stop), int(step)
        except ValueError:
            raise TypeError('an integers are required')
        if step == 0:
            raise ValueError('mrange() third argument must not be zero')
        elif step < 0:
            stop = min(stop, start)
        else:
            stop = max(stop, start)
        self._slice = slice(start, stop, step)
        self._len = (stop - start) // step + bool((stop - start) % step)
    
    @property
    def start(self):
        return self._slice.start

    @property
    def stop(self):
        return self._slice.stop

    @property
    def step(self):
        return self._slice.step

    def __hash__(self):
        return hash(self._slice)
        
    def __cmp__(self, other):
        return (cmp(type(self), type(other)) or cmp(self._slice, other._slice))

    def __repr__(self):
        if self.start == 0 and self.step == 1:
            return 'mrange(%d)' % self.stop
        elif self.step == 1:
            return 'mrange(%d, %d)' % (self.start, self.stop)
        return 'mrange(%d, %d, %d)' % (self.start, self.stop, self.step)

    def __len__(self):
        return self._len

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            if step == 0:
                raise ValueError('slice step cannot be 0')

            start = start or self.start
            stop = stop or self.stop
            if start < 0:
                start = max(0, start + self._len)
            if stop < 0:
                stop = max(start, stop + self._len)
            if step is None or step > 0:
                return mrange(start, stop, step or 1)
            else:
                rev = reversed(self)
                rev._slice = slice(rev._slice.start, rev._slice.stop, step)
                return rev
        elif isinstance(index, (int, long)):
            if index < 0:
                index = self._len + index
            if index < 0 or index >= self._len:
                raise IndexError('mrange object index out of range')
            return self.start + index * self.step
        else:
            raise TypeError("mrange indices must be slices or integers")

    def index(self, value):
        diff = value - self.start
        quotient, remainder = divmod(diff, self.step)
        if remainder == 0 and 0 <= quotient < self._len:
            return abs(quotient)
        raise ValueError('%r is not in range' % value)

    def __contains__(self, value):
        try:
            self.index(value)
            return True
        except ValueError:
            return False

    def __reversed__(self):
        sign = self.step / abs(self.step)
        last = self.start + ((self._len - 1) * self.step)
        return mrange(last, self.start - sign, -1 * self.step)
        
def getitem(obj, index):
    return obj[index]

class MrangeTests(unittest.TestCase):

    def test_init(self):
        r = mrange(0)
        self.assertEqual(0, r.start)
        self.assertEqual(0, r.stop)
        self.assertEqual(1, r.step)

        r = mrange(1)
        self.assertEqual(0, r.start)
        self.assertEqual(1, r.stop)
        self.assertEqual(1, r.step)

        r = mrange(2)
        self.assertEqual(0, r.start)
        self.assertEqual(2, r.stop)
        self.assertEqual(1, r.step)

        r = mrange(1, 2)
        self.assertEqual(1, r.start)
        self.assertEqual(2, r.stop)
        self.assertEqual(1, r.step)

        r = mrange(1, 2, 1)
        self.assertEqual(1, r.start)
        self.assertEqual(2, r.stop)
        self.assertEqual(1, r.step)

        r = mrange(2, 2, 1)
        self.assertEqual(2, r.start)
        self.assertEqual(2, r.stop)
        self.assertEqual(1, r.step)

        r = mrange(1, 2, -1)
        self.assertEqual(1, r.start)
        self.assertEqual(1, r.stop)
        self.assertEqual(-1, r.step)

        r = mrange(2, 1, -1)
        self.assertEqual(2, r.start)
        self.assertEqual(1, r.stop)
        self.assertEqual(-1, r.step)

        self.assertRaises(TypeError, mrange, 1, 2, 3, 4)
        self.assertRaises(TypeError, mrange, 'abc')
        self.assertRaises(ValueError, mrange, 1, 2, 0)

    def test_repr(self):
        self.assertEqual(repr(mrange(1)), 'mrange(1)')
        self.assertEqual(repr(mrange(1, 2)), 'mrange(1, 2)')
        self.assertEqual(repr(mrange(1, 3, 2)), 'mrange(1, 3, 2)')

    def test_contains(self):
        r = mrange(5)
        self.assertFalse(-1 in r)
        self.assertTrue(1 in r)
        self.assertTrue(4 in r)
        self.assertFalse(5 in r)

        r = mrange(0, 5, 2)
        self.assertFalse(-1 in r)
        self.assertTrue(0 in r)
        self.assertFalse(1 in r)
        self.assertTrue(2 in r)
        self.assertFalse(3 in r)
        self.assertTrue(4 in r)
        self.assertFalse(5 in r)

        r = mrange(5, 0, -1)
        self.assertFalse(-1 in r)
        self.assertFalse(0 in r)
        self.assertTrue(1 in r)
        self.assertTrue(2 in r)
        self.assertTrue(3 in r)
        self.assertTrue(4 in r)
        self.assertTrue(5 in r)
        self.assertFalse(6 in r)

    def test_iter_basic(self):
        self.assertEqual(
            [],
            [x for x in mrange(0)])

        self.assertEqual(
            [0],
            [x for x in mrange(1)])

        self.assertEqual(
            [0, 1, 2],
            [x for x in mrange(3)])

        self.assertEqual(
            [0, 2, 4],
            [x for x in mrange(0, 5, 2)])

        self.assertEqual(
            [5, 3, 1],
            [x for x in mrange(5, 0, -2)])

        iterator = iter(mrange(5))
        self.assertTrue(iterator is iter(iterator))

    def test_index(self):
        r = mrange(1)
        self.assertEqual(0, r.index(0))
        self.assertRaises(ValueError, r.index, -1)
        self.assertRaises(ValueError, r.index, 1)

        r = mrange(10)
        self.assertEqual(4, r.index(4))
        self.assertEqual(9, r.index(9))
        self.assertRaises(ValueError, r.index, -1)
        self.assertRaises(ValueError, r.index, 10)

        r = mrange(3, 6)
        self.assertEqual(0, r.index(3))
        self.assertEqual(2, r.index(5))
        self.assertRaises(ValueError, r.index, 2)
        self.assertRaises(ValueError, r.index, 6)

        r = mrange(3, 6, 2)
        self.assertEqual(0, r.index(3))
        self.assertEqual(1, r.index(5))
        self.assertRaises(ValueError, r.index, 2)
        self.assertRaises(ValueError, r.index, 6)

        r = mrange(5, 2, -1)
        self.assertEqual(2, r.index(3))
        self.assertEqual(0, r.index(5))
        self.assertRaises(ValueError, r.index, 2)
        self.assertRaises(ValueError, r.index, 6)

        r = mrange(5, 2, -2)
        self.assertEqual(1, r.index(3))
        self.assertEqual(0, r.index(5))
        self.assertRaises(ValueError, r.index, 2)
        self.assertRaises(ValueError, r.index, 6)

    def test_reversed(self):
        self.assertEqual(reversed(mrange(1)), mrange(0, -1, -1))
        self.assertEqual(reversed(mrange(5)), mrange(4, -1, -1))
        self.assertEqual(reversed(mrange(1, 5)), mrange(4, 0, -1))
        self.assertEqual(reversed(mrange(5, 1, -1)), mrange(2, 6, 1))

    def test_getitem(self):
        r = mrange(0)
        self.assertRaises(IndexError, getitem, r, -1)
        self.assertRaises(IndexError, getitem, r, 0)
        self.assertRaises(IndexError, getitem, r, 1)

        r = mrange(1)
        self.assertRaises(IndexError, getitem, r, -2)
        self.assertEqual(0, r[-1])
        self.assertEqual(0, r[0])
        self.assertRaises(IndexError, getitem, r, 1)

        r = mrange(3)
        self.assertRaises(IndexError, getitem, r, -4)
        self.assertEqual(0, r[-3])
        self.assertEqual(2, r[-1])
        self.assertEqual(0, r[0])
        self.assertEqual(2, r[2])
        self.assertRaises(IndexError, getitem, r, 3)

        r = mrange(1, 4)
        self.assertRaises(IndexError, getitem, r, -4)
        self.assertEqual(1, r[-3])
        self.assertEqual(3, r[-1])
        self.assertEqual(1, r[0])
        self.assertEqual(3, r[2])
        self.assertRaises(IndexError, getitem, r, 3)

        r = mrange(3, 0, -1)
        self.assertRaises(IndexError, getitem, r, -4)
        self.assertEqual(3, r[-3])
        self.assertEqual(1, r[-1])
        self.assertEqual(3, r[0])
        self.assertEqual(1, r[2])
        self.assertRaises(IndexError, getitem, r, 3)

    def test_getitem_slice(self):
        r = mrange(10)

        self.assertRaises(ValueError, getitem, r, slice(1, 2, 0))

        self.assertEqual(r[:], mrange(10))
        self.assertEqual(r[::], mrange(10))
        self.assertEqual(r[::1], mrange(10))
        self.assertEqual(r[::2], mrange(0, 10, 2))

        self.assertEqual(r[::-1], mrange(9, -1, -1))
        self.assertEqual(r[::-2], mrange(9, -1, -2))

        self.assertEqual(r[1:2], mrange(1, 2))
        self.assertEqual(r[1:9], mrange(1, 9))
        self.assertEqual(r[1:-1], mrange(1, 9))

        self.assertEqual(r[-20:-1], mrange(0, 9))
        self.assertEqual(r[-20:-19], mrange(0, 0))

    def test_len(self):
        r = mrange(0)
        self.assertEqual(0, len(r))

        r = mrange(1)
        self.assertEqual(1, len(r))

        r = mrange(10)
        self.assertEqual(10, len(r))

        r = mrange(3, 5)
        self.assertEqual(2, len(r))

        r = mrange(3, 5, 2)
        self.assertEqual(1, len(r))

        r = mrange(5, 3, -1)
        self.assertEqual(2, len(r))

        r = mrange(5, 3, -2)
        self.assertEqual(1, len(r))

    def test_large_nums(self):
        r = mrange(2**64 + 1)
        self.assertEqual(r._len, 2**64 + 1)
        self.assertEqual(r[0], 0)
        self.assertEqual(r[-1], 2**64)

if __name__ == '__main__':
    unittest.main()