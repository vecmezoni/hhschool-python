from math import sqrt
eratosthenes = lambda n: [x for x in xrange(2,n) if not any ([y for y in xrange(2,1+int(sqrt(x))) if not x%y])]
assert eratosthenes(2) == []
assert eratosthenes(3) == [2]
assert eratosthenes(4) == [2,3]
assert eratosthenes(30) == [2,3,5,7,11,13,17,19,23,29]