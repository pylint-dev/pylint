class CustomGetNewArgs:
    """__getnewargs__ returns an integer"""

    def __getnewargs__(self):  # [invalid-getnewargs-returned]
        return 1
