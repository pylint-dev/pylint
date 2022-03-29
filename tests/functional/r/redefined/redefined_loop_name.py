"""Tests for redefinitions of loop variables inside the loop body.

See: https://github.com/PyCQA/pylint/issues/5608
"""
# pylint: disable=invalid-name

lines = ["1\t", "2\t"]
for line in lines:
    line = line.strip()  # [redefined-outer-name]

for i in range(8):
    for j in range(8):
        for i in range(j):  # [redefined-outer-name]
            j = i  # [redefined-outer-name]
            print(i, j)

for i in range(8):
    for j in range(8):
        for k in range(j):
            k = (i, j)  # [redefined-outer-name]
            print(i, j, k)

lines = [(1, "1\t"), (2, "2\t")]
for i, line in lines:
    line = line.strip()  # [redefined-outer-name]

line = "no warning"

for i in range(10):
    i += 1  # [redefined-outer-name]
