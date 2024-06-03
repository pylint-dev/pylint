# pylint:disable=missing-docstring, unreachable, bad-except-order, bare-except, unnecessary-pass
# pylint: disable=undefined-variable, broad-except, raise-missing-from, too-few-public-methods
try:
    int("9a")
except:  # [try-except-raise]
    raise

try:
    int("9a")
except:
    raise ValueError('Invalid integer')


try:
    int("9a")
except:  # [try-except-raise]
    raise
    print('caught exception')

try:
    int("9a")
except:
    print('caught exception')
    raise


class AAAException(Exception):
    """AAAException"""
    pass

class BBBException(AAAException):
    """BBBException"""
    pass

def ccc():
    """try-except-raise test function"""

    try:
        raise BBBException("asdf")
    except BBBException:
        raise
    except AAAException:
        raise BBBException("raised from AAAException")


def ddd():
    """try-except-raise test function"""

    try:
        raise BBBException("asdf")
    except AAAException:
        raise BBBException("raised from AAAException")
    except:  # [try-except-raise]
        raise

try:
    pass
except RuntimeError:
    raise
except:
    print("a failure")

try:
    pass
except:
    print("a failure")
except RuntimeError:  # [try-except-raise]
    raise

try:
    pass
except:  # [try-except-raise]
    raise
except RuntimeError:
    print("a failure")

try:
    pass
except (FileNotFoundError, PermissionError):
    raise
except OSError:
    print("a failure")

class NameSpace:
    error1 = FileNotFoundError
    error2 = PermissionError
    parent_error=OSError

try:
    pass
except (NameSpace.error1, NameSpace.error2):
    raise
except NameSpace.parent_error:
    print("a failure")

# also consider tuples for subsequent exception handler instead of just bare except handler
try:
    pass
except (FileNotFoundError, PermissionError):
    raise
except (OverflowError, OSError):
    print("a failure")

try:
    pass
except (FileNotFoundError, PermissionError):  # [try-except-raise]
    raise
except (OverflowError, ZeroDivisionError):
    print("a failure")

try:
    pass
except (FileNotFoundError, PermissionError):
    raise
except Exception:
    print("a failure")

try:
    pass
except (FileNotFoundError, PermissionError):
    raise
except (Exception,):
    print("a failure")
