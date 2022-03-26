import astroid

tree = astroid.parse("a = lambda x: x**2")
tree
