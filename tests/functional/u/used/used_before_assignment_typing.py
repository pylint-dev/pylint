"""Tests for used-before-assignment for typing related issues"""
# pylint: disable=missing-function-docstring,ungrouped-imports,invalid-name


from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    if True:  # pylint: disable=using-constant-test
        import math
    import dbm
    print(dbm)  # no error when defined and used in the same false branch
    from urllib.request import urlopen
    import array
    import base64
    import binascii
    import calendar
    import collections
    import copy
    import datetime
    import email
    import heapq
    import json
    import mailbox
    import mimetypes
    import numbers
    import pprint
    import types
    import zoneinfo
elif input():
    import calendar, bisect  # pylint: disable=multiple-imports
    if input() + 1:
        import heapq
    else:
        import heapq
elif input():
    try:
        numbers = None if input() else 1
        import array
    except Exception as e:  # pylint: disable=broad-exception-caught
        import types
    finally:
        copy = None
elif input():
    for i in range(1,2):
        email = None
    else:  # pylint: disable=useless-else-on-loop
        json = None
    while input():
        import mailbox
    else:  # pylint: disable=useless-else-on-loop
        mimetypes = None
elif input():
    with input() as base64:
        pass
    with input() as temp:
        import binascii
else:
    from urllib.request import urlopen
    zoneinfo: str = ''
    def pprint():
        pass
    class collections:  # pylint: disable=too-few-public-methods,missing-class-docstring
        pass

class MyClass:
    """Type annotation or default values for first level methods can't refer to their own class"""

    def incorrect_typing_method(
        self, other: MyClass  # [undefined-variable]
    ) -> bool:
        return self == other

    def incorrect_nested_typing_method(
        self, other: List[MyClass]  # [undefined-variable]
    ) -> bool:
        return self == other[0]

    def incorrect_default_method(
        self, other=MyClass()  # [undefined-variable]
    ) -> bool:
        return self == other

    def correct_string_typing_method(self, other: "MyClass") -> bool:
        return self == other

    def correct_inner_typing_method(self) -> bool:
        def inner_method(self, other: MyClass) -> bool:
            return self == other

        return inner_method(self, MyClass())


class MySecondClass:
    """Class to test self referential variable typing.
    This regressed, reported in: https://github.com/pylint-dev/pylint/issues/5342
    """

    def self_referential_optional_within_method(self) -> None:
        variable: Optional[MySecondClass] = self
        print(variable)

    def correct_inner_typing_method(self) -> bool:
        def inner_method(self, other: MySecondClass) -> bool:
            return self == other

        return inner_method(self, MySecondClass())


class MyOtherClass:
    """Class to test self referential variable typing, no regression."""

    def correct_inner_typing_method(self) -> bool:
        def inner_method(self, other: MyOtherClass) -> bool:
            return self == other

        return inner_method(self, MyOtherClass())

    def self_referential_optional_within_method(self) -> None:
        variable: Optional[MyOtherClass] = self
        print(variable)


class MyThirdClass:
    """Class to test self referential variable typing within conditionals.
    This regressed, reported in: https://github.com/pylint-dev/pylint/issues/5499
    """

    def function(self, var: int) -> None:
        if var < 0.5:
            _x: MyThirdClass = self

    def other_function(self) -> None:
        _x: MyThirdClass = self


class MyFourthClass:  # pylint: disable=too-few-public-methods
    """Class to test conditional imports guarded by TYPE_CHECKING two levels
    up then used in function annotation. See https://github.com/pylint-dev/pylint/issues/7539"""

    def is_close(self, comparator: math.isclose, first, second):  # [used-before-assignment]
        """Conditional imports guarded are only valid for variable annotations."""
        comparator(first, second)


class VariableAnnotationsGuardedByTypeChecking:  # pylint: disable=too-few-public-methods
    """Class to test conditional imports guarded by TYPE_CHECKING then used in
    local (function) variable annotations, which are not evaluated at runtime.

    See: https://github.com/pylint-dev/pylint/issues/7609
    and https://github.com/pylint-dev/pylint/issues/7882
    """

    still_an_error: datetime.date  # [used-before-assignment]

    def print_date(self, date) -> None:
        date: datetime.date = date
        print(date)

        import datetime  # pylint: disable=import-outside-toplevel


class ConditionalImportGuardedWhenUsed:  # pylint: disable=too-few-public-methods
    """Conditional imports also guarded by TYPE_CHECKING when used."""
    if TYPE_CHECKING:
        print(urlopen)


class TypeCheckingMultiBranch:  # pylint: disable=too-few-public-methods,unused-variable
    """Test for defines in TYPE_CHECKING if/elif/else branching"""
    def defined_in_elif_branch(self) -> calendar.Calendar:  # [possibly-used-before-assignment]
        print(bisect)  # [possibly-used-before-assignment]
        return calendar.Calendar()

    def defined_in_else_branch(self) -> urlopen:
        print(zoneinfo)  # [used-before-assignment]
        print(pprint())
        print(collections())
        return urlopen

    def defined_in_nested_if_else(self) -> heapq:  # [possibly-used-before-assignment]
        print(heapq)
        return heapq

    def defined_in_try_except(self) -> array:  # [used-before-assignment]
        print(types)  # [used-before-assignment]
        print(copy)  # [used-before-assignment]
        print(numbers)  # [used-before-assignment]
        return array

    def defined_in_loops(self) -> json:  # [used-before-assignment]
        print(email)  # [used-before-assignment]
        print(mailbox)  # [used-before-assignment]
        print(mimetypes)  # [used-before-assignment]
        return json

    def defined_in_with(self) -> base64:  # [used-before-assignment]
        print(binascii)  # [used-before-assignment]
        return base64
