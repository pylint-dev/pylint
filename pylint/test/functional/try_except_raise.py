# pylint:disable=missing-docstring

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
except ValueError:  # [try-except-raise]
    raise ValueError('Invalid integer')
