# pylint: disable=C0121
"""http://www.logilab.org/ticket/124337"""

import gtk

def print_some_constant(arg=gtk.BUTTONS_OK):
    """crash because gtk.BUTTONS_OK, a gtk enum type, is returned by
    astroid as a constant
    """
    print arg

