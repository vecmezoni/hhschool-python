from functools import wraps

def lazy(decorator):
	"""
	Makes supplied decorator lazy.
	"""
	@wraps(decorator)
	def lazy_decorator(function):
		@wraps(function)
		def decorated(*args, **kwargs):
			return decorator(function)(*args, **kwargs)
		return decorated
	return lazy_decorator

log = []

def logger(function):
	log.append(function.__name__)
	return function

@logger
def dummy():
	return 2
	
assert log == ['dummy']
dummy()
assert log == ['dummy']
dummy()
assert log == ['dummy']

log = []

@lazy
def lazylogger(function):
	log.append(function.__name__)
	return function

@lazylogger
def dummy():
	return 2
	
assert log == []
dummy()
assert log == ['dummy']
dummy()
assert log == ['dummy', 'dummy']
dummy()
assert log == ['dummy', 'dummy', 'dummy']
	
