"""
    'W0104': ('Statement seems to have no effect',
              'Used when a statement doesn\'t have (or at least seems to) \
              any effect.'),
    'W0105': ('String statement has no effect',
              'Used when a string is used as a statement (which of course \
              has no effect). This is a particular case of W0104 with its \
              own message so you can easily disable it if you\'re using \
              those strings as documentation, instead of comments.'),
    'W0106': ('Unnecessary semi-column',
              'Used when a statement is endend by a semi-colon (";"), which \
              isn\'t necessary (that\'s python, not C ;)'),
"""

__revision__ = ''

__revision__

__revision__ <= 1

__revision__.lower() # ok

[i for i in __revision__] # ko


"""inline doc string should use a separated message"""

__revision__.lower(); # unnecessary ;

list() and tuple() # ok
