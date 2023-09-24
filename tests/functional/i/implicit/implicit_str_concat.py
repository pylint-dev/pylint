# pylint: disable=invalid-name, missing-docstring, redundant-u-string-prefix, line-too-long, superfluous-parens

# Basic test with a list
TEST_LIST1 = ['a' 'b']  # [implicit-str-concat]
# Testing with unicode strings in a tuple, with a comma AFTER concatenation
TEST_LIST2 = (u"a" u"b", u"c")  # [implicit-str-concat]
# Testing with raw strings in a set, with a comma BEFORE concatenation
TEST_LIST3 = {r'''a''', r'''b''' r'''c'''}  # [implicit-str-concat]
# Testing that only ONE warning is generated when string concatenation happens
# in the middle of a list
TEST_LIST4 = ["""a""", """b""" """c""", """d"""]  # [implicit-str-concat]

print("Lorem ipsum " "dolor sit amet")  # [implicit-str-concat]
print('a', 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb' 'ccc')  # [implicit-str-concat]

# The following shouldn't raise a warning because string literals are
# on different lines
TEST_LIST5 = ('a', 'b'
              'c')

# The following shouldn't raise a warning because of the escaped newline
TEST_LIST6 = ('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb \
              ccc')

# But we should emit when there is an actual juxtaposition
# +1: [implicit-str-concat]
TEST_LIST7 = ('a' 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb \
              ccc')

# No warning for bytes
TEST_LIST8 = [b'A' b'B']

# There's an internal juxtaposition on the second line in a valid multiline
# TODO #6444: raise implicit-str-concat on the second line pylint: disable=fixme
print(
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
    " sed do eiusmod tempor " "incididunt ut labore et dolore "
    "magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea "
)

with open("myfile.txt" "a+b", encoding="utf8") as f:  # [implicit-str-concat]
    content = f.read()
