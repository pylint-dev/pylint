# pylint: disable=missing-docstring,invalid-name,nonlocal-without-binding


def tomato(is_tasty: bool = True):
    nonlocal is_tasty # [name-is-parameter-and-nonlocal]
