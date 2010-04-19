#pylint: disable=C0111,C0321
"""pylint complains about 'index' being used before definition"""

__revision__ = None

print (index
       for index in range(10))
