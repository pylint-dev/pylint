#pylint: disable=missing-docstring, undefined-variable, invalid-name, too-few-public-methods, wrong-import-position

# Positive test cases
class A:
    pass

class B(A):
    pass

isinstance(A(), A)
isinstance(A(), B)

isinstance(-9999, int)
isinstance(True and False, bool)
isinstance("a 'string'", type("test"))

import collections

isinstance(3.123213, collections.OrderedDict)
isinstance(foo, (int, collections.Counter))
isinstance("a string", ((int, type(False)), (float, set), str))
isinstance(10, (int,) + (str, bool) + (dict, list, tuple))

# Negative test cases
isinstance({a:1}, hash) # [isinstance-second-argument-not-valid-type]
isinstance(64, hex) # [isinstance-second-argument-not-valid-type]
isinstance({b: 100}, (hash, dict)) # [isinstance-second-argument-not-valid-type]
isinstance("string", ((dict, iter), str, (int, bool))) # [isinstance-second-argument-not-valid-type]
