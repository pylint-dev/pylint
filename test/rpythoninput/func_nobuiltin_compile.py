
import os

def function():
   retval = compile("a==b", "?", "eval")
   os.write(2, str(retval) + '\n')

def entry_point(argv):
    function()
    return 0

def target(*args):
    return entry_point, None
