import inspect


def graph(comp):
	"""
	Decorator for graph compiler
	"""
	def later(function):
		return comp(function)
	return later

def eager_compile(function):
	"""
	Simple compiler, computes all values of map
	"""
	def compiler(map):
		variables = inspect.getargspec(function)[0]
		for var in variables:
			if not map.has_key(var):
				raise KeyError("Key", var, "is missing.")
		dictionary = function(**map)
		return {key: evaluate(key, dictionary, map) for key in dictionary}
	return compiler
	
def lazy_compile(function):
	"""
	Lazy compiler, computes values by call
	"""
	class LazyDictionary(dict):
		def __init__(self, functions, variables):
			self.data = variables
			self.functions = functions
		def __getitem__(self, name):
			if not self.data.has_key(name):
				self.data[name] = evaluate(name, self.functions, self.data)
			return self.data[name]
		def __len__(self):
			return len(self.functions)
		def __str__(self):
			return str({key: 'not yet counted' if not self.data.has_key(key) else self.data[key] for key in self.functions})
		def __iter__(self):
			return self.iterkeys()
		def iteritems(self):
			return iter({key: 'not yet counted' if not self.data.has_key(key) else self.data[key] for key in self.functions}.iteritems())
		def iterkeys(self):
			return iter([key for key in self.functions])

	
	def compiler(map):
		variables = inspect.getargspec(function)[0]
		for var in variables:
			if not map.has_key(var):
				raise KeyError("Key", var, "is missing.")
		dictionary = function(**map)
		return LazyDictionary(dictionary, map)
	return compiler
	
def evaluate(key, dictionary, map = {}):
	"""
	Computes value of a variable.
	"""
	if dictionary.has_key(key):
		arguments = inspect.getargspec(dictionary[key])[0]
	if map.has_key(key):
		return map[key]
	else:
		values = {}
		for arg in arguments:
			map[arg] = evaluate(arg, dictionary, map)
			values[arg] = map[arg]
		map[key] = dictionary[key](**values)
		return map[key]


@graph(eager_compile)	
def stats_graph(xs):
	return {'v': (lambda m, m2: m2 - m**2),
			'n': (lambda xs: len(xs)),
			'm': (lambda xs, n: sum(xs) / n),
			'm2': (lambda xs, n: sum([x**2 for x in xs]) / n)}

assert stats_graph({'xs': [1, 2, 3, 4]}) == {'v': 3, 'n': 4, 'm': 2, 'm2': 7}

def v(m,m2):
	return m2 - m**2

def n(xs):
	return len(xs)
	
def m(xs, n):
	return sum(xs) / n

def m2(xs, n):
	return sum([x**2 for x in xs]) / n
			
@graph(eager_compile)	
def stats_graph_no_lambda(xs):
	return {'v': v,
			'n': n,
			'm': m,
			'm2': m2}
			
assert stats_graph_no_lambda({'xs': [1, 2, 3, 4]}) == {'v': 3, 'n': 4, 'm': 2, 'm2': 7}

@graph(lazy_compile)	
def stats_lazy(xs):
	return {'v': v,
			'n': n,
			'm': m,
			'm2': m2}

s = stats_lazy({'xs': [1, 2, 3, 4]})
assert str(s) == "{'v': 'not yet counted', 'n': 'not yet counted', 'm': 'not yet counted', 'm2': 'not yet counted'}"
assert s['n'] == 4
assert str(s) == "{'v': 'not yet counted', 'n': 4, 'm': 'not yet counted', 'm2': 'not yet counted'}"
assert s['v'] == 3
assert str(s) == "{'v': 3, 'n': 4, 'm': 2, 'm2': 7}"


	