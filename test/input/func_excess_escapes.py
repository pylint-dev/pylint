# pylint:disable=W0105, W0511
"""Stray backslash escapes may be missing a raw-string prefix."""

__revision__ = '$Id$'

# Bad escape sequences, which probably don't do what you expect.
A = "\[\]\\"
assert '\/' == '\\/'
ESCAPE_BACKSLASH = '\`'

# Valid escape sequences.
NEWLINE = "\n"
OLD_ESCAPES = '\a\b\f\n\t\r\v'
HEX = '\xad\x0a\x0d'
OCTAL = '\o123\o000'
UNICODE = u'\u1234'
HIGH_UNICODE = u'\U0000abcd'
QUOTES = '\'\"'
LITERAL_NEWLINE = '\
'
ESCAPE_UNICODE = "\\\\n"

# Bad docstring
"""Even in a docstring

You shouldn't have ambiguous text like: C:\Program Files\alpha
"""

# Would be valid in Unicode, but probably not what you want otherwise
BAD_UNICODE = '\u0042'
BAD_LONG_UNICODE = '\U00000042'
BAD_NAMED_UNICODE = '\N{GREEK SMALL LETTER ALPHA}'

GOOD_UNICODE = u'\u0042'
GOOD_LONG_UNICODE = u'\U00000042'
GOOD_NAMED_UNICODE = u'\N{GREEK SMALL LETTER ALPHA}'


# Valid raw strings
RAW_BACKSLASHES = r'raw'
RAW_UNICODE = ur"\u0062\n"

# In a comment you can have whatever you want: \ \\ \n \m
# even things that look like bad strings: "C:\Program Files"
