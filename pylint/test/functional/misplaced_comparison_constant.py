"""Check that the constants are on the right side of the comparisons"""

# pylint: disable=singleton-comparison
def bad_comparisons():
    """this is not ok: 5 should be on the right"""
    for i in range(10):
        if 5 <= i:  # [misplaced-comparison-constant]
            print "foo"
        if True == True:  # [misplaced-comparison-constant]
            pass
        if 'bar' != 'foo':  # [misplaced-comparison-constant]
            pass
        if 1 == i:  # [misplaced-comparison-constant]
            print "bar"

def good_comparison():
    """this is ok"""
    for i in range(10):
        if i == 5:
            print "foo"
