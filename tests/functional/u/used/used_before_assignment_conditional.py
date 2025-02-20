"""used-before-assignment cases involving IF conditions"""

if 1 + 1 == 2:
    X = X + 1  # [used-before-assignment]

if Y:  # [used-before-assignment]
    Y = Y + 1
