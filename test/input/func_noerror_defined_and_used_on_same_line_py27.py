#pylint: disable=C0111,C0321
"""pylint complains about 'index' being used before definition"""

__revision__ = 1

with open('f') as f, open(f.read()) as g:
    print g.read()
