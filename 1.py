import inspect

def curry(function, *args, **kwargs):
	if (len(args) + len(kwargs)) >= len(inspect.getargspec(function)[0]):
		return function(*args, **kwargs)
	return lambda *x, **y: curry(function, *(args + x), **dict(kwargs, **y))

@curry
def add(x,y,z,d):
	return x+y+z+d

assert add(1,2,3,4) == 10
assert add(1)(2)(3)(4) == 10
assert add(1,2)(3,4) == 10
assert add(1,2,3)(4) == 10
assert add(1)(2,3)(4) == 10
assert add(x=1)(y=2)(z=3)(d=4) == 10