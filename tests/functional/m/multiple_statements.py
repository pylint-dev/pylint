"""Tests for multiple-statements"""
# pylint: disable=using-constant-test, missing-class-docstring, missing-function-docstring, bare-except
# pylint: disable=unused-argument, function-redefined

from typing import overload

if True: print("Golfing sure is nice")  # [multiple-statements]
if True: pass  # [multiple-statements]
if True: ...  # [multiple-statements]

if True: print("Golfing sure is nice")  # [multiple-statements]
else:
    pass

if True: pass  # [multiple-statements]
else:
    pass

if True: ...  # [multiple-statements]
else:
    pass

# The following difference in behavior is due to black 2024's style
# that reformat pass on multiple line but reformat "..." on a single line
# (only for classes, not for the examples above)
class MyException(Exception): print("Golfing sure is nice")  # [multiple-statements]
class MyError(Exception): pass  # [multiple-statements]
class DebugTrueDetected(Exception): ...

class MyError(Exception): a='a'  # [multiple-statements]

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

# Test for multiple statements on finally line
try:
    pass
finally: pass  # [multiple-statements]

# Test for multiple statements on else line
try:
    pass
except:
    pass
else: pass  # [multiple-statements]

# Test for multiple statements on else and finally lines
try:
    pass
except:
    pass
else: pass  # [multiple-statements]
finally: pass  # [multiple-statements]
