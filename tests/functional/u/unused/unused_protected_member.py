# pylint: disable=missing-docstring, invalid-name, too-few-public-methods, no-self-use, line-too-long

class HasUnusedInClass():  # [unused-protected-member,unused-protected-member,unused-protected-member,unused-protected-member]

    _my_secret = "I have no secrets"  # this is unused (1/4)

    def __init__(self):  # Will not trigger as it begins with __ and ends with __
        self._instance_secret = "I will never be initialized"  # this is unused (2/4)
        self._another_secret = "hello world"

    def __str__(self):  # Will not trigger as it begins with __ and ends with __
        return "hello"

    def _test(self, x, y, z):  # this is unused (3/4)
        pass

    def _my_print(self, string):
        print(self._another_secret + string)

    def hey(self):  # Will not trigger as it does not begin with _
        self._my_print("!")

    def _test_fn_as_var(self):
        pass

    def assign_fn_to_var(self):
        fn = self._test_fn_as_var
        fn()

    def _test_recursive(self):  # will trigger, unused recursive method (4/4)
        self._test_recursive()
