# pylint: disable=missing-docstring,no-self-use,unused-argument,pointless-statement
# pylint: disable=too-few-public-methods

class Class:
    @classmethod
    def from_string(cls, source) -> Class:  # [undefined-variable]
        ...

    def validate_b(self, obj: OtherClass) -> bool:  # [used-before-assignment]
        ...


class OtherClass:
    ...
