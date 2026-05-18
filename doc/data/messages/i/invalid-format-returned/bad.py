class CustomFormat:
    """__format__ returns <type 'int'>"""

    def __format__(self, format_spec):  # [invalid-format-returned]
        return 1
