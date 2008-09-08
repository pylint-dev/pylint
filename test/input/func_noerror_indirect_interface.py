"""shows a bug where pylint can't find interfaces when they are
used indirectly. See input/indirect[123].py for details on the
setup"""

__revision__ = None

from input.indirect2 import AbstractToto

class ConcreteToto(AbstractToto):
    """abstract to implements an interface requiring machin to be defined"""
    def __init__(self):
        self.duh = 2
    
    def machin(self):
        """for ifacd"""
        return self.helper()*2
