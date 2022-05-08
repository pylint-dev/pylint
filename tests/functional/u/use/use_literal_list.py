# pylint: disable=missing-docstring, invalid-name

x = list()  # [use-list-literal]
x = list("string")  # [use-list-literal]
x = list({1, 2, 3})  # [use-list-literal]
x = list(range(3))
x = []
x = ['s', 't', 'r', 'i', 'n', 'g']
x = [1, 2, 3]
x = [range(3)]
