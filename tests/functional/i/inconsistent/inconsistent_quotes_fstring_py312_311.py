# pylint: disable=missing-module-docstring

dictionary = {'0': 0}
# quotes are consistent when targeting 3.11 and earlier (cannot use single quotes here)
F_STRING = f'{dictionary["0"]}'
