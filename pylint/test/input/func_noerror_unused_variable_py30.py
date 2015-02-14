""" Test nonlocal uses and unused-variable. """

__revision__ = 1

def test_nonlocal():
    """ Test that assigning to a nonlocal does not trigger
    an 'unused-variable' warnings.
    """
    attr = True
    def set_value(val):
        """ Set the value in a nonlocal. """
        nonlocal attr
        attr = val
    return set_value
