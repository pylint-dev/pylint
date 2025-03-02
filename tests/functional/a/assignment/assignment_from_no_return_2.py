# pylint: disable=useless-return, condition-evals-to-constant, invalid-name
"""check assignment to function call where the function doesn't return

    'E1111': ('Assigning to function call which doesn\'t return',
              'Used when an assignment is done on a function call but the \
              inferred function doesn\'t return anything.'),
    'W1111': ('Assigning to function call which only returns None',
              'Used when an assignment is done on a function call but the \
              inferred function returns nothing but None.'),

"""

def func_no_return():
    """function without return"""
    print('dougloup')

A = func_no_return()  # [assignment-from-no-return]


def func_return_none():
    """function returning none"""
    print('dougloup')
    return None

A = func_return_none()  # [assignment-from-none]


def func_implicit_return_none():
    """Function returning None from bare return statement."""
    return

A = func_implicit_return_none()  # [assignment-from-none]

lst = [3, 2]
A = lst.sort()  # [assignment-from-no-return]
my_dict = {3: 2}
B = my_dict.update({2: 1})  # [assignment-from-no-return]
my_set = set()
C = my_set.symmetric_difference_update([6])  # [assignment-from-no-return]

def func_return_none_and_smth():
    """function returning none and something else"""
    print('dougloup')
    if 2 or 3:
        return None
    return 3

A = func_return_none_and_smth()

def generator():
    """no problemo"""
    yield 2

A = generator()

class Abstract:
    """bla bla"""

    def abstract_method(self):
        """use to return something in concrete implementation"""
        raise NotImplementedError

    def use_abstract(self):
        """should not issue E1111"""
        var = self.abstract_method()
        print(var)
