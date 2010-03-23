'''Assert check example'''
__revision__ = 0

assert (1 == 1, 2 == 2), "no error"
assert (1 == 1, 2 == 2) #this should generate a warning
assert 1 == 1, "no error"
assert (1 == 1, ), "no error"
assert (1 == 1, )
assert (1 == 1, 2 == 2, 3 == 5), "no error"
assert ()
assert (True,'error msg') #this should generate a warning
