import inspect

class KeywordMissing(BaseException):
	pass
	
def graph(function, map = {}):
	if (len(map)) >= function.__code__.co_argcount:
		for var in function.__code__.co_varnames:
			if not map.has_key(var):
				raise KeywordMissing(var)
		result = {}
		lambdas = function(**map)
		stack = {}
		while len(lambdas) > 0 or len(stack) > 0:
			if len(lambdas) == 0:
				lambdas = stack
				stack = {}
			l = lambdas.popitem()
			if len(set(inspect.getargspec(l[1])[0]) & map.viewkeys()) < len(inspect.getargspec(l[1])[0]):
				stack.update({l[0]: l[1]})
			else:
				temp = {l[0]: l[1](**{key: map[key] for key in inspect.getargspec(l[1])[0]})}
				result.update(temp)
				map.update(temp)
		return result
	return lambda map: graph(function, map)	
	
@graph	
def stats_graph(xs):
	return {'v': (lambda m, m2: m2 - m**2),
			'n': (lambda xs: len(xs)),
			'm': (lambda xs, n: sum(xs) / n),
			'm2': (lambda xs, n: sum([x**2 for x in xs]) / n)}
			
print stats_graph({'xs': [1,2,3,4]})


	