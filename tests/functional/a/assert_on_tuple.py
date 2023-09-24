'''Assert check example'''

# pylint: disable=comparison-with-itself, comparison-of-constants, line-too-long
assert (1 == 1, 2 == 2), "message is raised even when there is an assert message"  # [assert-on-tuple]
assert (1 == 1, 2 == 2) # [assert-on-tuple]
assert 1 == 1, "no error"
assert (1 == 1, ), "message is raised even when there is an assert message"  # [assert-on-tuple]
assert (1 == 1, ) # [assert-on-tuple]
assert (1 == 1, 2 == 2, 3 == 5), "message is raised even when there is an assert message"  # [assert-on-tuple]
assert ()
assert (True, 'error msg') # [assert-on-tuple]
