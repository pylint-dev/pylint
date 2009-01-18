"""Test that decorators sees the class namespace - just like
function default values does but function body doesn't.

https://www.logilab.net/elo/ticket/3711 - bug finding decorator arguments 
https://www.logilab.net/elo/ticket/5626 - name resolution bug inside classes
"""
 
class Test:

    ident = lambda x: x

    @ident(ident)
    def f(self, val=ident(7), f=ident):
        return f(val)

print Test().f()
