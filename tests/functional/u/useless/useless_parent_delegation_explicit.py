"""Detect redundant overrides which call a parent by name (issue #5083)."""


class Parent:
    def __init__(self, value):
        self.value = value

    def method(self, value=1):
        return value

    def variadic(self, *args, flag=True, **kwargs):
        return args, flag, kwargs


class Redundant(Parent):
    def __init__(self, value):  # [useless-parent-delegation]
        Parent.__init__(self, value)

    def method(self, value=1):  # [useless-parent-delegation]
        return Parent.method(self, value)

    def variadic(self, *args, flag=True, **kwargs):  # [useless-parent-delegation]
        return Parent.variadic(self, *args, flag=flag, **kwargs)


ParentAlias = Parent


class Aliased(Parent):
    def method(self, value=1):  # [useless-parent-delegation]
        return ParentAlias.method(self, value)


class PositionalOnly(Parent):
    def method(self, /, value=1):  # [useless-parent-delegation]
        return Parent.method(self, value)


class NamedReceiver(Parent):
    def method(instance, value=1):  # [useless-parent-delegation]
        return Parent.method(instance, value)


class ChangedDefault(Parent):
    def method(self, value=2):
        return Parent.method(self, value)


class ChangedArgument(Parent):
    def method(self, value=1):
        return Parent.method(self, value + 1)


class OtherReceiver(Parent):
    def method(self, value=1):
        return Parent.method(value, value)


class ConstantReceiver(Parent):
    def method(self, value=1):
        return Parent.method(None, value)


class MissingReceiver(Parent):
    def method(self, value=1):
        return Parent.method()


class NoParameters(Parent):
    def method():
        return Parent.method(None)


class DifferentMethod(Parent):
    def method(self, value=1):
        return Parent.__init__(self, value)


class Unrelated:
    def method(self, value=1):
        return Parent.method(self, value)


class Intermediate(Parent):
    def method(self, value=1):
        return value + 1


class BypassedOverride(Intermediate):
    def method(self, value=1):
        return Parent.method(self, value)


class OtherParent:
    def method(self, value=1):
        return value + 2


class BypassedMro(OtherParent, Parent):
    def method(self, value=1):
        return Parent.method(self, value)


class MatchingMro(OtherParent, Parent):
    def method(self, value=1):  # [useless-parent-delegation]
        return OtherParent.method(self, value)


class EmptyParent:
    pass


class MissingMethod(EmptyParent):
    def method(self):
        return EmptyParent.method(self)


class InvalidMro(Parent, Parent):
    def method(self, value=1):
        return Parent.method(self, value)


class StaticParent:
    @staticmethod
    def method(value):
        return value


class InstanceOverride(StaticParent):
    def method(self, value):
        return StaticParent.method(value)


class StaticReceiver(StaticParent):
    def method(self):
        return StaticParent.method(self)


class ClassParent:
    @classmethod
    def method(cls, value):
        return value


class ClassReceiver(ClassParent):
    def method(self, value):
        return ClassParent.method(self, value)


class NonClassReceiver(Parent):
    def method(self, value=1):
        return value.method(value)


class ThroughEmptyParent(EmptyParent, Parent):
    def method(self, value=1):  # [useless-parent-delegation]
        return Parent.method(self, value)


class BuiltinParent(Exception):
    def __init__(self):
        Exception.__init__(self)


class UnknownBase(Unknown):
    def method(self, value=1):
        return value


class UnknownMro(UnknownBase):
    def method(self, value=1):
        return UnknownBase.method(self, value)
