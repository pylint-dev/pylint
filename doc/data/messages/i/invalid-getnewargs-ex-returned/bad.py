class CustomGetNewArgsEx:
    """__getnewargs_ex__ returns tuple with incorrect arg length"""

    def __getnewargs_ex__(self):  # [invalid-getnewargs-ex-returned]
        return (tuple(1), dict(x="y"), 1)
