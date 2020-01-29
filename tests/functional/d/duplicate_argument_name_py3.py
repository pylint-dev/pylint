"""Check for duplicate function keywordonly arguments."""


def foo1(_, *_, _=3): # [duplicate-argument-name, duplicate-argument-name]
    """Function with duplicate argument name."""
