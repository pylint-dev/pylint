"""Tests for multiple-statements with single-line-***-stmt turned on."""
# pylint: disable=using-constant-test, missing-class-docstring, missing-function-docstring, bare-except
# pylint: disable=unused-argument, function-redefined

from typing import overload

if True: pass

if True: pass  # [multiple-statements]
else:
    pass

class MyError(Exception): pass

class MyError(Exception): a='a'

class MyError(Exception): a='a'; b='b'  # [multiple-statements]

try:
    pass
except:
    pass
finally:
    pass


@overload
def concat2(arg1: str) -> str: ...

def concat2(arg1: str) -> str: ...
