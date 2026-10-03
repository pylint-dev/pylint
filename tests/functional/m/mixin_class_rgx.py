"""Tests for the mixin-class-rgx option"""
# pylint: disable=too-few-public-methods


# Tests for not-async-context-manager


class AsyncManagerMixedin:
    """Class that does not match the option pattern"""

    def __aenter__(self):
        pass


class AsyncManagerMixin:
    """Class that does match the option pattern"""

    def __aenter__(self):
        pass


async def check_not_async_context_manager():
    """Function calling the classes for not-async-context-manager"""
    async with AsyncManagerMixedin:  # [not-async-context-manager]
        pass
    async with AsyncManagerMixin():
        pass


# Tests for attribute-defined-outside-init


class OutsideInitMixedin:
    """Class that does not match the option pattern"""

    def set_attribute(self):
        """Set an attribute outside of __init__"""
        self.attr = 1  # [attribute-defined-outside-init]


class OutsideInitMixin:
    """Class that does match the option pattern"""

    def set_attribute(self):
        """Set an attribute outside of __init__"""
        self.attr = 1


# Tests for no-member


class NoMemberMixedin:
    """Class that does not match the option pattern"""

MY_CLASS = OutsideInitMixedin().method() # [no-member]

class NoMemberMixin:
    """Class that does match the option pattern"""

MY_OTHER_CLASS = NoMemberMixin().method()
