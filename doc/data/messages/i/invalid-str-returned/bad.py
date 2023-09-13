class CustomStr:
    """__str__ returns int"""

    def __str__(self):  # [invalid-str-returned]
        return 1
