"""Test the superfluous-parens warning with python 3.8 functionality (walrus operator)"""
# pylint: disable=missing-function-docstring, invalid-name, missing-class-docstring, import-error, pointless-statement,named-expr-without-context
import numpy

# Test parens in if statements
if not (x := False):
    print(x)

if not (foo := 5):
    pass

A = 1
if odd := isinstance(A, int):
    pass

if not ((x := 1)):  # [superfluous-parens]
    pass

if ((x := A)):   # [superfluous-parens]
    pass

if not ((x := A)):  # [superfluous-parens]
    pass

if not ((((x := 1)))):  # [superfluous-parens]
    pass

# Test assertions
assert (ret := str(42))

# Teast 2D arrays with numpy (since they allow commas within indexing)
ARRAY_2D = numpy.zeros((3, 3), dtype=bool)
E = not (vals := ARRAY_2D[:, :].all())
F = not (vals := ARRAY_2D[2, 2].all())
G = not (vals := ARRAY_2D[::].all())
H = not (vals := ARRAY_2D[2:2].all())

# Test yield
class TestYieldClass:
    @classmethod
    def function_A(cls):
        yield (var := 1 + 1)
        print(var)

    @classmethod
    def function_B(cls):
        yield str(1 + 1)

    @classmethod
    def function_C(cls):
        yield (1 + 1) # [superfluous-parens]


if (x := "Test " + "String"):
    print(x)

if (x := ("Test " + "String")):  # [superfluous-parens]
    print(x)

if not (foo := "Test " + "String" in "hello"):
    print(foo)

if not (foo := ("Test " + "String") in "hello"):  # [superfluous-parens]
    print(foo)

assert (ret := "Test " + "String")
assert (ret := ("Test " + "String"))  # [superfluous-parens]

(walrus := False)
(walrus := (False))  # [superfluous-parens]

(hi := ("CONST"))  # [superfluous-parens]
(hi := ("CONST",))
