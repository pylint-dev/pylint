# pylint: disable=missing-docstring,too-few-public-methods

def baz():  # [disallowed-name]
    pass

class foo():  # [disallowed-name]
    pass

foo = {}.keys()  # [disallowed-name]
foo = 42  # [disallowed-name]
aaa = 42  # [invalid-name]

# Disallowed names are still reported when the assigned value is not a constant,
# while `invalid-name` remains silenced for such names.
toto = {}.keys()  # [disallowed-name]
some_name = {}.keys()

for _ in range(3):
    tata = {}.keys()  # [disallowed-name]
    some_other_name = {}.keys()
