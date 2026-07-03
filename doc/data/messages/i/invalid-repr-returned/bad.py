class CustomRepr:
    """__repr__ returns <type 'int'>"""

    def __repr__(self):  # [invalid-repr-returned]
        return 1
