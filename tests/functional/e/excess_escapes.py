# pylint:disable=pointless-string-statement, fixme, comparison-with-itself, comparison-of-constants
"""Stray backslash escapes may be missing a raw-string prefix."""
# pylint: disable=redundant-u-string-prefix


# Bad escape sequences, which probably don't do what you expect.
A = "\[\]\\"  # [anomalous-backslash-in-string,anomalous-backslash-in-string]
assert '\/' == '\\/' # [anomalous-backslash-in-string]
ESCAPE_BACKSLASH = '\`'  # [anomalous-backslash-in-string]

# Valid escape sequences.
NEWLINE = "\n"
OLD_ESCAPES = '\a\b\f\n\t\r\v'
HEX = '\xad\x0a\x0d'
# +1:[anomalous-backslash-in-string,anomalous-backslash-in-string]
FALSE_OCTAL = '\o123\o000'  # Not octal in Python
OCTAL = '\123\000'
NOT_OCTAL = '\888\999'  # [anomalous-backslash-in-string,anomalous-backslash-in-string]
NUL = '\0'
UNICODE = u'\u1234'
HIGH_UNICODE = u'\U0000abcd'
QUOTES = '\'\"'
LITERAL_NEWLINE = '\
'
ESCAPE_UNICODE = "\\\\n"

# Bad docstring
# +3:[anomalous-backslash-in-string]
"""Even in a docstring

You shouldn't have ambiguous text like: C:\Program Files\alpha
"""
