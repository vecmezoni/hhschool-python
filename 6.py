	

class Operator(object):
	def __init__(self, function, left = None, right = None):
		self.function = function
		self.left = left
		self.right = right
	def evaluate(self):
		return self.function(self.left,self.right)
	def __ror__(self, other):
		self.left = other
		return Operator(self.function, self.left, self.right)
	def __or__(self, other):	
		if self.right != None:
			self.right = self.right | other
		else:
			self.right = other
		return Operator(self.function, self.left, self.right)
	def __lt__(self, other):
		return self.function(self.left,self.right) < other
	def __le__(self, other):
		return self.function(self.left,self.right) <= other
	def __eq__(self, other):
		return self.function(self.left,self.right) == other
	def __ne__(self, other):
		return self.function(self.left,self.right) != other
	def __gt__(self, other):
		return self.function(self.left,self.right) > other
	def __ge__(self, other)	:
		return self.function(self.left,self.right) >= other
	def __str__(self):
		return str(self.function(self.left,self.right))
	def __getattr__(self, name):
		if self.left != None and self.right != None:
			return self.evaluate().__getattribute__(name)


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
assert 1 | 2 |to| 10 | 1 == [3, 4, 5, 6, 7, 8, 9, 10]

