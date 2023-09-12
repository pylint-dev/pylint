class CustomFormat:
    """__format__ returns <type 'str'>"""

    def __format__(self, format_spec):
        return "hello!"
