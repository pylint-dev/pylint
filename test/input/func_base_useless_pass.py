"""W0107: unnecessary pass statement
"""
__revision__ = None

try:
    A = 2
except ValueError:
    print A
    pass
