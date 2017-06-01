"""checking pylint question"""
# pylint: disable=invalid-name,using-constant-test
needed = False

if needed:
    test1 = "appelflap"
elif True:
    test1['test'] = 1234 # [used-before-assignment]
else:
    test1['somekey'] = 1234
