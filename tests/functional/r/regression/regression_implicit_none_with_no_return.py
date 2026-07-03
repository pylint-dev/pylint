# pylint: disable=missing-docstring,pointless-statement,invalid-name

class A:
    def func(self):
        print('hello')

    @property
    def index(self):
        print('world')


# Since these are not assigned anywhere, assignment-from-none etc.
# in typecheck does not warn

a = A()
# double call is workaround for #4426
a.func()()  # [not-callable]
[1, 2, 3][a.index]  # [invalid-sequence-index]
