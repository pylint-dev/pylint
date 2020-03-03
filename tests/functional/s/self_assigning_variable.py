# pylint: disable=missing-docstring,too-few-public-methods
# pylint: disable=unpacking-non-sequence,attribute-defined-outside-init,invalid-name

class Class:
    pass

CLS = Class()
FIRST = 1
# Not enough values on the right hand side
FIRST, SECOND = FIRST
# Not enough values on the left hand side
FIRST = FIRST, SECOND
# Not equivalent to a self assignment
FIRST = (FIRST, )
# Not assigning to an attribute
CLS.FIRST = FIRST
# Not a name on the right hand side
FIRST = Class()
FIRST = FIRST # [self-assigning-variable]
FIRST, SECOND = FIRST, CLS.FIRST # [self-assigning-variable]


FOO = 1
FOO, = [FOO]


class RedefinedModuleLevel:
    FOO = FOO
