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
