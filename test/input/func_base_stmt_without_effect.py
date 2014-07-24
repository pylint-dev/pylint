"""
    'W0104': ('Statement seems to have no effect',
              'Used when a statement doesn\'t have (or at least seems to) \
              any effect.'),
    'W0105': ('String statement has no effect',
              'Used when a string is used as a statement (which of course \
              has no effect). This is a particular case of W0104 with its \
              own message so you can easily disable it if you\'re using \
              those strings as documentation, instead of comments.'),
    'W0106': ('Expression "%s" is assigned to nothing',
              'Used when an expression that is not a function call is assigned\
              to nothing. Probably something else was intended.'),
"""
# pylint: disable=too-few-public-methods
__revision__ = ''

__revision__

__revision__ <= 1

__revision__.lower() # ok

[i for i in __revision__] # ko


"""inline doc string should use a separated message"""

__revision__.lower(); # unnecessary ;

list() and tuple() # W0106

def to_be():
    """return 42"""
    return "42"

ANSWER = to_be() # ok
ANSWER == to_be() # W0106, typical typo

to_be() or not to_be() # W0106, strange conditional function call (or nonsens)
to_be().title # W0106, very strange, maybe typo

GOOD_ATTRIBUTE_DOCSTRING = 42
"""Module level attribute docstring is fine. """

class ClassLevelAttributeTest(object):
    """ test attribute docstrings. """

    good_attribute_docstring = 24
    """ class level attribute docstring is fine either. """
    second_good_attribute_docstring = 42
    # Comments are good.

    # empty lines are good, too.
    """ Still a valid class level attribute docstring. """

    def __init__(self):
        self.attr = 42
        """ Good attribute docstring """
        attr = 24
        """ Still a good __init__ level attribute docstring. """
        val = 0
        for val in range(42):
            val += attr
        """ Invalid attribute docstring """
        self.val = val

    def test(self):
        """ invalid attribute docstrings here. """
        self.val = 42
        """ this is an invalid attribute docstring. """
    