# pylint: disable=too-few-public-methods
"""Test case for the problem described below :
 - A class extends 'object'
 - This class defines its own __init__()
   * pylint will therefore check that baseclasses' init()
     are called
 - If this class defines an 'object' attribute, then pylint
   will use this new definition when trying to retrieve
   object.__init__()
"""


class Statement:
    """ ... """
    def __init__(self):
        pass
    object = None
