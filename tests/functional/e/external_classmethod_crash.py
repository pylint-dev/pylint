# pylint: disable=no-init,too-few-public-methods,unused-argument,useless-object-inheritance
"""tagging a function as a class method cause a crash when checking for
signature overriding
"""

def fetch_config(mainattr=None):
    """return a class method"""

    def fetch_order(cls, attr, var):
        """a class method"""
        if attr == mainattr:
            return var
        return None
    fetch_order = classmethod(fetch_order)
    return fetch_order

class Aaa(object):
    """hop"""
    fetch_order = fetch_config('A')

__revision__ = None
