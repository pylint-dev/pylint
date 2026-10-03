"""Checks of Dosctrings 'docstring-first-line-empty'"""
# pylint: disable=too-few-public-methods,bad-docstring-quotes

def check_messages(*messages):  # [docstring-first-line-empty]
    """
    docstring"""
    return messages


def function2():
    """Test Ok"""


class FFFF:  # [docstring-first-line-empty]
    """
    Test Docstring First Line Empty
    """

    def method1(self):  # [docstring-first-line-empty]
        '''
        Test Triple Single Quotes docstring
        '''
