# pylint: disable=missing-docstring, invalid-name

x = dict()  # [use-dict-literal]
x = dict(a="1", b=None, c=3)  # [use-dict-literal]
x = dict((('a', 1), ('b', 2)))  # [use-dict-literal]
x = dict(zip(["a", "b", "c"], [1, 2, 3]))
x = {}
x = {"a": 1, "b": 2, "c": 3}
