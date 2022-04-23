# pylint: disable=missing-docstring,too-few-public-methods

class Meta(type):
    @property
    def values(cls):
        return ['foo', 'bar']


class Parent(metaclass=Meta):
    pass


assert 'foo' in Parent.values  # no warning
for value in Parent.values:  # no warning
    print(value)


class Child(Parent):
    pass


assert 'foo' in Child.values  # false-positive: unsupported-membership-test
for value in Child.values:  # false-positive: not-an-iterable
    print(value)


class Meta2(type):
    def a_method(cls):
        return [123]


class Parent2(metaclass=Meta2):
    @property
    def a_method(self):
        return "actually a property"


class Child2(Parent2):
    pass


assert 123 in Child2.a_method  # [unsupported-membership-test]
for value in Child2.a_method:  # [not-an-iterable]
    print(value)
