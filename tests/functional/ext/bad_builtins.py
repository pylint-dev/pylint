# pylint: disable=missing-docstring
input("Yes or no ? (Y=1, n=0)")  # [bad-builtin]
print(map(str, filter(1, [1, 2, 3])))  # [bad-builtin, bad-builtin, bad-builtin]
