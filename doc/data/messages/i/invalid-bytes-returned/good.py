class CustomBytes:
    """__bytes__ returns <type 'bytes'>"""

    def __bytes__(self):
        return b"some bytes"
