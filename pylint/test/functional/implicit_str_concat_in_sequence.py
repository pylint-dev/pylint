#pylint: disable=bad-continuation,invalid-name,missing-docstring

# Basic test with a list
TEST_LIST1 = ['a' 'b']  # [implicit-str-concat-in-sequence]
# Testing with unicode strings in a tuple, with a comma AFTER concatenation
TEST_LIST2 = (u"a" u"b", u"c")  # [implicit-str-concat-in-sequence]
# Testing with raw strings in a set, with a comma BEFORE concatenation
TEST_LIST3 = {r'''a''', r'''b''' r'''c'''}  # [implicit-str-concat-in-sequence]
# Testing that only ONE warning is generated when string concatenation happens
# in the middle of a list
TEST_LIST4 = ["""a""", """b""" """c""", """d"""]  # [implicit-str-concat-in-sequence]

# The following shouldn't raise a warning because it is a function call
print('a', 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb' 'ccc')

# The following shouldn't raise a warning because string literals are
# on different lines
TEST_LIST5 = ('a', 'b'
              'c')

# The following shouldn't raise a warning because of the escaped newline
TEST_LIST6 = ('a' 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb \
              ccc')

# No warning for bytes
TEST_LIST7 = [b'A' b'B']
