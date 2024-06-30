"""Tests for fixme in docstrings"""
# pylint: disable=missing-function-docstring, pointless-string-statement

# +1: [fixme]
"""TODO resolve this"""

"""
FIXME don't forget this # [fixme]
XXX also remember this # [fixme]
??? but not this

    TODO yes this # [fixme]
    FIXME: and this line, but treat it as one FIXME TODO # [fixme]
# TODO not this, however, even though it looks like a comment
also not if there's stuff in front TODO
  XXX spaces are okay though  # [fixme]
"""

# +1: [fixme]
# FIXME should still work

# +1: [fixme]
# TODO """ should work

# """ TODO should not work
"""# TODO neither should this"""

"""TODOist API should not result in a message"""

# +2: [fixme]
"""
TO make something DO: look a regex
"""

# pylint: disable-next=fixme
"""TODO won't work anymore"""

# +2: [fixme]
def function():
    """./TODO implement this"""


'''
  XXX single quotes should be no different # [fixme]
'''
def function2():
    '''
    ./TODO implement this # [fixme]
    FIXME and this # [fixme]
    '''
    '''FIXME one more for good measure''' # [fixme]
