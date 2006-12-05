# pylint: disable-msg=W0232,R0903
"""tagging a function as a class method cause a crash when checking for
signature overriding
"""

def fetch_config(mainattr=None):
    """return a class method"""
    @classmethod
    def fetch_order(cls, attr, var):
        """a class method"""
        if attr == mainattr:
            return var
        return None
    return fetch_order

class Aaa:
    """hop"""
    fetch_order = fetch_config('A')

__revision__ = None
