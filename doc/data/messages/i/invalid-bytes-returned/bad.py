class CustomBytes:
    """__bytes__ returns <type 'str'>"""

    def __bytes__(self):  # [invalid-bytes-returned]
        return "123"
