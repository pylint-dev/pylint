"""Test for consider-using-any-all
This refactoring message is emitted when pylint detects boolean expression like
a or b or c which can be refactored to any([a, b, c]). Similarly multiple `and`
operations can be refactored using `all` function."""

# pylint: disable=invalid-name, undefined-variable, too-many-boolean-expressions

a = True
b = True
c = True

if a or b or c: # [consider-using-any-all]
    print('atleast something is true')

if a and b and c and get_foo():   # [consider-using-any-all]
    print('all values are true')

# for or there is only single operand d, therefore does not emit msg for it
if a and b and c and get_foo() or d:    # [consider-using-any-all]
    print('For we live by faith, not by sight.')

if a == b and c or d or e or f or b == c:    # [consider-using-any-all]
    print("The pain that you've been feeling, can't compare to the joy that's coming.")

# only d and e qualify for iterable in any, however currently we emit this message
# only if there are more than 2 named variable in bool op with same operator.
if a == b and c or d or e or b == c:
    pass
