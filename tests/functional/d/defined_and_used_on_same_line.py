"""Check for definitions and usage happening on the same line."""
#pylint: disable=missing-docstring,multiple-statements,wrong-import-position,unnecessary-comprehension,unspecified-encoding,unnecessary-lambda-assignment

print([index
       for index in range(10)])

print((index
       for index in range(10)))

filter_func = lambda x: not x

def func(xxx): return xxx

def func2(xxx): return xxx + func2(1)

import sys; print(sys.exc_info())

for i in range(10): print(i)

j = 4; lamb = lambda x: x+j

func4 = lambda a, b: a != b

# test https://www.logilab.org/ticket/6954:

with open('f') as f: print(f.read())

with open('f') as f, open(f.read()) as g:
    print(g.read())
