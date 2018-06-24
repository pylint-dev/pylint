# pylint: disable=missing-docstring


def some_func():
    pass


class Class:

    def some_method(self):
        pass

    def some_other_method(self):
        value = self.some_method()  # [assignment-from-no-return]
        return value + 1


VALUE = some_func() # [assignment-from-no-return]
