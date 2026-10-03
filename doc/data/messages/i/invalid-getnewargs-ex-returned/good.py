class CustomGetNewArgsEx:
    """__getnewargs_ex__ returns <type 'tuple'>"""

    def __getnewargs_ex__(self):
        return ((1,), {"2": 2})
