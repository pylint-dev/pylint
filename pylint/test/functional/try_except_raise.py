# pylint:disable=missing-docstring, unreachable, bad-except-order, bare-except

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
