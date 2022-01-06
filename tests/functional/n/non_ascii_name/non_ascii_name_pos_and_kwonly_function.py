"""
Test for names within keyword and position only function
"""
# pylint: disable=unused-argument


def name(
    some_thing_long_but_okay,
    not_okay_łol,  # [non-ascii-identifier]
    not_okay_defaułt=None,  # [non-ascii-identifier]
    /,
    p_or_kw_okay=None,
    p_or_kw_not_økay=None,  # [non-ascii-identifier]
    *,
    kw_arg_okay,
    kw_arg_not_økay,  # [non-ascii-identifier]
):
    """
    Do something!
    """
    return "Foobar"
