try:
    1 / 0
except ValueError + TypeError:  # [wrong-exception-operation]
    pass
