from indirect1 import TotoInterface

class AbstractToto:
    __implements__ = TotoInterface

    def helper(self):
        return 'help'
