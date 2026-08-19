# pylint: disable=missing-docstring,too-few-public-methods

def baz():  # [disallowed-name]
    pass

class foo():  # [disallowed-name]
    pass

foo = {}.keys()  # [disallowed-name]
foo = 42  # [disallowed-name]
aaa = 42  # [invalid-name]

# Disallowed names are reported when the assigned value is not a constant.
# The lines below with no expected message are the other half of the check:
# they must stay silent because `invalid-name` is still suppressed for these
# names. If that suppression regresses they start emitting `invalid-name`
# ("Constant name ... doesn't conform to UPPER_CASE") and this test fails.
toto = {}.keys()  # [disallowed-name]
some_name = {}.keys()

for _ in range(3):
    tata = {}.keys()  # [disallowed-name]
    some_other_name = {}.keys()
