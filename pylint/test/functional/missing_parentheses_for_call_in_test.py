"""Verify if call to function or method inside tests are missing parentheses."""
# pylint: disable=invalid-name, missing-docstring,too-few-public-methods
# pylint: disable=no-init,expression-not-assigned, useless-object-inheritance

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


instance = Class()

if collections:
    pass

if bool_function: # [missing-parentheses-for-call-in-test]
    pass

if not bool_function():
    pass
