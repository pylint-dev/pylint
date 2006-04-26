"""check empty except statement
"""

__revision__ = 0

if __revision__:
    try:
        print __revision__
    except:
        print 'error'

try:
    __revision__ += 1
except TypeError:
    print 'error'
except Exception:
    print 'error'
