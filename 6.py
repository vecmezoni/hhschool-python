
class Operator():
	'''
	This operator has lowest priority
	'''
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
	def __getattr__(self, name):
		'''
		If operator dont have method we call - we call results method with this name
		and Operator object do not exist anymore
		'''
		if self.left != None and self.right != None:
			return getattr(self.evaluate(), name)
		else:
			raise TypeError()
	def __coerce__(self, other):
		return
	

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

assert (1 |to| 10) * 2 == [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
assert 1 |to| 10 == [1, 2, 3, 4, 5, 6, 7, 8, 9]
assert 1 | 2 |to| 10 * 2 | 1 == [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
assert 1 | 2 |to| 10 | 1 == [3, 4, 5, 6, 7, 8, 9, 10]

