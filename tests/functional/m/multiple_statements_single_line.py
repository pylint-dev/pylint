"""Tests for multiple-statements with single-line-***-stmt turned on."""
# pylint: disable=using-constant-test, missing-class-docstring, missing-function-docstring, bare-except
# pylint: disable=unused-argument, function-redefined

from typing import overload

if True: print("Golfing sure is nice")
if True: pass
if True: ...

if True: print("Golfing sure is nice")  # [multiple-statements]
else:
    pass

if True: pass  # [multiple-statements]
else:
    pass

if True: ...  # [multiple-statements]
else:
    pass

class MyException(Exception): print("Golfing sure is nice")
class MyError(Exception): pass
class DebugTrueDetected(Exception): ...


class MyError(Exception): a='a'

class MyError(Exception): a='a'; b='b'  # [multiple-statements]

try:  #@
    pass
except:
    pass
finally:
    pass


@overload
def concat2(arg1: str) -> str: ...

def concat2(arg1: str) -> str: ...
