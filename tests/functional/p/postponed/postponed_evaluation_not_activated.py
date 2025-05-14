# pylint: disable=missing-docstring,unused-argument,pointless-statement
# pylint: disable=too-few-public-methods

class Class:
    @classmethod
    def from_string(cls, source) -> Class:  # <3.14:[undefined-variable]
        ...

    def validate_b(self, obj: OtherClass) -> bool:  # <3.14:[used-before-assignment]
        ...


class OtherClass:
    ...
