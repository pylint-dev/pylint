"""Like f-strings since PEP 701, the text of a template string (PEP 750) is its
own TSTRING_MIDDLE token, so a ``;`` at the end of that text is string content,
not a statement terminator (#11444)."""
# pylint: disable=invalid-name

b = "value"

# An explicit continuation ends the line without a NEWLINE token, so the last
# token on the line is the t-string's closing quote and the one before it is ``;``.
a = t"{b};" \
t""

c = t"{b};" \
    t"{b};" \
    t""

# A real semicolon after a t-string is still reported.
d = t"{b};";  # [unnecessary-semicolon]
# +1: [unnecessary-semicolon]
e = t"{b}";
