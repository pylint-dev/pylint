"""
'W0601': ('global variable %s undefined at the module level',
          'Used when a variable is defined through the "global" statement \
          but the variable is not defined in the module scope.'),
'W0602': ('Using global for %s but no assignment is done',
          'Used when a variable is defined through the "global" statement \
          but no assignment to this variable is done.'),
'W0603': ('Using the global statement', # W0121
          'Used when you use the "global" statement to update a global \
          variable. PyLint just try to discourage this \
          usage. That doesn\'t mean you can not use it !'),
'W0604': ('Using the global statement at the module level', # W0103
          'Used when you use the "global" statement at the module level \
          since it has no effect'),
"""

__revision__ = ''

CONSTANT = 1

def fix_contant(value):
    """all this is ok, but try not using global ;)"""
    global CONSTANT
    print CONSTANT
    CONSTANT = value
global CSTE # useless
print CSTE # ko

def other():
    """global behaviour test"""
    global HOP
    print HOP # ko

other()


def define_constant():
    """ok but somevar is not defined at the module scope"""
    global somevar
    somevar = 2
