# pylint: disable=missing-docstring,too-few-public-methods,bad-option-value


def myfunc(): # [useless-return]
    print('---- testing ---')
    return

class SomeClass:
    def mymethod(self): # [useless-return]
        print('---- testing ---')
        return None

    # These are not emitted
    def item_at(self):
        return None


def function2(parameter):  # [useless-return]
    if parameter:
        pass
    return


def function3(parameter):  # [useless-return]
    if parameter:
        pass
    else:
        return


def function4(parameter):  # [useless-return]
    try:
        parameter.do()
    except RuntimeError:
        parameter.other()
        return


def function5(parameter):  # [useless-return]
    try:
        parameter.do()
    except RuntimeError:
        return


def code_after_return(param):
    try:
        param.kaboom()
    except RuntimeError:
        param.other()
        return

    param.something_else()
    param.state = "good"


def code_after_else(obj):
    if obj.k:
        pass
    else:
        return

    obj.do()


def return_in_loop(obj):
    for _ in range(10):
        obj.do()
        if obj.k:
            return

    return
