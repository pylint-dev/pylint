"""Module whose function shadows a name set from another module."""


def main():
    """Shadow the attribute that the test module sets."""
    some_redefined_variable = "something else"
    print(some_redefined_variable)
