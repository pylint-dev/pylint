"""test for eval usage"""

eval('os.listdir(".")')  # [eval-used]
eval('os.listdir(".")', globals={})  # [eval-used]

eval('os.listdir(".")', globals=globals())  # [eval-used]


def func():
    """ eval in local scope"""
    eval('b = 1')  # [eval-used]


def func2(param):
    """eval used from param"""
    param("c = 2")


def func3():
    """eval used from many ways"""
    my_dict = {
        'my_eval': eval,  # [eval-used]
    }
    my_list = [eval]  # [eval-used]

    my_var = eval  # [eval-used]
    # inferred case
    my_var('d = 3')  # [eval-used]
    func2(eval)  # [eval-used]
    return my_dict, my_list
