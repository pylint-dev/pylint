"""test global statement"""

__revision__ = 0

exec('a = __revision__')
exec('a = 1', globals={})

exec('a = 1', globals=globals())

def func():
    """exec in local scope"""
    exec('b = 1')

