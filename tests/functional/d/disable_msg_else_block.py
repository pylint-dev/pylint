# Regression test for https://github.com/pylint-dev/pylint/issues/872
# A disable comment at the start of an `else` block used to have no effect.
# Fixed with astroid 4.3.0, where `block_range` considers `else` its own block.
"""Check that a disable in an `else` block silences messages in that block only."""


def first_line_of_else_block(fruits, apple):
    """Disable as the first line of the else block."""
    if fruits:
        print(fruits)
    else:
        # pylint: disable=protected-access
        print(apple._color)
    return apple._color  # [protected-access]


def line_above_else_keyword(fruits, apple):
    """Disable on the line just above the else keyword."""
    if fruits:
        print(fruits)
    # pylint: disable=protected-access
    else:
        print(apple._color)


def control(apple):
    """No disable: the message is emitted."""
    return apple._color  # [protected-access]
