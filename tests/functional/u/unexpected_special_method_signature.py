"""Test for special methods implemented incorrectly."""

# pylint: disable=missing-docstring, unused-argument, too-few-public-methods
# pylint: disable=invalid-name,too-many-arguments,bad-staticmethod-argument

class Invalid:

    def __enter__(self, other): # [unexpected-special-method-signature]
        pass

    def __del__(self, other): # [unexpected-special-method-signature]
        pass

    def __format__(self, other, other2): # [unexpected-special-method-signature]
        pass

    def __setattr__(self): # [unexpected-special-method-signature]
        pass

    def __round__(self, invalid, args): # [unexpected-special-method-signature]
        pass

    def __deepcopy__(self, memo, other): # [unexpected-special-method-signature]
        pass

    def __iter__(): # [no-method-argument]
        pass

    @staticmethod
    def __getattr__(self, nanana): # [unexpected-special-method-signature]
        pass

    def __subclasses__(self, blabla):  # [unexpected-special-method-signature]
        pass


class FirstBadContextManager:
    def __enter__(self):
        return self
    def __exit__(self, exc_type): # [unexpected-special-method-signature]
        pass

class SecondBadContextManager:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, value, tb, stack): # [unexpected-special-method-signature]
        pass

class ThirdBadContextManager:
    def __enter__(self):
        return self

    # +1: [unexpected-special-method-signature]
    def __exit__(self, exc_type, value, tb, stack, *args):
        pass


class Async:

    def __aiter__(self, extra): # [unexpected-special-method-signature]
        pass
    def __anext__(self, extra, argument): # [unexpected-special-method-signature]
        pass
    def __await__(self, param): # [unexpected-special-method-signature]
        pass
    def __aenter__(self, first): # [unexpected-special-method-signature]
        pass
    def __aexit__(self): # [unexpected-special-method-signature]
        pass


class Valid:

    def __new__(cls, test, multiple, args):
        pass

    # pylint: disable-next=too-many-positional-arguments
    def __init__(self, this, can, have, multiple, args, as_well):
        pass

    def __call__(self, also, trv, for_this):
        pass

    def __round__(self, n):
        pass

    def __index__(self, n=42):
        """Expects 0 args, but we are taking in account arguments with defaults."""

    def __deepcopy__(self, memo):
        pass

    def __format__(self, format_specification=''):
        pass

    def __copy__(self, this=None, is_not=None, necessary=None):
        pass

    @staticmethod
    def __enter__():
        pass

    @staticmethod
    def __getitem__(index):
        pass

    @classmethod
    def __init_subclass__(cls, blabla):
        pass


class FirstGoodContextManager:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, value, tb):
        pass

class SecondGoodContextManager:
    def __enter__(self):
        return self
    def __exit__(self, exc_type=None, value=None, tb=None):
        pass

class ThirdGoodContextManager:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, *args):
        pass


# unexpected-special-method-signature
# https://github.com/pylint-dev/pylint/issues/6644
class Philosopher:
    def __init_subclass__(cls, default_name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.default_name = default_name

class AustralianPhilosopher(Philosopher, default_name="Bruce"):
    pass
