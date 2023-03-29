# pylint: disable=missing-docstring,too-few-public-methods

def test_unused(first, second, _not_used): # [unused-argument, unused-argument]
    pass


def test_prefixed_with_ignored(first, ignored_second):
    first()


def test_prefixed_with_unused(first, unused_second):
    first()

# for Sub.inherited, only the warning for "aay" is desired.
# The warnings for "aab" and "aac"  are most likely false positives though,
# because there could be another subclass that overrides the same method and does
# use the arguments (e.g. Sub2)


class Base:
    "parent"
    def inherited(self, aaa, aab, aac):
        "abstract method"
        raise NotImplementedError

class Sub(Base):
    "child 1"
    def inherited(self, aaa, aab, aac):
        "overridden method, though don't use every argument"
        return aaa

    def newmethod(self, aax, aay):  # [unused-argument]
        "another method, warning for aay desired"
        return self, aax

class Sub2(Base):
    "child 1"

    def inherited(self, aaa, aab, aac):
        "overridden method, use every argument"
        return aaa + aab + aac

def metadata_from_dict(key):
    """
    Should not raise unused-argument message because key is
    used inside comprehension dict
    """
    return {key: str(value) for key, value in key.items()}


def metadata_from_dict_2(key):
    """Similar, but with more nesting"""
    return {key: (a, b) for key, (a, b) in key.items()}


# pylint: disable=too-few-public-methods, wrong-import-position


def function(arg=1):  # [unused-argument]
    """ignore arg"""


class AAAA:
    """dummy class"""

    def method(self, arg):  # [unused-argument]
        """dummy method"""
        print(self)
    def __init__(self, *unused_args, **unused_kwargs):
        pass

    @classmethod
    def selected(cls, *args, **kwargs):  # [unused-argument, unused-argument]
        """called by the registry when the vobject has been selected.
        """
        return cls

    def using_inner_function(self, etype, size=1):
        """return a fake result set for a particular entity type"""
        rset = AAAA([('A',)]*size, f'{etype} X',
                    description=[(etype,)]*size)
        def inner(row, col=0, etype=etype, req=self, rset=rset):
            """inner using all its argument"""
            # pylint: disable=maybe-no-member
            return req.vreg.etype_class(etype)(req, rset, row, col)
        # pylint: disable = attribute-defined-outside-init
        rset.get_entity = inner

class BBBB:
    """dummy class"""

    def __init__(self, arg):  # [unused-argument]
        """Constructor with an extra parameter. Should raise a warning"""
        self.spam = 1


# Regression test for https://github.com/pylint-dev/pylint/issues/5771
# involving keyword-only arguments
class Ancestor:
    def __init__(self):
        self.thing = None

    def set_thing(self, thing, *, other=None):  # [unused-argument]
        self.thing = thing

class Descendant(Ancestor):
    def set_thing(self, thing, *, other=None):
        """Subclass does not raise unused-argument"""
        self.thing = thing


# Test that Class with both `__init__` and `__new__` don't check
# on `__new__` for unused arguments

# pylint: disable=invalid-name

class TestClassWithInitAndNew:
    def __init__(self, argA, argB):
        self.argA = argA
        self.argB = argB

    def __new__(cls, argA, argB):
        return object.__new__(cls)

# Test that `__new__` method is checked for unused arguments
# when `__init__` is not in the Class

class TestClassWithOnlyNew:
    def __new__(cls, argA, argB): # [unused-argument, unused-argument]
        return object.__new__(cls)
