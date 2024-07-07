"""Miscellaneous used-before-assignment cases"""
# pylint: disable=consider-using-f-string, missing-function-docstring
import datetime
import sys
from typing import NoReturn

MSG = "hello %s" % MSG  # [used-before-assignment]

MSG2 = "hello %s" % MSG2  # [used-before-assignment]

def outer():
    inner()  # [used-before-assignment]
    def inner():
        pass

outer()


class ClassWithProperty:  # pylint: disable=too-few-public-methods
    """This test depends on earlier and later defined module-level functions."""
    prop = property(redefine_time_import)  # [used-before-assignment]
    prop_defined_earlier = property(outer)


calculate(1.01, 2)  # [used-before-assignment]
def calculate(value1: int, value2: float) -> int:
    return value1 + value2


# pylint: disable=unused-import, wrong-import-position, import-outside-toplevel, reimported, redefined-outer-name, global-statement
import time
def redefine_time_import():
    print(time.time())  # [used-before-assignment]
    import time


def redefine_time_import_with_global():
    global time  # pylint: disable=invalid-name
    print(time.time())
    import time


# Control flow cases
FALSE = False
if FALSE:
    VAR2 = True
if VAR2:  # [used-before-assignment]
    pass

if FALSE:  # pylint: disable=simplifiable-if-statement
    VAR3 = True
elif VAR2:
    VAR3 = True
else:
    VAR3 = False
if VAR3:
    pass

if FALSE:
    VAR4 = True
elif VAR2:
    pass
else:
    VAR4 = False
if VAR4:  # [possibly-used-before-assignment]
    pass

if FALSE:
    VAR5 = True
elif VAR2:
    if FALSE:  # pylint: disable=simplifiable-if-statement
        VAR5 = True
    else:
        VAR5 = True
if VAR5:  # [possibly-used-before-assignment]
    pass

if FALSE:
    VAR6 = False
if VAR6:  # [used-before-assignment]
    pass


# Nested try
if FALSE:
    try:
        VAR7 = True
    except ValueError:
        pass
else:
    VAR7 = False
if VAR7:
    pass

if FALSE:
    try:
        VAR8 = True
    except ValueError as ve:
        print(ve)
        raise
else:
    VAR8 = False
if VAR8:
    pass

if FALSE:
    for i in range(5):
        VAR9 = i
        break
print(VAR9)

if FALSE:
    with open(__name__, encoding='utf-8') as f:
        VAR10 = __name__
print(VAR10)  # [used-before-assignment]

for num in [0, 1]:
    VAR11 = num
    if VAR11:
        VAR12 = False
print(VAR12)  # [possibly-used-before-assignment]

if input("This tests terminating functions: "):
    sys.exit()
else:
    VAR13 = 1
print(VAR13)

def turn_on2(**kwargs):
    """https://github.com/pylint-dev/pylint/issues/7873"""
    if "brightness" in kwargs:
        brightness = kwargs["brightness"]
        var, *args = (1, "set_dimmer_state", brightness)
    else:
        var, *args = (1, "restore_dimmer_state")

    print(var, *args)


# Variables guarded by the same test when used.

# Always false
if 1 in []:
    PERCENT = 20
    SALE = True

if 1 in []:
    print(PERCENT)

# Different test
if 1 in [1]:
    print(SALE)  # [used-before-assignment]


# Ambiguous, but same test
if not datetime.date.today():
    WAS_TODAY = True

if not datetime.date.today():
    print(WAS_TODAY)


# Different tests but same inferred values
# Need falsy values here
def give_me_zero():
    return 0

def give_me_nothing():
    return 0

if give_me_zero():
    WE_HAVE_ZERO = True
    ALL_DONE = True

if give_me_nothing():
    print(WE_HAVE_ZERO)


# Different tests, different values
def give_me_none():
    return None

if give_me_none():
    print(ALL_DONE)  # [used-before-assignment]


attr = 'test'  # pylint: disable=invalid-name
class T:  # pylint: disable=invalid-name, too-few-public-methods, undefined-variable
    '''Issue #8754, no crash from unexpected assignment between attribute and variable'''
    T.attr = attr


if outer():
    NOT_ALWAYS_DEFINED = True
print(NOT_ALWAYS_DEFINED)  # [used-before-assignment]


def inner_if_continues_outer_if_has_no_other_statements():
    for i in range(5):
        if isinstance(i, int):
            # Testing no assignment here, before the inner if
            if i % 2 == 0:
                order = None
            else:
                continue
        else:
            order = None
        print(order)


class PlatformChecks:  # pylint: disable=missing-docstring
    """https://github.com/pylint-dev/pylint/issues/9674"""
    def skip(self, msg) -> NoReturn:
        raise Exception(msg)  # pylint: disable=broad-exception-raised

    def print_platform_specific_command(self):
        if sys.platform == "linux":
            cmd = "ls"
        elif sys.platform == "win32":
            cmd = "dir"
        else:
            self.skip("only runs on Linux/Windows")

        print(cmd)
