``\z`` is same as ``\\z`` because there's no escape sequence for ``z``. But it is not clear
for the reader of the code.

Background

Python's string literals use the backslash for their own escape
sequences (like \n for a newline). When Python sees an escape sequence
it doesn't recognize, such as "\." (a literal "dot" character in regex),
it gives a DeprecationWarning.

To avoid this warning, you can use a raw string literal for your regular
expression. Raw string literals don't treat the backslash as a special
character and are often used for regular expressions in Python.

By adding the r before the string, you're telling Python to treat this
as a raw string literal, so it won't try to interpret \. as an escape
sequence and will instead ignore it.

An alternative would be to use double backslash \\. The first backslash
escapes the second one when the string is parsed by python. The second
backslash works as the escape sequence for the . when sent to the regex
engine for parsing. In other words, '\\.' becomes '\.' when parsed by
python, and it can then be used in a regex. The "r" before the string
tells python to treat the string as a "raw" string literal (and not to
modify it).
