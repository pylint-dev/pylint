"""Tests for non-standard-exit-argument-names."""

# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods
# pylint: disable=unused-argument,invalid-name,unexpected-special-method-signature
# pylint: disable=redefined-outer-name


class Good:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None


class AsyncGood:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return None


class ShortNames:
    def __exit__(self, t, v, tb):  # [non-standard-exit-argument-names]
        return None


class AbbreviatedNames:
    def __exit__(self, exc_type, exc_val, exc_tb):  # [non-standard-exit-argument-names]
        return None


class AsyncBadNames:
    async def __aexit__(self, typ, value, tb):  # [non-standard-exit-argument-names]
        return None


class PositionalOnly:
    def __exit__(self, t, v, tb, /):  # [non-standard-exit-argument-names]
        return None


class IgnoredNames:
    def __exit__(self, _, __, ___):
        return None


class PartlyIgnored:
    def __exit__(self, exc_type, _exc_value, tb):  # [non-standard-exit-argument-names]
        return None


class StarArgs:
    def __exit__(self, *args):
        return None


class StarArgsAfterNames:
    def __exit__(self, t, v, tb, *args, **kwargs):
        return None


class DefaultValues:
    def __exit__(self, t=None, v=None, tb=None):  # [non-standard-exit-argument-names]
        return None


class WrongArity:
    def __exit__(self, exc_type, exc_value):
        return None


class StaticExit:
    @staticmethod
    def __exit__(t, v, tb):
        return None


def __exit__(t, v, tb):
    """Module-level function, not a context manager method."""


class Outer:
    def method(self):
        def __exit__(t, v, tb):
            return None

        return __exit__


class NotExit:
    def __enter__(self, t, v, tb):
        return self
