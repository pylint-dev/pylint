# pylint: disable=missing-docstring
__revision__ = 0

try:
    __revision__ += 1
except Exception: # [broad-exception-caught]
    print('error')


try:
    __revision__ += 1
except BaseException: # [broad-exception-caught]
    print('error')
