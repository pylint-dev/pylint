"""Checks of Dosctrings 'bad-docstring-quotes'"""
# pylint: disable=docstring-first-line-empty,missing-class-docstring


class FFFF:
    def method1(self):  # [bad-docstring-quotes]
        '''
        Test Triple Single Quotes docstring
        '''

    def method2(self):  # [bad-docstring-quotes]
        "bad docstring 1"

    def method3(self):  # [bad-docstring-quotes]
        'bad docstring 2'

    def method4(self):  # [bad-docstring-quotes]
        ' """bad docstring 3 '
