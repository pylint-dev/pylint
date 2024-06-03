"""Check exceeding negations in boolean expressions trigger warnings"""

# pylint: disable=singleton-comparison,too-many-branches,too-few-public-methods,undefined-variable
# pylint: disable=literal-comparison, comparison-with-itself, comparison-of-constants
def unnecessary_negation():
    """This is not ok
    """
    bool_var = True
    someint = 2
    if not not bool_var:  # [unnecessary-negation]
        pass
    if not someint == 1:  # [unnecessary-negation]
        pass
    if not someint != 1:  # [unnecessary-negation]
        pass
    if not someint < 1:  # [unnecessary-negation]
        pass
    if not someint > 1:  # [unnecessary-negation]
        pass
    if not someint <= 1:  # [unnecessary-negation]
        pass
    if not someint >= 1:  # [unnecessary-negation]
        pass
    if not not someint:  # [unnecessary-negation]
        pass
    if not bool_var == True:  # [unnecessary-negation]
        pass
    if not bool_var == False:  # [unnecessary-negation]
        pass
    if not bool_var != True:  # [unnecessary-negation]
        pass
    if not True == True:  # [unnecessary-negation]
        pass
    if not 2 in [3, 4]:  # [unnecessary-negation]
        pass
    if not someint == 'test':  # [unnecessary-negation]
        pass


def tolerated_statements():
    """This is ok"""
    bool_var = True
    someint = 2
    if not(bool_var == False and someint == 1):
        pass
    if 2 not in [3, 4]:
        pass
    if not someint == bool_var == 2:
        pass
    if not 2 <= someint < 3 < 4:
        pass
    if not set('bar') <= set('foobaz'):
        pass
    if not set(something) <= 3:
        pass
    if not frozenset(something) <= 3:
        pass


class Klass:
    """This is also ok"""
    def __ne__(self, other):
        return not self == other
