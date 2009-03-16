from os import remove
from glob import glob

code = """
import os

def function():
   retval = %s
   os.write(2, str(retval) + '\\n')

def entry_point(argv):
    function()
    return 0

def target(*args):
    return entry_point, None
"""

msg = "E:  5:function: Using unavailable builtin '%s'"

checks = [
    'set([1, 2, 3])', 'frozenset()',
    'dict()', 'unicode("f")', "complex(3, 4)",
    'file("foo.txt")', 'open("foo.txt")',

    'super(str)', 'object()', 
    
    'raw_input()', 'input()', 'buffer()', 
    
    'vars()', 'locals()', 'globals()', 'dir()',
    
    'getattr(function, "bar")', 'delattr(function, "bar")', 'setattr(function, "bar", "baz")',
    'staticmethod(function)', 'classmethod(function)', 'property(function)',
    
    "reduce(function, [])", "filter(function, [])", 'map(function, [])', 
    'sum(xrange(4))', 'enumerate(range(5))', 
    'sorted(range(5))', 'reversed(range(5))',

    'callable(function)', 'issubclass(function, str)',
    
    'reload(module)',

    'eval("a == b")', 'compile("a==b", "?", "eval")', 'execfile("foo.py")',
    
    'id(function)', 'help(function)',
    
    'intern("foo")',  'round(3.4)', 'iter([])',
    ]


for check in checks:
    builtin, _ = check.split('(', 1)
    if builtin == 'isinstance':
        builtin = 'basestring'
    basename = 'func_nobuiltin_%s' % builtin
    print basename
print 'generated %s test' % len(checks)
