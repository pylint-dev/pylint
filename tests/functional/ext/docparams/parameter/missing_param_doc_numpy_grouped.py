"""Regression test for https://github.com/pylint-dev/pylint/issues/3420.

Numpy style docstrings can document several parameters on one line,
``x, y, z : int``. Those count as documented, also when other parameters
follow on their own line.
"""


def grouped_only(valx, valy, valz):
    """Add three numbers.

    Parameters
    ----------
    valx, valy, valz : int
        The numbers to add.

    Returns
    -------
    int
        The sum.
    """
    return valx + valy + valz


def grouped_then_single(valx, valy, valz, factor):
    """Add three numbers, then multiply the sum.

    Parameters
    ----------
    valx, valy, valz : int
        The numbers to add.
    factor : int
        What to multiply the sum by.

    Returns
    -------
    int
        The sum times the factor.
    """
    return (valx + valy + valz) * factor


def grouped_with_missing(valx, valy, valz, factor):  # [missing-param-doc, missing-type-doc]
    """Add three numbers, then multiply the sum.

    Parameters
    ----------
    valx, valy : int
        Two of the numbers to add.
    factor : int
        What to multiply the sum by.

    Returns
    -------
    int
        The sum times the factor.
    """
    return (valx + valy + valz) * factor
