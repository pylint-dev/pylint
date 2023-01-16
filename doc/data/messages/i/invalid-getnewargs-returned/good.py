class GoodGetNewArgs:
    """__getnewargs__ returns <type 'tuple'>"""

    def __getnewargs__(self):
        return (1, 2)
