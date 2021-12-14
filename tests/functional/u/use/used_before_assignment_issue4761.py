"""used-before-assignment (E0601)"""
def function():
    """Consider that except blocks may not execute."""
    try:
        pass
    except ValueError:
        some_message = 'some message'

    if not some_message:  # [used-before-assignment]
        return 1

    return some_message
