"""Use symbolic message instead are also tested in messages_managed_by_id.py"""

# pylint: disable=C0111,R0903,T1234  # [bad-option-value,use-symbolic-message-instead,use-symbolic-message-instead]
# pylint: enable=C0111   # [use-symbolic-message-instead]

def myfunction(arg):  # [missing-function-docstring]
    return arg or True

# pylint: disable=C0111  # [use-symbolic-message-instead]
# pylint: enable=R0903  # [use-symbolic-message-instead]
# pylint: disable=R0903  # [use-symbolic-message-instead]
