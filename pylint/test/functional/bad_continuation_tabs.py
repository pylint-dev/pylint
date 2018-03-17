"""Regression test case for bad-continuation with tabs"""
# pylint: disable=too-few-public-methods,missing-docstring,invalid-name,unused-variable
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
		self.d(
			c)

	def d(self, e):
		self.b(
		       e)  # [bad-continuation]

	def f(self):
		return [
			self.b,
			self.d
		]

	def g(self):
		return [self.b,
		        self.d
		]  # [bad-continuation]

	def h(self):
		return [self.b,
		        self.d
		        ]

	def i(self):
		return [self.b,
		        self.d
		       ]
