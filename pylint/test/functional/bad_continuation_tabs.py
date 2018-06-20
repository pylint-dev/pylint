"""Regression test case for bad-continuation with tabs"""
# pylint: disable=too-few-public-methods,missing-docstring,invalid-name,unused-variable, useless-object-inheritance
# Various alignment for brackets

# Issue 638
TEST1 = ["foo",
         "bar",
         "baz"
         ]

MY_LIST = [
	1, 2, 3,
	4, 5, 6
	]

# Issue 1148
class Abc(object):
	def b(self, c):
		# bock indentation
		self.d(
			c)  # (is: tabs only)

	def d(self, e):
		# bad hanging indentation
		self.b(
		       e)  # [bad-continuation] (is: 2 tabs + 7 spaces)

	def f(self):
		# block indentiation (is: all tabs only)
		return [
			self.b,
			self.d
		]

	def g(self):
		# bad hanging indentation
		# the closing ] requires 7 - 8 more spcaes; see h(), i()
		return [self.b,
		        self.d  # (is: 2 tabs + 8 spaces)
		]  # [bad-continuation] (is: tabs only)

	def h(self):
		# hanging indentation: all lined up with first token 'self.b'
		return [self.b,
		        self.d # (is: 2 tabs + 8 spaces)
		        ] # (is: 2 tabs + 8 spaces)

	def i(self):
		# hangin identation: closing ] lined up with opening [
		return [self.b,
		        self.d   # (2 tabs + 8 spaces)
		       ]  # (2 tabs + 7 spaces)
