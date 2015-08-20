# pylint: disable=C0102
'''A little testscript for PEP 3102 and pylint'''
def function(*, foo):
    '''A function for testing'''
    print(foo)

function(foo=1)

foo = 1
function(foo)

function(1)
