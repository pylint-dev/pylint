# pylint: disable=missing-docstring,invalid-name,too-few-public-methods


def test(**kwargs):
    print(kwargs)

# metaclasses as mappings
class Meta(type):
    def __getitem__(cls, key):
        return ord(key)

    def keys(cls):
        return ['a', 'b', 'c']

class SomeClass(metaclass=Meta):
    pass

test(**SomeClass)
test(**SomeClass())  # [not-a-mapping]
