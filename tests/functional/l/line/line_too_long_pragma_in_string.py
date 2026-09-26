"""A '#' inside a string must not break the
line-too-long pragma handling.

See issue #11440.
"""

# pylint: disable=invalid-name

# The '#' inside the string is not the pragma start: the
# suppression is real, so nothing is reported for a1.
a1 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa#bbbbbbbbbbbbbbbbbbbbbbbb"  # pylint: disable=line-too-long

# Without the pragma the string content is counted.
# +1: [line-too-long]
a2 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa#bbbbbbbbbbbbbbbbbbbbbbbb"

# A comment before the pragma is skipped over as before.
b1 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # hello # pylint: disable=line-too-long

# A comment without a pragma does not suppress anything.
# +1: [line-too-long]
b2 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # hi
