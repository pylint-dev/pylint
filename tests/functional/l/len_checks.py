# pylint: disable=too-few-public-methods,import-error, no-absolute-import,missing-docstring, misplaced-comparison-constant
# pylint: disable=useless-super-delegation,wrong-import-position,invalid-name, wrong-import-order, condition-evals-to-constant

if len('TEST'):  # [len-as-condition]
    pass

if not len('TEST'):  # [len-as-condition]
    pass

z = []
if z and len(['T', 'E', 'S', 'T']):  # [len-as-condition]
    pass

if True or len('TEST'):  # [len-as-condition]
    pass

if len('TEST') == 0:  # Should be fine
    pass

if len('TEST') < 1:  # Should be fine
    pass

if len('TEST') <= 0:  # Should be fine
    pass

if 1 > len('TEST'):  # Should be fine
    pass

if 0 >= len('TEST'):  # Should be fine
    pass

if z and len('TEST') == 0:  # Should be fine
    pass

if 0 == len('TEST') < 10:  # Should be fine
    pass

if 0 < 1 <= len('TEST') < 10:  # Should be fine
    pass

if 10 > len('TEST') != 0:  # Should be fine
    pass

if 10 > len('TEST') > 1 > 0:  # Should be fine
    pass

if 0 <= len('TEST') < 100:  # Should be fine
    pass

if z or 10 > len('TEST') != 0:  # Should be fine
    pass

if z:
    pass
elif len('TEST'):  # [len-as-condition]
    pass

if z:
    pass
elif not len('TEST'):  # [len-as-condition]
    pass

while len('TEST'):  # [len-as-condition]
    pass

while not len('TEST'):  # [len-as-condition]
    pass

while z and len('TEST'):  # [len-as-condition]
    pass

while not len('TEST') and z:  # [len-as-condition]
    pass

assert len('TEST') > 0  # Should be fine

x = 1 if len('TEST') != 0 else 2  # Should be fine

f_o_o = len('TEST') or 42  # Should be fine

a = x and len(x)  # Should be fine

def some_func():
    return len('TEST') > 0  # Should be fine

def github_issue_1325():
    l = [1, 2, 3]
    length = len(l) if l else 0  # Should be fine
    return length

def github_issue_1331(*args):
    assert False, len(args)  # Should be fine

def github_issue_1331_v2(*args):
    assert len(args), args  # [len-as-condition]

def github_issue_1331_v3(*args):
    assert len(args) or z, args  # [len-as-condition]

def github_issue_1331_v4(*args):
    assert z and len(args), args  # [len-as-condition]

b = bool(len(z)) # [len-as-condition]
c = bool(len('TEST') or 42) # [len-as-condition]


def github_issue_1879():

    class ClassWithBool(list):
        def __bool__(self):
            return True

    class ClassWithoutBool(list):
        pass

    class ChildClassWithBool(ClassWithBool):
        pass

    class ChildClassWithoutBool(ClassWithoutBool):
        pass

    assert len(ClassWithBool())
    assert len(ChildClassWithBool())
    assert len(ClassWithoutBool())  # [len-as-condition]
    assert len(ChildClassWithoutBool())  # [len-as-condition]
    assert len(range(0))  # [len-as-condition]
    assert len([t + 1 for t in []])  # [len-as-condition]
    assert len(u + 1 for u in [])  # [len-as-condition]
    assert len({"1":(v + 1) for v in {}})  # [len-as-condition]
    assert len(set((w + 1) for w in set()))  # [len-as-condition]

    # pylint: disable=import-outside-toplevel
    import numpy
    numpy_array = numpy.array([0])
    if len(numpy_array) > 0:
        print('numpy_array')
    if len(numpy_array):
        print('numpy_array')
    if numpy_array:
        print('b')

    import pandas as pd
    pandas_df = pd.DataFrame()
    if len(pandas_df):
        print("this works, but pylint tells me not to use len() without comparison")
    if len(pandas_df) > 0:
        print("this works and pylint likes it, but it's not the solution intended by PEP-8")
    if pandas_df:
        print("this does not work (truth value of dataframe is ambiguous)")

    def function_returning_list(r):
        if r==1:
            return [1]
        return [2]

    def function_returning_int(r):
        if r==1:
            return 1
        return 2

    # def function_returning_generator(r):
    #     for i in [r, 1, 2, 3]:
    #         yield i

    # def function_returning_comprehension(r):
    #     return [x+1 for x in [r, 1, 2, 3]]

    # def function_returning_function(r):
    #     return function_returning_generator(r)

    assert len(function_returning_list(z))  # [len-as-condition]
    assert len(function_returning_int(z))
    # This should raise a len-as-conditions once astroid can infer it
    # See https://github.com/PyCQA/pylint/pull/3821#issuecomment-743771514
    # assert len(function_returning_generator(z))
    # assert len(function_returning_comprehension(z))
    # assert len(function_returning_function(z))


def github_issue_4215():
    # Test undefined variables
    # https://github.com/PyCQA/pylint/issues/4215
    if len(undefined_var):  # [undefined-variable]
        pass
    if len(undefined_var2[0]):  # [undefined-variable]
        pass
