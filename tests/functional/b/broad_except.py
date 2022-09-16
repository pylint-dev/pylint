# pylint: disable=missing-docstring
__revision__ = 0

try:
    __revision__ += 1
except Exception: # [broad-except]
    print('error')


try:
    __revision__ += 1
except BaseException: # [broad-except]
    print('error')
