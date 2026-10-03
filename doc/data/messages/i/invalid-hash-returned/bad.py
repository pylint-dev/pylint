class CustomHash:
    """__hash__ returns dict"""

    def __hash__(self):  # [invalid-hash-returned]
        return {}
