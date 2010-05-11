"""Test function argument checker"""
__revision__ = ''

def function_1_arg(first_argument):
    """one argument function"""
    return first_argument

def function_3_args(first_argument, second_argument, third_argument):
    """three arguments function"""
    return first_argument, second_argument, third_argument

def function_default_arg(one=1, two=2):
    """fonction with default value"""
    return two, one


function_1_arg(420)
function_1_arg()
function_1_arg(1337, 347)

function_3_args(420, 789)
function_3_args()
function_3_args(1337, 347, 456)
function_3_args('bab', 'bebe', None, 5.6)

function_default_arg(1, two=5)
function_default_arg(two=5)
# repeated keyword is syntax error in python >= 2.6:
# tests are moved to func_keyword_repeat_py25- / func_keyword_repeat_py26

function_1_arg(bob=4)
function_default_arg(1, 4, coin="hello")

function_default_arg(1, one=5)

