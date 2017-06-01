"""checking pylint question"""
# pylint: disable=invalid-name
needed = False

if needed:
    test1 = "appelflap"
else:
    test1['somekey'] = 1234 # [used-before-assignment]
