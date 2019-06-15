# pylint: disable = invalid-name,missing-docstring,unused-variable,unused-argument
def function(hello):
    x, y, z = (1,2,3,) # [bad-whitespace, bad-whitespace]

AAA =1  # [bad-whitespace]
BBB =  2  # [bad-whitespace]
CCC= 1  # [bad-whitespace]
