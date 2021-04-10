"""Test that we emit unused-argument when a function uses `raise

https://github.com/PyCQA/pylint/issues/3416
"""

# pylint:disable=raise-missing-from

# +1: [unused-argument, unused-argument, unused-argument]
def fun(arg_a, arg_b, arg_c) -> None:
    """Routine docstring"""
    try:
        pass
    except Exception:
        raise RuntimeError("")
