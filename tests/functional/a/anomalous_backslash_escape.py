# pylint:disable=W0105, W0511
"""Test for anomalous backslash escapes in strings"""

BAD_ESCAPE = '\z'  # [anomalous-backslash-in-string]
BAD_ESCAPE_NOT_FIRST = 'abc\z'  # [anomalous-backslash-in-string]
BAD_ESCAPE_WITH_PREFIX = b'abc\z'  # [anomalous-backslash-in-string]
BAD_ESCAPE_WITH_BACKSLASH = b'a\
    \z'  # [anomalous-backslash-in-string]
# +3:[anomalous-backslash-in-string]
BAD_ESCAPE_BLOCK = b'''
    abc
    \z
'''
BAD_ESCAPE_PARENS = (b'abc'
                     b'\z')  # [anomalous-backslash-in-string]
GOOD_ESCAPE = '\b'

# Valid raw strings
BAD_ESCAPE_BUT_RAW = r'\z'

# In a comment you can have whatever you want: \z
