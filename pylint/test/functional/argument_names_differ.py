"""Test that we are emitting arguments-differ when the arguments are different."""
# pylint: disable=missing-docstring, too-few-public-methods, unused-argument,useless-super-delegation, useless-object-inheritance, invalid-name

def minimal_example(x, y):
    pass

def put_things_in_scope():
    x = 10
    y = 20
    z = 30

    minimal_example(x, y)
    minimal_example(x, x)
    minimal_example(y, y)
    minimal_example(x, z)
    minimal_example(x, 0)
    minimal_example(z, y)
    minimal_example(z, z)
    minimal_example(x=y, y=x)
    minimal_example(z, y=x)

    minimal_example(y, x)  # [arg-var-name-clash, arg-var-name-clash]
    minimal_example(y, z)  # [arg-var-name-clash]
    minimal_example(y, 0)  # [arg-var-name-clash]
    minimal_example(z, x)  # [arg-var-name-clash]

def realistic_example(a, b, c=None, d=None):
    pass

def scope_2():
    a = 1
    b = 2
    c = 3
    other_args = [3, 4]

    realistic_example(a, b, *other_args)
    realistic_example(a, c, c=1)
    realistic_example(b, *other_args) # [arg-var-name-clash]
    realistic_example(a, c) # [arg-var-name-clash]


class MethodsToo(object):
    def a_method(self, x, y):
        pass


def scope_3():
    m = MethodsToo()

    x = 10
    y = 20

    m.a_method(y, x)  # [arg-var-name-clash, arg-var-name-clash]
