"""
Test for names within keyword and position only function

This test is 3.8+ as the columns are not correctly identified
by the ast parser < 3.8
"""
# pylint: disable=unused-argument,too-many-arguments


def name(
    some_thing_long_but_okay,
    not_okay_łol,  # [non-ascii-name]
    not_okay_defaułt=None,  # [non-ascii-name]
    /,
    p_or_kw_okay=None,
    p_or_kw_not_økay=None,  # [non-ascii-name]
    *,
    kw_arg_okay,
    kw_arg_not_økay,  # [non-ascii-name]
):
    """
    Do something!
    """
    return "Foobar"
