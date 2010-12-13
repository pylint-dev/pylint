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

