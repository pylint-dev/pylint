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
