# pylint: disable=missing-docstring
__revision__ = 0

class CustomBroadException(Exception):
    pass


class CustomNarrowException(CustomBroadException):
    pass


try:
    __revision__ += 1
except* Exception: # [broad-exception-caught]
    print('error')


try:
    __revision__ += 1
except* BaseException: # [broad-exception-caught]
    print('error')


try:
    __revision__ += 1
except* ValueError:
    print('error')


try:
    __revision__ += 1
except CustomBroadException: # [broad-exception-caught]
    print('error')


try:
    __revision__ += 1
except* CustomNarrowException:
    print('error')
