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

msg = "E:  3:function: Using unavailable builtin '%s'"

checks = [
    'set([1, 2, 3]', 'frozenset()', 'file("foo.txt")', 'open("foo.txt")',
    'dict()', 'unicode("f")', "complex(3, 4)",

    
    'raw_input()', 'input()', 
    'vars()', 'locals()', 'globals()', 'dir()',
    'issubclass(function, str)',
    'getattr(function, "bar")', 'delattr(function, "bar")', 'setattr(function, "bar", "baz")',
    'sum(xrange(4))', 'enumerate(range(5))', 

    'reload(module)', 'callable(function)','eval("a == b")',
    'execfile("foo.py")',

    'compile("a==b", "?", "eval")',
    "reduce(function, [])", "filter(function, [])",

    'id(function)', 'help(function)',
    'isinstance("foo", basestring)' # test basestring, not isinstance
    'staticmethod(function)', 'classmethod(function)', 'property(function)',
    'round(3.4)', 'iter([])',
    'sorted(range(5))', 'reversed(range(5))',
    'intern("foo")', 
    'buffer()', 'map(function, [])', 'super(str)',
    'object()', 
    ]



for filename in glob('rpythoninput/func_nobuiltin_*'):
    remove(filename)
for filename in glob('rpythonmessages/func_nobuiltin_*'):
    remove(filename)    
for check in checks:
    builtin, _ = check.split('(', 1)
    basename = 'func_nobuiltin_%s' % builtin
    file('rpythoninput/%s.py' % basename, 'w').write(code % check)
    file('rpythonmessages/%s.txt' % basename, 'w').write(msg % builtin)

