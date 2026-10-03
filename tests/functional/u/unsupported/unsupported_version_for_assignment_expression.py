# pylint: disable=missing-function-docstring, missing-module-docstring
import random
if zero_or_one := random.randint(0, 1):  # [using-assignment-expression-in-unsupported-version]
    assert zero_or_one == 1
