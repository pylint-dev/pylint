# pylint: disable=missing-docstring, invalid-name

x = set(['py', 'lint'])  # [use-set-literal]
x = set((1, 2, 3))  # [use-set-literal]
x = set([3, 1, 4, 1, 5, 9])  # [use-set-literal]
x = set()
x = {'py', 'lint'}
x = {1, 2, 3}
x = {'a', 'b', 'c'}
