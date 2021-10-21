""" docstring for file property_pattern.py """


class FuncHolder:
    def __init__(self, f_set, f_get, f_del, docstr):
        pass


class PropertyPatterns:
    prop1 = property(lambda x: (x) * 2, None, None, "property usage 1")

    @property
    def prop2(self):
        """property usage 2"""
        return self._prop2

    @prop2.setter
    def prop2(self, value):
        self._prop2 = value * 2

    prop3 = FuncHolder(lambda x: (x) * 3, None, None, "non property 1")

    prop4 = lambda self, x: x * 2  # noqa: E731

    def __init__(self):
        pass
