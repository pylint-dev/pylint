"""Tests for fixme in docstrings"""
# pylint: disable=missing-function-docstring, pointless-string-statement

# +1: [fixme]
"""TODO resolve this"""
# +1: [fixme]
""" TODO: indentations are permitted """
# +1: [fixme]
''' TODO: indentations are permitted '''
# +1: [fixme]
"""    TODO: indentations are permitted"""

""" preceding text TODO: is not permitted"""

"""
FIXME don't forget this # [fixme]
XXX also remember this # [fixme]
FIXME: and this line, but treat it as one FIXME TODO # [fixme]
text cannot precede the TODO: it must be at the start
      XXX indentations are okay # [fixme]
??? the codetag must be recognized
"""

# +1: [fixme]
# FIXME should still work

# +1: [fixme]
# TODO """ should work

# """ TODO will not work
"""# TODO will not work"""

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
