# property_decorator.py
class AnnotatedPropertyTest:
    """Test class for property decorators with annotated return type"""
    def __init__(self):
        self._x = 0

    @property
    def x(self) -> int:
        """This is a getter for x"""
        return self._x

    @x.setter
    def x(self, value):
        """This is a setter for x"""
        self._x = value

    @x.deleter
    def x(self):
        """This is a deleter for x"""
        del self._x


class NonAnnotatedPropertyTest:
    """Test class for property decorators without annotated return type"""
    def __init__(self):
        self._x = 0

    @property
    def x(self):
        """This is a getter for x"""
        return self._x

    @x.setter
    def x(self, value):
        """This is a setter for x"""
        self._x = value

    @x.deleter
    def x(self):
        """This is a deleter for x"""
        del self._x
