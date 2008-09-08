"""test name defined in generator expression are not available
outside the genexpr scope
"""

__revision__ = list(n for n in range(10))
print n
