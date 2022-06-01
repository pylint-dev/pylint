"""Tests for bad string format type"""
# pylint: disable=consider-using-f-string, pointless-statement

# Test formatting of bytes
b"test".format(1, 2)  # [no-member]

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

NUM = 0
KEY = "abc"
DICT = {}
CHAR = "f"

f'{NUM:d}'
"{:d}".format(NUM)
f"{NUM:d}"
"{:e}".format(NUM)
f"{NUM:e}"
"{:f}".format(NUM)
f"{NUM:f}"
"{:x}".format(NUM)
f"{NUM:x}"
"{:}".format(NUM)
f"{NUM:}"
"{:s}".format(KEY)
f"{KEY:s}"
"{!s:s}".format([])
f"{[]!s:s}"
"{!s}".format({})
f"{dict!s}"
"{:}".format({})
f"{dict:}"
"{}".format({})
f"{dict}"
"{:e}".format(1.1)
f"{1.1:e}"
"{:e} {:x}".format(1.1, 1)
f"{1.1:e} {1:x}"
"{:#{}}".format(1.1, "f")
f"{1.1:#{CHAR}}"

f'{KEY:d}'  # [bad-string-format-type]
"{:d}".format(KEY)  # [bad-string-format-type]
f"{KEY:d}" # [bad-string-format-type]
"{:x}".format([])  # [bad-string-format-type]
f"{[]:x}" # [bad-string-format-type]
"{:e}".format({})  # [bad-string-format-type]
f"{DICT:e}" # [bad-string-format-type]
"{:d}".format(1.1) # [bad-string-format-type]
f"{1.1:d}" # [bad-string-format-type]
"{!s:x}".format([]) # [bad-string-format-type]
f"{[]!s:x}" # [bad-string-format-type]
"{:x} {:x}".format(1, []) # [bad-string-format-type]
f"{1:x} {[]:x}" # [bad-string-format-type]
"{:#{:e}}".format(1.1, "f") # [bad-string-format-type]
f"{1.1:#{CHAR:e}}" # [bad-string-format-type]


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
