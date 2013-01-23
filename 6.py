class Operator:
	def __init__(self, function):
		self.function = function
	def __ror__(self, other):
		return Operator(lambda x, self=self, other=other: self.function(other, x))
	def __or__(self, other):
		return self.function(other)
		
def isSubset(x,y):
	for item in x:
		if item not in y:
			return False
	return True
		
x = Operator(isSubset)

assert ['a','b','e'] |x| ['c','b','a','d'] == False
assert ['a','b','c'] |x| ['c','b','a','d'] == True
assert "rts" |x| "string" == True

to = Operator(lambda x, y: range(x,y))

assert 1 |to| 10 == [1, 2, 3, 4, 5, 6, 7, 8, 9]
