"""Tests for bad string format type"""
# pylint: disable=consider-using-f-string, pointless-statement

# Test formatting of bytes
b"test".format(1, 2) # [no-member]

# Test format types
"%s" % 1
"%d" % 1
"%f" % 1
"%s" % 1
"%(key)s" % {"key": 1}
"%d" % 1
"%(key)d" % {"key": 1}
"%f" % 1
"%(key)f" % {"key": 1}
"%d" % 1.1
"%(key)d" % {"key": 1.1}
"%s" % []
"%(key)s" % {"key": []}
"%s" % None
"%(key)s" % {"key": None}

# Test incorrect format types
"%d" % "1"  # [bad-string-format-type]
"%(key)d" % {"key": "1"}  # [bad-string-format-type]
"%x" % 1.1  # [bad-string-format-type]
"%(key)x" % {"key": 1.1}  # [bad-string-format-type]
"%d" % []  # [bad-string-format-type]
"%(key)d" % {"key": []}  # [bad-string-format-type]

WORD = "abc"
"%d" % WORD  # [bad-string-format-type]
"%d %s" % (WORD, WORD)  # [bad-string-format-type]

VALUES_TO_FORMAT = (1, "2", 3.0)
"%d %s %f" % VALUES_TO_FORMAT
"%d %d %f" % VALUES_TO_FORMAT  # [bad-string-format-type]


def test_format(my_input_value, my_other_input_value):
    """In some cases it is not possible to determine the content of the input variable.
    Pylint must not crash or yield false positives in such cases.
    """
    print("%d" % my_input_value)
    print("%d %s" % (my_input_value, my_other_input_value))
    to_be_formatted = (my_input_value, my_other_input_value)
    print("%d %s" % to_be_formatted)
