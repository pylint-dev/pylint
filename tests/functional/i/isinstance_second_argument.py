#pylint: disable=missing-docstring, undefined-variable, invalid-name, too-few-public-methods

# Positive test cases
class A:
    pass

class B(A):
    pass

isinstance(-9999, int)
isinstance(True and False, bool)
isinstance("a 'string'", float)
isinstance(3.123213, set)
isinstance(A(), A)
isinstance(A(), B)

# Negative test cases
isinstance({a:1}, any)
