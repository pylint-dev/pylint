# pylint: disable=missing-docstring, comparison-with-itself


if 2 is 2:  # [literal-comparison, comparison-of-constants]
    pass

if "a" is b"a":  # [literal-comparison, comparison-of-constants]
    pass

if 2.0 is 3.0:  # [literal-comparison, comparison-of-constants]
    pass

if () is (1, 2, 3):
    pass

if () is {1:2, 2:3}:  # [literal-comparison]
    pass

if [] is [4, 5, 6]:  # [literal-comparison]
    pass

if () is {1, 2, 3}:  # [literal-comparison]
    pass

if () is not {1:2, 2:3}: # [literal-comparison]
    pass

if [] is not [4, 5, 6]: # [literal-comparison]
    pass

if () is not {1, 2, 3}: # [literal-comparison]
    pass


CONST = 24


if CONST is 0: # [literal-comparison]
    pass

if CONST is 1: # [literal-comparison]
    pass

if CONST is 42: # [literal-comparison]
    pass

# We do not do inference for this check, since the comparing
# object might be used as a sentinel.
if () is CONST:
    pass

def github_issue_3031(arg=()):
    if arg is ():
        pass

    if arg is not ():
        pass


def variable_name_containing_is():
    # Regression test: the suggested replacement must not corrupt an identifier
    # that contains the substring "is" (e.g. ``axis`` was rendered ``ax==``).
    axis = 5
    return axis is 5  # [literal-comparison]
