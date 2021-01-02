"""Use symbolic message instead are also tested in use_symbolic_message_instead.py"""
# pylint: disable=C0111  # [use-symbolic-message-instead]


def foo():  # pylint: disable=C0102  # [use-symbolic-message-instead]
    return 1


def toto():  # pylint: disable=C0102,R1711  # [use-symbolic-message-instead,use-symbolic-message-instead]
    return


def test_enabled_by_id_msg():  # pylint: enable=C0111  # [use-symbolic-message-instead,missing-function-docstring]
    pass


def baz(): #pylint: disable=blacklisted-name
    return 1
