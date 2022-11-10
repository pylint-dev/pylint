# pylint: disable=missing-docstring
COUNTER = 0


class CustomBroadException(Exception):
    pass


class CustomNarrowException(CustomBroadException):
    pass


try:
    COUNTER += 1
except Exception: # [broad-exception-caught]
    print('error')


try:
    COUNTER += 1
except BaseException: # [broad-exception-caught]
    print('error')


try:
    COUNTER += 1
except ValueError as e:
    print('error')
    raise TypeError() from e


try:
    COUNTER += 1
except CustomBroadException as e:  # [broad-exception-caught]
    print('error')
    raise CustomNarrowException() from e


try:
    COUNTER += 1
except CustomNarrowException as e:
    print('error')
    raise CustomBroadException() from e  # [broad-exception-raised]
