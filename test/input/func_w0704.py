"""test empty except
"""

__revision__ = 1

try:
    __revision__ += 1
except TypeError:
    pass

try:
    __revision__ += 1
except TypeError:
    pass
else:
    __revision__ = None 
