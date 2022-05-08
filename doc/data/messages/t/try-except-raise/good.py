# The try except might be remove entirely:
1 / 0

# Or another more detailed exception can be raised:
try:
    1 / 0
except ZeroDivisionError as e:
    raise ValueError("The area of the rectangle cannot be zero") from e
