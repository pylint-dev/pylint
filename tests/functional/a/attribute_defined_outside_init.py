# pylint: disable=missing-docstring,too-few-public-methods,invalid-name

class A:

    def __init__(self):
        self.x = 0
        self.setUp()

    def set_y(self, y):
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_z(self, z):
        self.z = z # [attribute-defined-outside-init]

    def setUp(self):
        self.x = 0
        self.y = 0


class B(A):

    def test(self):
        self.z = 44 # [attribute-defined-outside-init]


class C:

    def __init__(self):
        self._init()

    def _init(self):
        self.z = 44


class D:

    def setUp(self):
        self.set_z()

    def set_z(self):
        self.z = 42


class E:

    def __init__(self):
        i = self._init
        i()

    def _init(self):
        self.z = 44


class Mixin:

    def test_mixin(self):
        """Don't emit attribute-defined-outside-init for mixin classes."""
        if self.defined_already: # pylint: disable=access-member-before-definition
            self.defined_already = None


class F:
    def func(self):
        self.__dict__ = {'foo': 'bar'}


class Mine:
    def __init__(self, param):
        self.prop = param

    @property
    def prop(self):
        return self.__prop

    @prop.setter
    def prop(self, value):
        self.__prop = value

class DataClass:
    def __post_init__(self):
        self.a = 42


class SetattrAttributeDefinitions:
    class_attr = None

    def __init__(self):
        setattr(self, "defined_in_init", 1)

    def later(self, name):
        setattr(self, "set_by_setattr", 1)  # [attribute-defined-outside-init]  # noqa: B010
        setattr(self, "defined_in_init", 2)  # noqa: B010
        setattr(self, "class_attr", 1)  # noqa: B010
        setattr(self, name, 1)

    def shadowed(self):
        def setattr(obj, name, value):  # pylint: disable=redefined-builtin,unused-argument
            return None

        setattr(self, "shadowed", 1)

    @classmethod
    def class_later(cls):
        setattr(cls, "class_attr", 1)  # noqa: B010


class ParentAttrInInit:
    def __init__(self):
        self.parent_attr = 1
        setattr(self, "defined_by_parent", 1)  # noqa: B010


class ChildSetattrForParentAttr(ParentAttrInInit):
    def later(self):
        setattr(self, "parent_attr", 2)  # noqa: B010
        setattr(self, "defined_by_parent", 2)  # noqa: B010
