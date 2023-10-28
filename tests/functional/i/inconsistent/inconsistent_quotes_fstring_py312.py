# pylint: disable=missing-module-docstring

dictionary = {'0': 0}
# quotes are inconsistent when targetting Python 3.12 (use single quotes)
f_string = f'{dictionary["0"]}'  # [inconsistent-quotes]
