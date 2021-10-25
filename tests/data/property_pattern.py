""" docstring for file property_pattern.py """
class PropertyPatterns:
    prop1 = property(lambda self: self._prop1*2, None, None, "property usage 1")

    @property
    def prop2(self):
        """property usage 2"""
        return self._prop2

    @prop2.setter
    def prop2(self, value):
        self._prop2 = value * 2

    def __init__(self):
        self._prop1=1
        self._prop2=2
