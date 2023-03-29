"""Tests for redefinitions of loop variables inside the loop body.

See: https://github.com/pylint-dev/pylint/issues/5608
"""
# pylint: disable=invalid-name

lines = ["1\t", "2\t"]
for line in lines:
    line = line.strip()  # [redefined-loop-name]

for i in range(8):
    for j in range(8):
        for i in range(j):  # [redefined-loop-name]
            j = i  # [redefined-loop-name]
            print(i, j)

for i in range(8):
    for j in range(8):
        for k in range(j):
            k = (i, j)  # [redefined-loop-name]
            print(i, j, k)

lines = [(1, "1\t"), (2, "2\t")]
for i, line in lines:
    line = line.strip()  # [redefined-loop-name]

line = "no warning"

for i in range(10):
    i += 1  # [redefined-loop-name]


def outer():
    """No redefined-loop-name for variables in nested scopes"""
    for i1 in range(5):
        def inner():
            """No warning, because i has a new scope"""
            for i1 in range(3):
                print(i1)
        print(i1)
        inner()


def outer2():
    """Similar, but with an assignment instead of homonymous loop variables"""
    for i1 in range(5):
        def inner():
            """No warning, because i has a new scope"""
            for _ in range(3):
                i1 = 0
                print(i1)
        print(i1)
        inner()
