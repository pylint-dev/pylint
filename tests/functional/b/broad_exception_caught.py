# pylint: disable=missing-docstring
__revision__ = 0

class CustomBroadException(Exception):
    pass


class CustomNarrowException(CustomBroadException):
    pass


try:
    __revision__ += 1
except Exception: # [broad-exception-caught]
    print('error')


try:
    __revision__ += 1
except BaseException: # [broad-exception-caught]
    print('error')


try:
    __revision__ += 1
except ValueError:
    print('error')
    raise TypeError()


try:
    __revision__ += 1
except CustomBroadException as e: # [broad-exception-caught]
    print('error')
    raise CustomNarrowException() from e


try:
    __revision__ += 1
except CustomNarrowException as e:
    print('error')
    raise CustomBroadException() from e  # [broad-exception-raised]
