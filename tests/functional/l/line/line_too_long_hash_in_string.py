"""A # in a string literal starts no comment (#11440).

The pragma that turns line-too-long off, and that is
removed before the line is measured, has to be found
in the real trailing comment.
"""
# pylint: enable=useless-suppression

# The string holds a #, and the line is too long even
# without the pragma, so the suppression is useful.
PATTERN = "xxxxxxxxxxxxxxxx#yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"  # pylint: disable=line-too-long

# The pragma is looked for in the trailing comment, so one
# inside the string before it does not count.
TEXT = "a # pylint: disable=line-too-long in a string, not a comment"  # [line-too-long]

# A short line with a # in its string does not need it.
# +1: [useless-suppression]
SHORT = "a#b"  # pylint: disable=line-too-long
