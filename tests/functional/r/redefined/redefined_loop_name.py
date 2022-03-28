"""Tests for redefinitions of loop variables inside the loop body.

See: https://github.com/PyCQA/pylint/issues/5608
"""
# pylint: disable=invalid-name

lines = ["1\t", "2\t"]
for line in lines:
    line = line.strip()  # [redefined-outer-name]

lines = [(1, "1\t"), (2, "2\t")]
for i, line in lines:
    line = line.strip()  # [redefined-outer-name]

line = "no warning"

for i in range(10):
    i += 1  # [redefined-outer-name]
