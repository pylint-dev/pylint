# pylint: disable = invalid-name, line-too-long
"""Simple test sets for checking duplicate values"""

set1 = {1, 2, 3, 4}
set2 = {1, 1, 2} # [duplicate-value]
set3 = {1, 2, 2} # [duplicate-value]

set4 = {'one', 'two', 'three'}
set5 = {'one', 'two', 'one'} # [duplicate-value]
set6 = {'one', 'two', 'two'} # [duplicate-value]

wrong_set = {12, 23, True, 6, True, 0, 12} # [duplicate-value, duplicate-value]
correct_set = {12, 13, 23, 24, 89}

wrong_set_mixed = {1, 2, 'value', 1} # [duplicate-value]
wrong_set = {'arg1', 'arg2', False, 'arg1', True} # [duplicate-value]

another_wrong_set = {2, 3, 'arg1', True, 'arg1', False, True} # [duplicate-value, duplicate-value]
