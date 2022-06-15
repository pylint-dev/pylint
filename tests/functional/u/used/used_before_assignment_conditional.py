"""used-before-assignment cases involving IF conditions"""
if 1 + 1 == 2:
    x = x + 1  # [used-before-assignment]

if y:  # [used-before-assignment]
    y = y + 1

if (z := z):  # [used-before-assignment]
    z = z + 1
