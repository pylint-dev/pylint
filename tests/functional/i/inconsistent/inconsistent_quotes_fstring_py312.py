# pylint: disable=missing-module-docstring

DICTIONARY = {'0': 0}
# quotes are inconsistent when targeting Python 3.12 (use single quotes)
F_STRING = f'{DICTIONARY["0"]}'  # [inconsistent-quotes]
