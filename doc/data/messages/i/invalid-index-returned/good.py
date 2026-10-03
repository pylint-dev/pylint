class CustomIndex:
    """__index__ returns <type 'int'>"""

    def __index__(self):
        return 19
