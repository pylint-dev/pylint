"""Make sure no-member is not emitted when modifying __doc__ via augmented assignment

https://github.com/pylint-dev/pylint/issues/1078
"""
# pylint: disable=too-few-public-methods,missing-class-docstring
class Cls:
    def test(self):
        "a"

    test.__doc__ += "b"


print(Cls().test.__doc__)
print(Cls.test.__doc__)
