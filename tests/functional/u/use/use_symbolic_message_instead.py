# pylint: disable=C0111,R0903,T1234  # [unknown-option-value,use-symbolic-message-instead,use-symbolic-message-instead]
# pylint: enable=c0111,w0223   # [use-symbolic-message-instead,use-symbolic-message-instead]

def my_function(arg):  # [missing-function-docstring]
    return arg or True

# pylint: disable=C0111  # [use-symbolic-message-instead]
# pylint: enable=R0903  # [use-symbolic-message-instead]
# pylint: disable=R0903  # [use-symbolic-message-instead]


def foo():  # pylint: disable=C0102  # [use-symbolic-message-instead]
    return 1


def toto():  # pylint: disable=C0102,R1711  # [use-symbolic-message-instead,use-symbolic-message-instead]
    return


def test_enabled_by_id_msg():  # pylint: enable=C0111  # [use-symbolic-message-instead,missing-function-docstring]
    pass


def baz():  # pylint: disable=blacklisted-name
    return 1
