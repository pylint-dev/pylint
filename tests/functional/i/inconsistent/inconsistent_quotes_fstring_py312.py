# pylint: disable=missing-module-docstring

dictionary = {'0': 0}
# quotes are inconsistent when targeting Python 3.12 (use single quotes)
F_STRING = f'{dictionary["0"]}'  # [inconsistent-quotes]
