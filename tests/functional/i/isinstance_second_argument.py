#pylint: disable=missing-docstring, undefined-variable, invalid-name, too-few-public-methods

# Positive test cases
class A:
    pass

class B(A):
    pass

isinstance(A(), A)
isinstance(A(), B)

isinstance(-9999, int)
isinstance(True and False, bool)
isinstance("a 'string'", float)
isinstance(3.123213, set)
isinstance(foo, (int, str))
isinstance("a string", ((int, bool), (float, set), str))

# Negative test cases
isinstance({a:1}, hash) # [isinstance-second-argument-not-valid-type]
isinstance(64, hex) # [isinstance-second-argument-not-valid-type]
isinstance({b: 100}, (hash, dict)) # [isinstance-second-argument-not-valid-type]
isinstance("string", ((dict, iter), str, (int, bool))) # [isinstance-second-argument-not-valid-type]
