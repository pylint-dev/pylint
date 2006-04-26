"""test max branch 
"""

__revision__ = ''

def stupid_function(arg):
    """reallly stupid function"""
    if arg == 1:
        print 1
    elif arg == 2:
        print 2
    elif arg == 3:
        print 3
    elif arg == 4:
        print 4
    elif arg == 5:
        print 5
    elif arg == 6:
        print 6
    elif arg == 7:
        print 7
    elif arg == 8:
        print 8
    elif arg == 9:
        print 9
    elif arg == 10:
        print 10
    else:
        if arg < 1:
            print 0
        else:
            print 100
        arg = 0
    if arg:
        print None
    else:
        print arg
