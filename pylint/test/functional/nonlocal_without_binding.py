""" Checks that reversed() receive proper argument """
# pylint: disable=missing-docstring,invalid-name,unused-variable
# pylint: disable=too-few-public-methods,no-self-use,no-absolute-import

def test():
    def parent():
        a = 42
        def stuff():
            nonlocal a

    def parent2():
        a = 42
        def stuff():
            def other_stuff():
                nonlocal a

b = 42
def func():
    def other_func():
        nonlocal b  # [nonlocal-without-binding]
