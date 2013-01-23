def ireduce(function, iterable, initializer=None):
	it = iter(iterable)
	if initializer is None:
		try:
			initializer = next(it)
		except StopIteration:
			raise TypeError('ireduce() of empty sequence with no initial value')
	accum_value = initializer
	for x in it:
		accum_value = function(accum_value, x)
		yield accum_value