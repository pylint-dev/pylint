"""Checking disallowed names does not report the multiple naming styles.

Module-level names assigned a value that is not a constant are only checked
against ``bad-names``; they must not take part in the multiple naming style
detection, which reports ``invalid-name``.
"""

foo = {}.keys()  # [disallowed-name]
first_name = {}.keys()
second_name = {}.keys()
thirdName = {}.keys()
