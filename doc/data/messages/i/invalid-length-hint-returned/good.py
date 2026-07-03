class CustomLengthHint:
    """__length_hint__ returns <type 'int'>"""

    def __length_hint__(self):
        return 10
