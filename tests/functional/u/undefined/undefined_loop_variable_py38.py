"""Tests for undefined-loop-variable with assignment expressions"""


def walrus_in_comprehension_test(container):
    """https://github.com/pylint-dev/pylint/issues/7222"""
    for something in container:
        print(something)
    print([my_test for something in container if (my_test := something)])
