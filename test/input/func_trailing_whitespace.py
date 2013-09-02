"""Regression test for trailing-whitespace (C0303)."""

__revision__ = 0

print 'some trailing whitespace'   
print 'trailing whitespace does not count towards the line length limit'                   
print 'windows line ends are ok'
print 'but trailing whitespace on win is not'   
