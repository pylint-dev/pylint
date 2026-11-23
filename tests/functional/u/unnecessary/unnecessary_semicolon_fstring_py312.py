"""Since PEP 701 the text of an f-string is its own FSTRING_MIDDLE token, so a
``;`` at the end of that text is string content, not a statement terminator (#11444)."""
# pylint: disable=invalid-name

b = "value"

# An explicit continuation ends the line without a NEWLINE token, so the last
# token on the line is the f-string's closing quote and the one before it is ``;``.
a = f"{b};" \
""

c = f"{b};" \
    f"{b};" \
    ""

# A real semicolon after an f-string is still reported.
d = f"{b};";  # [unnecessary-semicolon]
# +1: [unnecessary-semicolon]
e = f"{b}";
