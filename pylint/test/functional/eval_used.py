"""test for eval usage"""

eval('os.listdir(".")') # [eval-used]
eval('os.listdir(".")', globals={})  # [eval-used]

eval('os.listdir(".")', globals=globals())  # [eval-used]

def func():
    """ eval in local scope"""
    eval('b = 1')  # [eval-used]

def func2():
    """Use of infer node"""
    seudo_eval = eval
    seudo_eval('b = 1')  # [eval-used]
