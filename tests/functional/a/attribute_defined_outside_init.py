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
        setattr(self, "set_by_setattr", 1)  # [attribute-defined-outside-init]
        setattr(self, "defined_in_init", 2)
        setattr(self, "class_attr", 1)
        setattr(self, name, 1)

    def shadowed(self):
        def setattr(obj, name, value):  # pylint: disable=redefined-builtin,unused-argument
            return None

        setattr(self, "shadowed", 1)

    @classmethod
    def class_later(cls):
        setattr(cls, "class_attr", 1)


class ParentAttrInInit:
    def __init__(self):
        self.parent_attr = 1
        setattr(self, "defined_by_parent", 1)


class ChildSetattrForParentAttr(ParentAttrInInit):
    def later(self):
        setattr(self, "parent_attr", 2)
        setattr(self, "defined_by_parent", 2)


class AttributeMeta(type):
    def add_attribute(cls):
        setattr(cls, "class_attr", 1)


class StarArgs:
    def star(*args):  # pylint: disable=no-self-argument
        setattr(args, "grape", 4)


class PositionalOnlySetattr:
    def later(self, /):
        setattr(self, "positional_only", 1)  # [attribute-defined-outside-init]


class OtherInstanceSetattr:
    def later(self, other):
        setattr(other, "not_self", 1)


class NonMethodDefiningParent:
    __init__ = None


class ChildOfNonMethodDefiningParent(NonMethodDefiningParent):
    def later(self):
        setattr(self, "not_defined_by_parent", 1)  # [attribute-defined-outside-init]


class ChildAssignmentForParentSetattr(ParentAttrInInit):
    def later(self):
        self.defined_by_parent = 2


class ParentWithNestedSetattr:
    def __init__(self):
        def rename(self):
            setattr(self, "nested_attr", 1)

        rename(object())


class ChildOfParentWithNestedSetattr(ParentWithNestedSetattr):
    def later(self):
        setattr(self, "nested_attr", 2)  # [attribute-defined-outside-init]


class TwoArgumentSetattr:
    def __init__(self):
        setattr(self, "two_arg")  # TypeError at runtime, defines nothing

    def later(self):
        setattr(self, "two_arg", 1)  # [attribute-defined-outside-init]


class ClassAndStaticSetattr:
    @classmethod
    def from_class(cls):
        setattr(cls, "made_in_classmethod", 1)

    @staticmethod
    def from_static(self):  # pylint: disable=bad-staticmethod-argument
        setattr(self, "made_in_staticmethod", 1)


class ShadowedSetattr:
    def later(self):
        def setattr(obj, name, value):  # pylint: disable=redefined-builtin,unused-argument
            return None

        setattr(self, "not_really_set", 1)


class SameClassSetattrThenAssign:
    def __init__(self):
        setattr(self, "from_init", 1)

    def later(self):
        self.from_init = 2


class G:
    """https://github.com/pylint-dev/pylint/issues/5214"""

    def __init__(self):
        self.init_helper()

    def init_helper(self):
        self.var1 = True

    def other_func(self):
        self.var1 = False


class HParent:
    def __init__(self):
        self.init_helper()

    def init_helper(self):
        self.var1 = True


class HDerived(HParent):
    def other_func(self):
        self.var1 = False


class UnrelatedHelperOwner:
    def init_helper(self):
        """Same name as SameNameHelperCall.init_helper, other class."""


class SameNameHelperCall:
    # '_called_in_methods' matches the called method by name only, so calling
    # 'init_helper' on another object counts as calling our own: both
    # assignments below are known false negatives.
    def __init__(self):
        self.other = UnrelatedHelperOwner()
        self.other.init_helper()

    def init_helper(self):
        self.var1 = True

    def other_func(self):
        self.var1 = False
