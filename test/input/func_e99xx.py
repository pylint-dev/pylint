"""test string format error
"""

__revision__ = 1

PARG_1 = PARG_2 = PARG_3 = 1

def pprint():
    """Test string format
    """
    print "%s %s" % {'PARG_1': 1, 'PARG_2': 2} # E9906
    print "%s" % (PARG_1, PARG_2) # E9905
    print "%(PARG_1)d %d" % {'PARG_1': 1, 'PARG_2': 2} # E9902
    print "%(PARG_1)d %(PARG_2)d" % {'PARG_1': 1} # E9904
    print "%(PARG_1)d %(PARG_2)d" % {'PARG_1': 1, 'PARG_2':2, 'PARG_3':3} # W9901
    print "%(PARG_1)d %(PARG_2)d" % {'PARG_1': 1, 2:3} # W9900 E9904
    print "%(PARG_1)d %(PARG_2)d" % (2, 3) # 9903
    print "%(PARG_1)d %(PARG_2)d" % [2, 3] # 9903
    print "%2z" % PARG_1
    print "strange format %2" % PARG_2

