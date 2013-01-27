def ireduce(function, iterable, initializer = None):
	"""
	Apply function of two arguments cumulatively to the items of iterable, from left to right, so as to reduce the iterable to a single value.
	Returns generator.
	
	If iterable has only one element, the result is iterable[0].

	If iterable more than one elements, the result is f(...f(f(iterable[0], iterable[1]), iterable[2]),...).

	If iterable is empty and no initial value was provided, the function raises a TypeError exception.
	"""
	it = iter(iterable)
	if initializer is None:
		try:
			initializer = next(it)
		except StopIteration:
			raise TypeError('ireduce() of empty sequence with no initial value')
	accum_value = initializer
	yield accum_value
	for x in it:
		accum_value = function(accum_value, x)
		flag = True
		yield accum_value

red = ireduce(lambda x, y: x + y, [1,2,3,4])
assert list(red) == [3, 6, 10]

red = ireduce(lambda x, y: x + y, [1,2,3,4])
assert next(red) == 3
assert next(red) == 6
assert next(red) == 10

red = ireduce(lambda x, y: x + y, [1,2,3,4], 15)
assert list(red) == [16, 18, 21, 25]

red = ireduce(lambda x, y: x + y, [1,2,3,4], 15)
assert next(red) == 16
assert next(red) == 18
assert next(red) == 21
assert next(red) == 25
