# pylint: disable=missing-docstring, invalid-name

MY_DICTIONARY = {"key_one": 1, "key_two": 2, "key_three": 3}

try:  # [max-try-statements]
    value = MY_DICTIONARY["key_one"]
    value += 1
except KeyError:
    pass

try:
    value = MY_DICTIONARY["key_one"]
except KeyError:
    value = 0
