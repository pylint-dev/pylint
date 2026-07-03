This check only works for old-style string formatting using the '%' operator.

This check only works if the dictionary with the values to be formatted is defined inline.
Passing a variable will not trigger the check as the other keys in this dictionary may be
used in other contexts, while an inline defined dictionary is clearly only intended to hold
the values that should be formatted.
