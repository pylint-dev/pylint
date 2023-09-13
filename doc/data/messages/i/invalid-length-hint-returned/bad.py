class CustomLengthHint:
    """__length_hint__ returns non-int"""

    def __length_hint__(self):  # [invalid-length-hint-returned]
        return 3.0
