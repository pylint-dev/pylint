"""Verify if call to function or method inside tests are missing parentheses."""
# pylint: disable=using-constant-test, missing-docstring, useless-object-inheritance
# pylint: disable=invalid-name, expression-not-assigned

import collections


def bool_function():
    return True

def nonbool_function():
    return 42


class Class(object):

    @staticmethod
    def bool_method():
        return False

    @staticmethod
    def nonbool_method():
        return 42


if collections:
    pass

if bool_function: # [missing-parentheses-for-call-in-test]
    pass

if not bool_function():
    pass

if nonbool_function:  # [missing-parentheses-for-call-in-test]
    pass

if nonbool_function() != 42:
    pass

instance = Class()

if instance.bool_method:  # [missing-parentheses-for-call-in-test]
    pass

if not instance.bool_method():
    pass

if not instance.nonbool_method:
    pass
elif instance.bool_method:  # [missing-parentheses-for-call-in-test]
    pass

bool_lambda = lambda: True

if bool_lambda:  # [missing-parentheses-for-call-in-test]
    pass

if not bool_lambda():
    pass

nonbool_lambda = lambda: 42

if nonbool_lambda: # [missing-parentheses-for-call-in-test]
    pass

if not nonbool_lambda():
    pass

MY_VALUE = 42 if bool_function else -1  # [missing-parentheses-for-call-in-test]
MY_2ND_VALUE = 42 if not bool_function() else -1
MY_THIRD_VALUE = 42 if bool_lambda else -1  # [missing-parentheses-for-call-in-test]
MY_FOURTH_VALUE = 42 if nonbool_lambda else -1  # [missing-parentheses-for-call-in-test]

[x for x in range(100) if bool_function]  # [missing-parentheses-for-call-in-test]
[x for x in range(100) if bool_lambda]  # [missing-parentheses-for-call-in-test]
[x for x in range(100) if not bool_function()]
[x for x in range(100) if not bool_lambda()]
[x for x in range(100) if nonbool_lambda]  # [missing-parentheses-for-call-in-test]
[x for x in range(100) if nonbool_function]  # [missing-parentheses-for-call-in-test]

def non_const_node_function():
    return (1, 2, 42)

if non_const_node_function:  # [missing-parentheses-for-call-in-test]
    pass

def yielding_function():
    yield 42

if yielding_function: # [missing-parentheses-for-call-in-test]
    pass

if not yielding_function():
    pass
