# -*- encoding=utf-8 -*-
#pylint: disable=C0111
def foo(): #pylint: disable=C0102
    return 1

def toto(): #pylint: disable=C0102,R1711
    return

# +1: [missing-docstring]
def test_enabled_by_id_msg(): #pylint: enable=C0111
    pass
