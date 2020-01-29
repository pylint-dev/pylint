# pylint: disable=missing-docstring


def test_pragma():
    """Test that the control pragmas are not too eager to consume the entire line

    We should stop either at:
    - ; or #
    - or at the end of line
    """
    # noqa: E501 # pylint: disable=unused-variable #nosec
    variable = 1

    # noqa # pylint: disable=undefined-variable,no-member; don't trigger
    other_variable = some_variable + variable.member

    # noqa # pylint: disable=unbalanced-tuple-unpacking,no-member # no trigger
    first, second = some_other_variable
    return first + other_variable.method()
